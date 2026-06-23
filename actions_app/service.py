import logging
from common.models import Actions

logger = logging.getLogger(__name__)

class ActionService:
    def getAllActions(self) -> list:
        try:
            actions = Actions.objects.all().order_by('actionId')
            action_dtos = []
            for action in actions:
                action_dtos.append({
                    "actionId": action.actionId,
                    "actionName": action.actionName
                })
            return action_dtos
        except Exception as e:
            logger.error(f"Error getAllActions: {e}")
            raise Exception(str(e))
