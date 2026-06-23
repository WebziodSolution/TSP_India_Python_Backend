import logging
from common.models import CompanyTheme, CompanyDetails
from common.serializers import CompanyThemeSerializer

logger = logging.getLogger(__name__)

class CompanyThemeService:
    def get_theme(self, id: int) -> dict:
        try:
            theme = CompanyTheme.objects.filter(id=id).first()
            if not theme:
                raise Exception("Theme not found")
            dto = {
                "id": theme.id,
                "companyId": theme.companyDetails.id if theme.companyDetails else None,
                "primaryColor": theme.primaryColor,
                "sideNavigationBgColor": theme.sideNavigationBgColor,
                "contentBgColor": theme.contentBgColor,
                "contentBgColor2": theme.contentBgColor2,
                "headerBgColor": theme.headerBgColor,
                "textColor": theme.textColor,
                "iconColor": theme.iconColor
            }
            return CompanyThemeSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_theme: {e}")
            raise Exception(str(e))

    def get_all_theme(self, company_id: int) -> dict:
        try:
            theme = CompanyTheme.objects.filter(companyDetails_id=company_id).first()
            if not theme:
                raise Exception("Theme not found")
            return self.get_theme(theme.id)
        except Exception as e:
            logger.error(f"Error in get_all_theme: {e}")
            raise Exception(str(e))

    def create_theme(self, company_theme_dto: dict) -> dict:
        try:
            serializer = CompanyThemeSerializer(data=company_theme_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
                
            theme = CompanyTheme(
                companyDetails=company_details,
                primaryColor=validated_data.get("primaryColor"),
                sideNavigationBgColor=validated_data.get("sideNavigationBgColor"),
                contentBgColor=validated_data.get("contentBgColor"),
                contentBgColor2=validated_data.get("contentBgColor2"),
                headerBgColor=validated_data.get("headerBgColor"),
                textColor=validated_data.get("textColor"),
                iconColor=validated_data.get("iconColor")
            )
            theme.save()
            return self.get_theme(theme.id)
        except Exception as e:
            logger.error(f"Error in create_theme: {e}")
            raise Exception(str(e))

    def update_theme(self, id: int, company_theme_dto: dict) -> dict:
        try:
            serializer = CompanyThemeSerializer(data=company_theme_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            
            theme = CompanyTheme.objects.filter(companyDetails_id=company_id).first()
            if not theme:
                return None
                
            theme_type = validated_data.get("type")
            if theme_type == "setColor":
                theme.primaryColor = validated_data.get("primaryColor")
            elif theme_type == "setSideNavigationBgColor":
                theme.sideNavigationBgColor = validated_data.get("sideNavigationBgColor")
            elif theme_type == "setHeaderBgColor":
                theme.headerBgColor = validated_data.get("headerBgColor")
            elif theme_type == "setContentBgColor":
                theme.contentBgColor = validated_data.get("contentBgColor")
            elif theme_type == "setIconColor":
                theme.iconColor = validated_data.get("iconColor")
            elif theme_type == "setTextColor":
                theme.textColor = validated_data.get("textColor")
            else:
                theme.primaryColor = validated_data.get("primaryColor")
                theme.sideNavigationBgColor = validated_data.get("sideNavigationBgColor")
                theme.contentBgColor = validated_data.get("contentBgColor")
                theme.contentBgColor2 = validated_data.get("contentBgColor2")
                theme.headerBgColor = validated_data.get("headerBgColor")
                theme.textColor = validated_data.get("textColor")
                theme.iconColor = validated_data.get("iconColor")
                
            theme.save()
            return self.get_theme(theme.id)
        except Exception as e:
            logger.error(f"Error in update_theme: {e}")
            raise Exception(str(e))

    def delete_theme(self, id: int) -> None:
        try:
            theme = CompanyTheme.objects.filter(id=id).first()
            if not theme:
                raise Exception("Theme not found")
            theme.delete()
        except Exception as e:
            logger.error(f"Error in delete_theme: {e}")
            raise Exception(str(e))
