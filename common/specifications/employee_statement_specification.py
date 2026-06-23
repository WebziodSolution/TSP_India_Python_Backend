from django.db.models import Q

class EmployeeStatementSpecification:
    @staticmethod
    def match_created_on(date):
        return Q(createdOn=date)

    @staticmethod
    def between_created_on(start_date, end_date):
        return Q(createdOn__range=(start_date, end_date))

    @staticmethod
    def created_on_greater_than_equal(start_date):
        return Q(createdOn__gte=start_date)

    @staticmethod
    def created_on_less_than_equal(end_date):
        return Q(createdOn__lte=end_date)

    @staticmethod
    def has_user_ids(user_ids):
        # Filters UserInOut.user (which is a ForeignKey to CompanyEmployee)
        return Q(user__employeeId__in=user_ids)

    @staticmethod
    def has_department_ids(department_ids):
        # Filters CompanyEmployee.department
        return Q(department__id__in=department_ids)

    @staticmethod
    def has_employee_ids(employee_ids):
        # Filters CompanyEmployee.employeeId
        return Q(employeeId__in=employee_ids)

    @staticmethod
    def has_company_id(company_id):
        # Filters CompanyEmployee.companyDetails
        return Q(companyDetails__id=company_id)
