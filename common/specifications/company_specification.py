from django.db.models import Q

class CompanySpecification:
    @staticmethod
    def search_by_name(name: str):
        return Q(companyName__icontains=name)

    @staticmethod
    def register_date_greater_than_equal(date):
        return Q(registerDate__gte=date)

    @staticmethod
    def register_date_less_than_equal(date):
        return Q(registerDate__lte=date)

    @staticmethod
    def is_active(active: bool):
        return Q(isActive=1 if active else 0)

    @staticmethod
    def employee_count_between(min_val: int, max_val: int):
        return Q(employee_count__gte=min_val, employee_count__lte=max_val)

    @staticmethod
    def employee_count_greater_than(min_val: int):
        return Q(employee_count__gte=min_val)

    @staticmethod
    def employee_count_less_than(max_val: int):
        return Q(employee_count__lte=max_val)

    @staticmethod
    def apply_employee_count_annotation(queryset):
        from django.db.models import OuterRef, Subquery, IntegerField, Count
        from django.db.models.functions import Coalesce
        from common.models import CompanyEmployee
        
        employee_count_subquery = Coalesce(
            Subquery(
                CompanyEmployee.objects.filter(companyDetails=OuterRef('pk'))
                .values('companyDetails')
                .annotate(cnt=Count('employeeId'))
                .values('cnt')
            ),
            0,
            output_field=IntegerField()
        )
        return queryset.annotate(employee_count=employee_count_subquery)
