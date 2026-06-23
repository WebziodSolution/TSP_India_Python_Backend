import logging
from common.models import Country
from common.serializers import CountrySerializer

logger = logging.getLogger(__name__)

class CountryService:
    def get_country(self, id: int) -> dict:
        try:
            country = Country.objects.filter(id=id).first()
            if not country:
                raise Exception("Country not found")
            return CountrySerializer(country).data
        except Exception as e:
            logger.error(f"Error in get_country: {e}")
            raise Exception(str(e))

    def get_all_country(self) -> list:
        try:
            countries = Country.objects.all().order_by('id')
            country_dto_list = []
            for c in countries:
                country_dto_list.append(self.get_country(c.id))
            return country_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_country: {e}")
            raise Exception(str(e))
