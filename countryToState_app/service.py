import logging
from common.models import CountryToState
from common.serializers import CountryToStateSerializer

logger = logging.getLogger(__name__)

class CountryToStateService:
    def get_state_by_id(self, id: int) -> dict:
        try:
            state = CountryToState.objects.filter(id=id).first()
            if not state:
                raise Exception("State not found")
            dto = {
                "id": state.id,
                "countryId": state.country.id if state.country else None,
                "stateLong": state.stateLong,
                "stateShort": state.stateShort,
                "stateCapital": state.stateCapital
            }
            return CountryToStateSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_state_by_id: {e}")
            raise Exception(str(e))

    def get_all_state(self) -> list:
        try:
            states = CountryToState.objects.all().order_by('id')
            state_dto_list = []
            for s in states:
                state_dto_list.append(self.get_state_by_id(s.id))
            return state_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_state: {e}")
            raise Exception(str(e))

    def get_all_state_by_country(self, country_id: int) -> list:
        try:
            states = CountryToState.objects.filter(country_id=country_id).order_by('id')
            state_dto_list = []
            for s in states:
                state_dto_list.append(self.get_state_by_id(s.id))
            return state_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_state_by_country: {e}")
            raise Exception(str(e))
