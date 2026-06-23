from django.db.models import Q

class SalaryStatementHistorySpecification:
    @staticmethod
    def has_user_ids(user_ids):
        return Q(employeeId__in=user_ids)

    @staticmethod
    def has_department_ids(department_ids):
        return Q(departmentId__in=department_ids)

    @staticmethod
    def has_month(month):
        return Q(monthYear__in=month)

    @staticmethod
    def has_company(company_id):
        return Q(companyDetails__id=company_id)
