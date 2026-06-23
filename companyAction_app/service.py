import logging
from common.models import CompanyActions
from common.serializers import CompanyActionsSerializer

logger = logging.getLogger(__name__)

class CompanyActionService:
    def get_all_actions(self) -> list:
        try:
            actions = CompanyActions.objects.all()
            return CompanyActionsSerializer(actions, many=True).data
        except Exception as e:
            logger.error(f"Error get_all_actions: {e}")
            raise Exception(str(e))
