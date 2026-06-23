import logging
from django.db.models import Q
from django.core.paginator import Paginator
from common.models import CompanyDetails, CompanyEmployee
from common.service import CommonService
from common.specifications import CompanySpecification

logger = logging.getLogger(__name__)

class CompanyReportService:
    def __init__(self):
        self.common_service = CommonService()

    def getCompanies(self, start_date_str: str, end_date_str: str, min_val: int, max_val: int, page: int, size: int, time_zone: str) -> dict:
        try:
            queryset = CompanyDetails.objects.all()
            
            # Filter dates
            spec = Q()
            if start_date_str and time_zone:
                start_date = self.common_service.convert_local_to_utc(start_date_str, time_zone, False)
                spec &= Q(registerDate__gte=start_date)
            if end_date_str and time_zone:
                end_date = self.common_service.convert_local_to_utc(end_date_str, time_zone, False)
                spec &= Q(registerDate__lte=end_date)
                
            # Filter employee count
            queryset = CompanySpecification.apply_employee_count_annotation(queryset)
            if min_val is not None and max_val is not None:
                spec &= Q(employee_count__gte=min_val, employee_count__lte=max_val)
            elif min_val is not None:
                spec &= Q(employee_count__gte=min_val)
            elif max_val is not None:
                spec &= Q(employee_count__lte=max_val)
                
            queryset = queryset.filter(spec).order_by('-registerDate')
            
            paginator = Paginator(queryset, size if size > 0 else 10)
            django_page_num = page + 1
            
            try:
                page_obj = paginator.page(django_page_num)
            except Exception:
                page_obj = paginator.page(1)
                
            content = []
            for company in page_obj.object_list:
                employee_count = CompanyEmployee.objects.filter(companyDetails=company).count()
                
                formatted_date = None
                if time_zone and company.registerDate:
                    date_string = company.registerDate.strftime("%m/%d/%Y, %I:%M:%S %p").upper()
                    formatted_date = self.common_service.convert_utc_to_local(date_string, time_zone)
                    
                content.append({
                    "id": company.id,
                    "companyName": company.companyName,
                    "email": company.email,
                    "phone": company.phone,
                    "registerDate": formatted_date,
                    "employeeCount": employee_count
                })
                
            total_pages = paginator.num_pages
            current_page = page_obj.number - 1
            next_page = current_page + 1 if page_obj.has_next() else current_page
            number_of_elements = len(content)
            is_last = not page_obj.has_next()
            
            return {
                "content": content,
                "totalPages": total_pages,
                "currentPage": current_page,
                "nextPage": next_page,
                "numberOfElements": number_of_elements,
                "last": is_last,
                "sortDirection": "DESC"
            }
        except Exception as e:
            logger.error(f"Error getCompanies: {e}")
            raise Exception(str(e))
