import logging
from common.models import CompanyActions
from common.serializers import CompanyActionsSerializer

logger = logging.getLogger(__name__)

class CompanyRoleActionService:
    def get_company_actions(self) -> list:
        try:
            company_actions = CompanyActions.objects.all()
            company_actions_dtos = []
            for action in company_actions:
                company_actions_dtos.append(self.get_actions(action.actionId))
            return company_actions_dtos
        except Exception as e:
            logger.error(f"Error get_company_actions: {e}")
            raise Exception(str(e))

    def get_actions(self, action_id: int) -> dict:
        try:
            action = CompanyActions.objects.filter(actionId=action_id).first()
            if not action:
                raise Exception("Action not found")
            return CompanyActionsSerializer(action).data
        except Exception as e:
            logger.error(f"Error get_actions: {e}")
            raise Exception(str(e))

    def create_actions(self, company_actions_dto: dict) -> dict:
        try:
            serializer = CompanyActionsSerializer(data=company_actions_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            action = CompanyActions(
                actionName=validated_data.get("actionName") or ""
            )
            action.save()
            
            return CompanyActionsSerializer(action).data
        except Exception as e:
            logger.error(f"Error create_actions: {e}")
            raise Exception(str(e))

    def update_actions(self, action_id: int, company_actions_dto: dict) -> dict:
        try:
            action = CompanyActions.objects.filter(actionId=action_id).first()
            if not action:
                raise Exception("Action not found")
                
            serializer = CompanyActionsSerializer(data=company_actions_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            action.actionName = validated_data.get("actionName") or ""
            action.save()
            
            return CompanyActionsSerializer(action).data
        except Exception as e:
            logger.error(f"Error update_actions: {e}")
            raise Exception(str(e))

    def delete_actions(self, action_id: int) -> None:
        try:
            action = CompanyActions.objects.filter(actionId=action_id).first()
            if not action:
                raise Exception("Action not found")
            action.delete()
        except Exception as e:
            logger.error(f"Error delete_actions: {e}")
            raise Exception(str(e))
