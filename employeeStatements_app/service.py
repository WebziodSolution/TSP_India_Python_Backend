import logging
import math
from datetime import datetime, timedelta, time
from decimal import Decimal, ROUND_HALF_UP
import pytz

from django.db.models import Q
from common.models import (
    CompanyEmployee,
    UserInOut,
    AttendancePenaltyRules,
    Deductions,
    EmployeeLeaveMaster
)
from holidayTemplates_app.service import HolidayTemplatesService
from common.service import CommonService

logger = logging.getLogger(__name__)

class EmployeeSalaryStatementService:
    def __init__(self):
        self.holiday_templates_service = HolidayTemplatesService()
        self.common_service = CommonService()

    def get_employee_salary_statements(self, request_dto: dict) -> list:
        try:
            salary_statement_list = []
            
            employee_ids = request_dto.get("employeeIds")
            department_ids = request_dto.get("departmentIds")
            company_id = request_dto.get("companyId")

            has_employee_filter = employee_ids is not None and isinstance(employee_ids, list) and len(employee_ids) > 0
            has_department_filter = department_ids is not None and isinstance(department_ids, list) and len(department_ids) > 0

            if not has_employee_filter and not has_department_filter:
                company_employees = CompanyEmployee.objects.filter(companyDetails_id=company_id)
            else:
                spec = Q()
                if has_employee_filter:
                    spec &= Q(employeeId__in=employee_ids)
                if has_department_filter:
                    spec &= Q(department_id__in=department_ids)
                company_employees = CompanyEmployee.objects.filter(spec)

            for employee in company_employees:
                dto = self.build_employee_salary_statement(employee, request_dto)
                if dto is not None:
                    salary_statement_list.append(dto)
                    
            return salary_statement_list
        except Exception as e:
            logger.error(f"Error in get_employee_salary_statements: {e}")
            raise Exception(str(e))

    def build_employee_salary_statement(self, company_employee: CompanyEmployee, salary_statement_request_dto: dict) -> dict:
        time_zone = salary_statement_request_dto.get("timeZone")
        if not time_zone:
            time_zone = "Asia/Calcutta"
        tz = pytz.timezone(time_zone)

        start_date_str = salary_statement_request_dto.get("startDate")
        end_date_str = salary_statement_request_dto.get("endDate")

        if start_date_str and end_date_str:
            start_local_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
            end_local_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
        else:
            # Fallback to current month logic
            now = datetime.now(tz)
            start_local_date = now.replace(day=1).date()
            import calendar
            _, last_day = calendar.monthrange(now.year, now.month)
            end_local_date = now.replace(day=last_day).date()

        # Convert to UTC for database querying
        start_datetime_local = tz.localize(datetime.combine(start_local_date, datetime.min.time()))
        start_date_utc = start_datetime_local.astimezone(pytz.UTC)

        end_datetime_local = tz.localize(datetime.combine(end_local_date, datetime.max.time()))
        end_date_utc = end_datetime_local.astimezone(pytz.UTC)

        # Initialize DTO dict
        dto = {
            "employeeId": company_employee.employeeId,
            "companyId": company_employee.companyDetails.id if company_employee.companyDetails else None,
            "employeeName": f"{company_employee.firstName or ''} {company_employee.lastName or ''}".strip(),
        }

        if company_employee.basicSalary is not None:
            dto["basicSalary"] = company_employee.basicSalary

        if company_employee.department:
            dto["departmentId"] = company_employee.department.id
            dto["departmentName"] = company_employee.department.departmentName

        # 2. Fetch Holiday Dates
        holiday_dates = set()
        if company_employee.holidayTemplates:
            try:
                holiday_template = self.holiday_templates_service.get_holiday_template_by_id(company_employee.holidayTemplates.id)
                if holiday_template and holiday_template.get("holidayTemplateDetailsList"):
                    for detail in holiday_template["holidayTemplateDetailsList"]:
                        detail_date = detail.get("date")
                        if detail_date:
                            utc_date = self.common_service.convert_string_to_date(detail_date)
                            if utc_date:
                                local_holiday = utc_date.astimezone(tz).date()
                                holiday_dates.add(local_holiday)
            except Exception as e:
                logger.error(f"Error fetching holiday template details: {e}")

        # 3. Get Paid Day Configuration (All potential Weekly Offs + Holidays in range)
        config_paid_off_days = set()
        if company_employee.weeklyOff or len(holiday_dates) > 0:
            config_paid_off_days = self.calculate_paid_days(
                start_local_date, end_local_date, company_employee.weeklyOff, holiday_dates
            )

        # 4. Get actual attendance data
        user_in_out_list = UserInOut.objects.filter(
            user__employeeId=company_employee.employeeId,
            createdOn__gte=start_date_utc,
            createdOn__lte=end_date_utc,
            isSalaryGenerate=0
        )
        if not user_in_out_list.exists():
            return None

        # 5. Process attendance records
        daily_worked_minutes = {}
        actual_work_days = set()

        total_worked_millis = 0
        penalty_amount = 0
        adjusted_work_minutes_total = 0

        for user_in_out in user_in_out_list:
            dto["clockInOutId"] = user_in_out.id
            time_in = user_in_out.timeIn
            time_out = user_in_out.timeOut

            if time_in and time_out:
                # time_in and time_out are offset-aware in UTC. Convert to local timezone.
                time_in_tz = time_in.astimezone(tz)
                time_out_tz = time_out.astimezone(tz)

                worked_seconds = (time_out_tz - time_in_tz).total_seconds()
                worked_millis = int(worked_seconds * 1000)
                total_worked_millis += worked_millis

                date_val = time_in_tz.date()
                work_minutes = int(worked_seconds // 60)

                lunch_break_minutes = company_employee.lunchBreak if company_employee.lunchBreak is not None else 0
                adjusted_work_minutes = max(0, work_minutes - lunch_break_minutes)
                adjusted_work_minutes_total += adjusted_work_minutes

                daily_worked_minutes[date_val] = daily_worked_minutes.get(date_val, 0) + adjusted_work_minutes
                actual_work_days.add(date_val)

                # Penalty Calculations
                if company_employee.lateEntryPenaltyRule is True and company_employee.companyShift:
                    if company_employee.companyShift.shiftType == "Time Based":
                        penalty_amount += self.calculate_late_entry_penalty(company_employee, time_in, tz)

                if company_employee.earlyExitPenaltyRule is True and company_employee.companyShift:
                    if company_employee.companyShift.shiftType == "Time Based":
                        penalty_amount += self.calculate_early_exit_penalty(company_employee, time_out, tz)

        # --- 6. FIX: Calculate Final Paid Days ---
        # Remove any day the employee actually worked from the paid off-days pool.
        config_paid_off_days.difference_update(actual_work_days)
        total_paid_days_count = len(config_paid_off_days)

        # 7. Overtime & Deductions
        employee_shift_hours = company_employee.companyShift.totalHours if (company_employee.companyShift and company_employee.companyShift.totalHours is not None) else 0.0
        total_worked_minutes = total_worked_millis // (1000 * 60)
        
        lunch_break_minutes = company_employee.lunchBreak if company_employee.lunchBreak is not None else 0
        lunch_deduction = len(actual_work_days) * lunch_break_minutes
        net_worked_minutes = total_worked_minutes - lunch_deduction
        shift_minutes = employee_shift_hours * 60.0
        ot_final_minutes = int(max(net_worked_minutes - shift_minutes, 0))
        
        ot_amount_final = 0
        if company_employee.employeeType and company_employee.employeeType.id != 2:
            ot_amount_final = self.calculate_overtime_amount(company_employee, ot_final_minutes)

        # 8. Earnings
        is_hourly = (
            company_employee.employeeType and 
            company_employee.employeeType.id == 2 and 
            company_employee.hourlyRate is not None
        )

        allowances = self.calculate_total_allowance_and_deductions(company_employee.employeeId, "Allowance")
        total_allowance = sum(item["amount"] for item in allowances)

        deductions = self.calculate_total_allowance_and_deductions(company_employee.employeeId, "Deduction")
        total_deduction_amount = sum(item["amount"] for item in deductions)

        if is_hourly:
            total_minutes = adjusted_work_minutes_total
            hrs = total_minutes // 60
            mins = total_minutes % 60
            worked_hours = hrs + (mins / 100.0)
            hourly_rate = company_employee.hourlyRate
            dto["totalWorkingHours"] = worked_hours
            pay_for_worked = (hrs * hourly_rate) + (mins * hourly_rate / 60.0)
            base_salary = int(round(pay_for_worked))
        else:
            monthly_salary = company_employee.basicSalary if company_employee.basicSalary is not None else 0
            daily_rate = monthly_salary / 30.0

            # Re-calculate paid off-days (weekly offs + holidays) for this period
            paid_off_days = self.calculate_paid_days(
                start_local_date, end_local_date, company_employee.weeklyOff, holiday_dates
            )
            
            paid_day_count = min(len(actual_work_days) + len(paid_off_days), 30)
            base_salary = int(round(daily_rate * paid_day_count))

        other_deductions = self.calculate_canteen_deductions(company_employee, daily_worked_minutes, actual_work_days) + penalty_amount
        total_earnings = base_salary + ot_amount_final + total_allowance

        pt_amount = 0
        if company_employee.isPt is True:
            pt_amount = company_employee.ptAmount if company_employee.ptAmount is not None else 0
        dto["ptAmount"] = pt_amount

        total_deductions = other_deductions + total_deduction_amount + pt_amount

        # Calculate PF & PT
        pf_amount = 0
        if company_employee.isPf is True:
            earnings_for_pf = total_earnings - total_deductions
            if earnings_for_pf >= 15000:
                pf_amount = 1800
            else:
                pf_amount = (earnings_for_pf * 12) // 100

        dto["totalPfAmount"] = pf_amount
        if company_employee.isPf is True:
            if total_earnings - total_deductions >= 15000:
                dto["pfAmount"] = 1800
                dto["pfPercentage"] = None
            else:
                dto["pfAmount"] = None
                dto["pfPercentage"] = 12
        else:
            dto["pfAmount"] = 0
            dto["pfPercentage"] = None

        total_deductions += pf_amount

        # Set DTO values
        dto["totalEarnSalary"] = base_salary
        dto["overTime"] = ot_final_minutes
        dto["otAmount"] = ot_amount_final
        dto["totalPaidDays"] = total_paid_days_count
        dto["totalWorkingDays"] = len(actual_work_days)
        dto["totalDays"] = total_paid_days_count + len(actual_work_days)
        dto["totalAllowance"] = total_allowance
        dto["totalEarnings"] = total_earnings
        dto["deduction"] = total_deduction_amount
        dto["otherDeductions"] = other_deductions
        dto["totalPenaltyAmount"] = penalty_amount
        dto["totalDeductions"] = total_deductions
        dto["netSalary"] = total_earnings - total_deductions
        dto["employeeType"] = company_employee.employeeType.name if company_employee.employeeType else None

        # Calculate absent_count (same logic as in get_all_entries_grouped_by_user)
        absent_count = 0
        curr = start_local_date
        while curr <= end_local_date:
            if curr not in actual_work_days:
                is_holiday = curr in holiday_dates
                is_weekly_off = False
                if not is_holiday and company_employee.weeklyOff:
                    is_weekly_off = self.is_weekly_off_day(curr, company_employee.weeklyOff)
                
                if not is_holiday and not is_weekly_off:
                    absent_count += 1
            curr += timedelta(days=1)

        # Get record by userId from employee_leave_master table
        elm = EmployeeLeaveMaster.objects.filter(companyEmployee_id=company_employee.employeeId).first()
        if elm:
            current_used = elm.usedLeave or 0
            total_leave = elm.totalLeave
            new_used = current_used + absent_count
            if total_leave is not None and new_used > total_leave:
                new_used = total_leave
            dto["used_leave"] = new_used
        else:
            dto["used_leave"] = absent_count

        # Print/Log statements matching Java debugging output
        logger.error(f"============= Debugging Employee Salary Statement for Employee: {company_employee.userName} ================")
        logger.error(f"Basic Salary: {company_employee.basicSalary}")
        logger.error(f"Start Date: {start_date_utc} (Local Date: {start_local_date})")
        logger.error(f"End Date: {end_date_utc} (Local Date: {end_local_date})")
        logger.error(f"Paid Days: {total_paid_days_count}")
        logger.error(f"Worked Days: {len(actual_work_days)}")
        logger.error(f"Total Worked Days: {len(actual_work_days) + total_paid_days_count}")
        logger.error(f"Total Worked Minutes: {total_worked_minutes}")
        logger.error(f"Overtime Minutes: {ot_final_minutes}")
        logger.error(f"Overtime Amount: {ot_amount_final}")
        logger.error(f"Total Earnings: {total_earnings}")
        logger.error(f"PF Amount: {pf_amount}")
        logger.error(f"PT Amount: {pt_amount}")
        logger.error(f"Penalty Amount: {penalty_amount}")
        logger.error(f"Allowance: {total_allowance}")
        logger.error(f"Deductions: {total_deduction_amount}")
        logger.error(f"Other Deductions (Canteen + Penalty): {other_deductions}")
        logger.error(f"Total Deductions: {total_deductions}")
        logger.error(f"Net Salary: {total_earnings - total_deductions}")

        return dto

    def calculate_paid_days(self, start_local_date, end_local_date, config, holiday_dates) -> set:
        paid_days = set()
        curr = start_local_date
        while curr <= end_local_date:
            is_off_day = False
            
            # 1. Check if it's a Holiday
            if holiday_dates and curr in holiday_dates:
                is_off_day = True

            # 2. Check if it's a Weekly Off
            if not is_off_day and config is not None:
                is_off_day = self.is_weekly_off_day(curr, config)

            if is_off_day:
                paid_days.add(curr)
                
            curr += timedelta(days=1)
        return paid_days

    def is_weekly_off_day(self, date_obj, config) -> bool:
        if config is None:
            return False
            
        day_of_week = date_obj.weekday()  # 0 is Monday, ..., 6 is Sunday
        week_of_month = ((date_obj.day - 1) // 7) + 1  # 1 to 5
        
        if day_of_week == 6:  # SUNDAY
            return config.sundayAll or (
                (week_of_month == 1 and config.sunday1st) or
                (week_of_month == 2 and config.sunday2nd) or
                (week_of_month == 3 and config.sunday3rd) or
                (week_of_month == 4 and config.sunday4th) or
                (week_of_month == 5 and config.sunday5th)
            )
        elif day_of_week == 0:  # MONDAY
            return config.mondayAll or (
                (week_of_month == 1 and config.monday1st) or
                (week_of_month == 2 and config.monday2nd) or
                (week_of_month == 3 and config.monday3rd) or
                (week_of_month == 4 and config.monday4th) or
                (week_of_month == 5 and config.monday5th)
            )
        elif day_of_week == 1:  # TUESDAY
            return config.tuesdayAll or (
                (week_of_month == 1 and config.tuesday1st) or
                (week_of_month == 2 and config.tuesday2nd) or
                (week_of_month == 3 and config.tuesday3rd) or
                (week_of_month == 4 and config.tuesday4th) or
                (week_of_month == 5 and config.tuesday5th)
            )
        elif day_of_week == 2:  # WEDNESDAY
            return config.wednesdayAll or (
                (week_of_month == 1 and config.wednesday1st) or
                (week_of_month == 2 and config.wednesday2nd) or
                (week_of_month == 3 and config.wednesday3rd) or
                (week_of_month == 4 and config.wednesday4th) or
                (week_of_month == 5 and config.wednesday5th)
            )
        elif day_of_week == 3:  # THURSDAY
            return config.thursdayAll or (
                (week_of_month == 1 and config.thursday1st) or
                (week_of_month == 2 and config.thursday2nd) or
                (week_of_month == 3 and config.thursday3rd) or
                (week_of_month == 4 and config.thursday4th) or
                (week_of_month == 5 and config.thursday5th)
            )
        elif day_of_week == 4:  # FRIDAY
            return config.fridayAll or (
                (week_of_month == 1 and config.friday1st) or
                (week_of_month == 2 and config.friday2nd) or
                (week_of_month == 3 and config.friday3rd) or
                (week_of_month == 4 and config.friday4th) or
                (week_of_month == 5 and config.friday5th)
            )
        elif day_of_week == 5:  # SATURDAY
            return config.saturdayAll or (
                (week_of_month == 1 and config.saturday1st) or
                (week_of_month == 2 and config.saturday2nd) or
                (week_of_month == 3 and config.saturday3rd) or
                (week_of_month == 4 and config.saturday4th) or
                (week_of_month == 5 and config.saturday5th)
            )
        return False

    def calculate_overtime_amount(self, employee, ot_minutes) -> int:
        if ot_minutes <= 0 or not employee.overtimeRules:
            return 0

        rule = employee.overtimeRules
        ot_pay_per_slab = rule.otAmount if rule.otAmount is not None else 0.0
        daily_salary = 0

        if employee.employeeType and employee.employeeType.id == 2 and employee.hourlyRate is not None:
            shift_hours = employee.companyShift.totalHours if employee.companyShift and employee.companyShift.totalHours is not None else 0.0
            daily_salary = int(shift_hours * employee.hourlyRate)
        else:
            basic = employee.basicSalary if employee.basicSalary is not None else 0
            daily_salary = int(basic // 30)

        ot_type = rule.otType.strip().lower() if rule.otType else ""
        if ot_type == "fixed amount":
            return int(ot_pay_per_slab)
        elif ot_type == "fixed amount per hour":
            ot_hours = int(math.ceil(ot_minutes / 60.0))
            return int(ot_hours * ot_pay_per_slab)
        elif ot_type == "1 day salary":
            return daily_salary
        elif ot_type == "1.5 day salary":
            return int(daily_salary * 1.5)
        elif ot_type == "2 day salary":
            return daily_salary * 2
        elif ot_type == "2.5 day salary":
            return int(daily_salary * 2.5)
        elif ot_type == "3 day salary":
            return daily_salary * 3
        else:
            return 0

    def calculate_canteen_deductions(self, employee, daily_worked_minutes, work_days) -> int:
        canteen_type = employee.canteenType
        canteen_amount = employee.canteenAmount if employee.canteenAmount is not None else 0
        
        if canteen_type == "Office Type":
            return canteen_amount
        elif canteen_type == "Labour Type":
            per_day_amount = canteen_amount
            
            if employee.workingHoursIncludeLunch is None:
                return len(work_days) * per_day_amount * 2
                
            threshold = self.hh_dot_mm_to_minutes(employee.workingHoursIncludeLunch)
            
            heavy_working_days = 0
            for date_val in work_days:
                worked_min = daily_worked_minutes.get(date_val, 0)
                if worked_min > threshold:
                    heavy_working_days += 1
                    
            light_days = len(work_days) - heavy_working_days
            return (light_days * per_day_amount * 2) + (heavy_working_days * per_day_amount)
        else:
            return 0

    def hh_dot_mm_to_minutes(self, value) -> int:
        if value is None:
            return 0
        try:
            val = float(value)
            hours = int(val)
            minutes = int(round((val - hours) * 100))
            if minutes < 0 or minutes > 59:
                raise ValueError(f"Invalid minutes: {minutes}")
            return (hours * 60) + minutes
        except Exception as e:
            logger.error(f"Error in hh_dot_mm_to_minutes for value {value}: {e}")
            return 0

    def calculate_late_entry_penalty(self, employee, time_in_date, tz) -> int:
        if not employee.companyShift or not employee.companyShift.startTime:
            return 0
        
        basic = employee.basicSalary
        if not basic or basic <= 0:
            return 0
        
        day_salary = basic // 30
        total_hours = employee.companyShift.totalHours if employee.companyShift.totalHours is not None else 0.0

        actual_in = time_in_date.astimezone(tz)
        
        raw_start_str = employee.companyShift.startTime
        if isinstance(raw_start_str, (datetime, time)):
            if isinstance(raw_start_str, datetime):
                raw_start = raw_start_str.time()
            else:
                raw_start = raw_start_str
        elif isinstance(raw_start_str, str):
            try:
                if len(raw_start_str.split(":")) == 3:
                    raw_start = datetime.strptime(raw_start_str.strip(), "%H:%M:%S").time()
                else:
                    raw_start = datetime.strptime(raw_start_str.strip(), "%H:%M").time()
            except Exception as e:
                logger.error(f"Error parsing raw shift start time: {raw_start_str}, error: {e}")
                raw_start = time(0, 0, 0)
        else:
            raw_start = time(0, 0, 0)

        if raw_start == time(0, 0, 0) and actual_in.hour >= 12:
            raw_start = time(12, 0, 0)

        expected_start = tz.localize(datetime.combine(actual_in.date(), raw_start))
        late_minutes = int((actual_in - expected_start).total_seconds() // 60)
        
        if late_minutes <= 0:
            return 0
            
        return self.pick_and_apply_rule(employee, day_salary, total_hours, late_minutes, False)

    def calculate_early_exit_penalty(self, employee, time_out_date, tz) -> int:
        if not employee.companyShift or not employee.companyShift.endTime:
            return 0
            
        basic = employee.basicSalary
        if not basic or basic <= 0:
            return 0
            
        day_salary = basic // 30
        total_hours = employee.companyShift.totalHours if employee.companyShift.totalHours is not None else 0.0

        actual_out = time_out_date.astimezone(tz)
        
        raw_end_str = employee.companyShift.endTime
        if isinstance(raw_end_str, (datetime, time)):
            if isinstance(raw_end_str, datetime):
                raw_end = raw_end_str.time()
            else:
                raw_end = raw_end_str
        elif isinstance(raw_end_str, str):
            try:
                if len(raw_end_str.split(":")) == 3:
                    raw_end = datetime.strptime(raw_end_str.strip(), "%H:%M:%S").time()
                else:
                    raw_end = datetime.strptime(raw_end_str.strip(), "%H:%M").time()
            except Exception as e:
                logger.error(f"Error parsing raw shift end time: {raw_end_str}, error: {e}")
                raw_end = time(0, 0, 0)
        else:
            raw_end = time(0, 0, 0)

        if raw_end == time(0, 0, 0) and actual_out.hour <= 12:
            raw_end = time(12, 0, 0)

        expected_end = tz.localize(datetime.combine(actual_out.date(), raw_end))
        early_minutes = int((expected_end - actual_out).total_seconds() // 60)
        
        if early_minutes <= 0:
            return 0
            
        return self.pick_and_apply_rule(employee, day_salary, total_hours, early_minutes, True)

    def pick_and_apply_rule(self, employee, day_salary, total_hours, diff_minutes, type_val) -> int:
        rules = list(AttendancePenaltyRules.objects.filter(
            companyDetails_id=employee.companyDetails.id,
            isEarlyExit=type_val
        ))
        if not rules:
            return 0

        rules.sort(key=lambda r: r.minutes if r.minutes is not None else 0)

        chosen_rule = None
        for r in rules:
            rule_min = r.minutes if r.minutes is not None else 0
            if diff_minutes >= rule_min:
                chosen_rule = r
            elif chosen_rule is None:
                chosen_rule = r

        if not chosen_rule:
            return 0

        return self.compute_penalty(chosen_rule, day_salary, total_hours)

    def compute_penalty(self, rule, day_salary, total_hours) -> int:
        if not total_hours or total_hours <= 0:
            total_hours = 8.0

        per_hour_salary = day_salary / total_hours
        per_hour_salary = float(Decimal(str(per_hour_salary)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        per_minute_salary = per_hour_salary / 60.0
        per_minute_salary = float(Decimal(str(per_minute_salary)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        deduction_type = rule.deductionType
        if not deduction_type:
            return 0

        deduction_type = deduction_type.strip()

        if deduction_type == "Fixed Amount":
            return rule.amount if rule.amount is not None else 0
        elif deduction_type == "5 Min Salary":
            return int(round(per_minute_salary * 5))
        elif deduction_type == "15 Min Salary":
            return int(round(per_minute_salary * 15))
        elif deduction_type == "30 Min Salary":
            return int(round(per_minute_salary * 30))
        elif deduction_type == "1 Hour Salary":
            return int(round(per_hour_salary))
        elif deduction_type == "Half Day Salary":
            return int(day_salary // 2)
        elif deduction_type == "1 Day Salary":
            return int(day_salary)
        elif deduction_type == "1.5 Day Salary":
            return int(round(day_salary * 1.5))
        elif deduction_type == "2 Day Salary":
            return int(day_salary * 2)
        elif deduction_type == "2.5 Day Salary":
            return int(round(day_salary * 2.5))
        elif deduction_type == "3 Day Salary":
            return int(day_salary * 3)
        else:
            return 0

    def calculate_total_allowance_and_deductions(self, user_id: int, type_str: str) -> list:
        deductions_list = Deductions.objects.filter(companyEmployee__employeeId=user_id, type=type_str)
        res = []
        for d in deductions_list:
            res.append({
                "label": d.label,
                "amount": d.amount if d.amount is not None else 0,
                "type": d.type
            })
        return res
