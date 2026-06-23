from django.db.models import Q

class UserInOutSpecification:
    @staticmethod
    def created_on_greater_than_equal(start_date):
        return Q(createdOn__gte=start_date)

    @staticmethod
    def created_on_less_than_equal(end_date):
        return Q(createdOn__lte=end_date)

    @staticmethod
    def has_user_id(user_id):
        return Q(user__employeeId=user_id)

    @staticmethod
    def user_id_in(user_ids):
        return Q(user__employeeId__in=user_ids)

    @staticmethod
    def has_location_id(location_ids):
        return Q(locations__id__in=location_ids)

    @staticmethod
    def has_department_ids(department_ids):
        return Q(user__department__id__in=department_ids)

    @staticmethod
    def has_company(company_id):
        return Q(companyDetails__id=company_id)

    @staticmethod
    def is_salary_generate():
        return Q(isSalaryGenerate=0)
