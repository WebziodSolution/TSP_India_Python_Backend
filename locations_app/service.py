import logging
from datetime import datetime
from common.models import Locations, CompanyDetails
from common.service import CommonService

logger = logging.getLogger(__name__)

class LocationService:
    def __init__(self):
        self.common_service = CommonService()

    def _convert_model_to_dto(self, loc: Locations) -> dict:
        pay_period_start_str = None
        pay_period_end_str = None

        if loc.payPeriodStart:
            dt_start = datetime.combine(loc.payPeriodStart, datetime.min.time())
            pay_period_start_str = self.common_service.convert_date_to_string(dt_start)
            
        if loc.payPeriodEnd:
            dt_end = datetime.combine(loc.payPeriodEnd, datetime.min.time())
            pay_period_end_str = self.common_service.convert_date_to_string(dt_end)

        return {
            "id": loc.id,
            "locationName": loc.locationName,
            "city": loc.city,
            "state": loc.state,
            "country": loc.country,
            "address1": loc.address1,
            "address2": loc.address2,
            "employeeCount": loc.employeeCount,
            "zipCode": loc.zipCode,
            "companyId": loc.companyDetails.id if loc.companyDetails else None,
            "externalId": loc.externalId,
            "geofenceId": loc.geofenceId,
            "isActive": loc.isActive,
            "payPeriod": loc.payPeriod,
            "payPeriodStart": pay_period_start_str,
            "payPeriodEnd": pay_period_end_str
        }

    def get_company_active_locations(self, company_id: int) -> list:
        try:
            locations_list = Locations.objects.filter(companyDetails_id=company_id, isActive=1)
            return [self.get_location(loc.id) for loc in locations_list]
        except Exception as e:
            logger.error(f"Error get_company_active_locations: {e}")
            raise Exception("Error :" + str(e))

    def get_all_location_by_company(self, company_id: int) -> list:
        try:
            locations_list = Locations.objects.filter(companyDetails_id=company_id)
            return [self.get_location(loc.id) for loc in locations_list]
        except Exception as e:
            logger.error(f"Error get_all_location_by_company: {e}")
            raise Exception("Error :" + str(e))

    def get_all_location(self) -> list:
        try:
            locations_list = Locations.objects.all()
            return [self.get_location(loc.id) for loc in locations_list]
        except Exception as e:
            logger.error(f"Error get_all_location: {e}")
            raise Exception("Error :" + str(e))

    def get_locations(self, ids: list) -> list:
        try:
            locations_list = Locations.objects.filter(id__in=ids)
            if not locations_list.exists():
                raise Exception("No locations found for given IDs")
                
            dtos = []
            for loc in locations_list:
                dto = {
                    "id": loc.id,
                    "locationName": loc.locationName,
                    "city": loc.city,
                    "state": loc.state,
                    "country": loc.country,
                    "address1": loc.address1,
                    "address2": loc.address2,
                    "employeeCount": loc.employeeCount,
                    "zipCode": loc.zipCode,
                    "companyId": loc.companyDetails.id if loc.companyDetails else None,
                    "externalId": loc.externalId,
                    "geofenceId": loc.geofenceId,
                    "isActive": loc.isActive,
                    "payPeriod": loc.payPeriod,
                    "payPeriodStart": loc.payPeriodStart.strftime("%Y-%m-%d") if loc.payPeriodStart else None,
                    "payPeriodEnd": loc.payPeriodEnd.strftime("%Y-%m-%d") if loc.payPeriodEnd else None
                }
                dtos.append(dto)
            return dtos
        except Exception as e:
            logger.error(f"Error get_locations: {e}")
            raise Exception("Error: " + str(e))

    def get_location(self, id: int) -> dict:
        try:
            loc = Locations.objects.filter(id=id).first()
            if not loc:
                raise Exception("Location not found")
            return self._convert_model_to_dto(loc)
        except Exception as e:
            logger.error(f"Error get_location: {e}")
            raise Exception("Error :" + str(e))

    def _is_not_empty(self, val) -> bool:
        return val is not None and str(val).strip() != ""

    def create_location(self, dto: dict) -> dict:
        try:
            company_id = dto.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            loc = Locations()
            loc.companyDetails = company
            loc.locationName = dto.get("locationName")
            loc.city = dto.get("city")
            loc.state = dto.get("state")
            loc.country = dto.get("country")
            loc.address1 = dto.get("address1")
            loc.address2 = dto.get("address2",None)
            loc.employeeCount = dto.get("employeeCount")
            loc.zipCode = dto.get("zipCode")
            loc.externalId = dto.get("externalId")
            loc.geofenceId = dto.get("geofenceId")
            loc.payPeriod = dto.get("payPeriod")

            if dto.get("payPeriodStart"):
                loc.payPeriodStart = self.common_service.convert_string_to_date(dto.get("payPeriodStart"))
            if dto.get("payPeriodEnd"):
                loc.payPeriodEnd = self.common_service.convert_string_to_date(dto.get("payPeriodEnd"))

            if (
                self._is_not_empty(dto.get("locationName")) and
                self._is_not_empty(dto.get("city")) and
                self._is_not_empty(dto.get("country")) and
                self._is_not_empty(dto.get("state")) and
                self._is_not_empty(dto.get("address1")) and
                self._is_not_empty(dto.get("zipCode")) and
                self._is_not_empty(dto.get("geofenceId")) and
                self._is_not_empty(dto.get("externalId"))
            ):
                loc.isActive = 1
            else:
                loc.isActive = 0

            loc.save()
            return dto
        except Exception as e:
            logger.error(f"Error create_location: {e}")
            raise Exception(str(e))

    def update_location(self, id: int, dto: dict) -> dict:
        try:
            loc = Locations.objects.filter(id=id).first()
            if not loc:
                raise Exception("Location not found")

            company_id = dto.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            loc.companyDetails = company
            loc.city = dto.get("city")
            loc.state = dto.get("state")
            loc.country = dto.get("country")
            loc.address1 = dto.get("address1")
            loc.address2 = dto.get("address2")
            loc.employeeCount = dto.get("employeeCount")
            loc.zipCode = dto.get("zipCode")
            loc.locationName = dto.get("locationName")
            loc.geofenceId = dto.get("geofenceId")
            loc.externalId = dto.get("externalId")
            loc.payPeriod = dto.get("payPeriod")

            if dto.get("payPeriodStart"):
                loc.payPeriodStart = self.common_service.convert_string_to_date(dto.get("payPeriodStart"))
            else:
                loc.payPeriodStart = None
            if dto.get("payPeriodEnd"):
                loc.payPeriodEnd = self.common_service.convert_string_to_date(dto.get("payPeriodEnd"))
            else:
                loc.payPeriodEnd = None

            if (
                self._is_not_empty(dto.get("locationName")) and
                self._is_not_empty(dto.get("city")) and
                self._is_not_empty(dto.get("country")) and
                self._is_not_empty(dto.get("state")) and
                self._is_not_empty(dto.get("address1")) and
                self._is_not_empty(dto.get("zipCode")) and
                self._is_not_empty(dto.get("geofenceId")) and
                self._is_not_empty(dto.get("externalId"))
            ):
                loc.isActive = 1
            else:
                loc.isActive = 0

            loc.save()
            return dto
        except Exception as e:
            logger.error(f"Error update_location: {e}")
            raise Exception(str(e))

    def delete_location(self, id: int) -> None:
        try:
            loc = Locations.objects.filter(id=id).first()
            if not loc:
                raise Exception("Location not found")
            loc.delete()
        except Exception as e:
            logger.error(f"Error delete_location: {e}")
            raise Exception("Error :" + str(e))
