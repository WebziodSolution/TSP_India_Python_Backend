import logging
from django.core.paginator import Paginator
from common.models import CompanyModules, CompanyFunctionality, CompanyActions, CompanyModuleActions
from common.serializers import CompanyModuleSerializer, AssignCompanyActionsToCompanyModuleSerializer

logger = logging.getLogger(__name__)

class CompanyModuleService:
    def create_module(self, module_dto: dict) -> dict:
        try:
            functionality_id = module_dto.get("functionalityId")
            functionality = CompanyFunctionality.objects.filter(id=functionality_id).first()
            if not functionality:
                raise Exception("Functionality not found.")
                
            module = CompanyModules(
                moduleName=module_dto.get("moduleName") or "",
                functionality=functionality
            )
            module.save()
            
            # assign policies
            action_ids = module_dto.get("actions", [])
            self.assign_policies({
                "moduleId": module.moduleId,
                "actionIds": action_ids
            })
            
            return {
                "moduleId": module.moduleId,
                "moduleName": module.moduleName,
                "functionalityId": functionality.id,
                "functionalityName": functionality.functionalityName,
                "actions": action_ids
            }
        except Exception as e:
            logger.error(f"Error create_module: {e}")
            raise Exception(str(e))

    def paginate_modules(self, queryset, page: int, size: int) -> dict:
        paginator = Paginator(queryset, size if size > 0 else 10)
        django_page_num = page + 1  # Django pages are 1-indexed, Java's are 0-indexed
        
        try:
            page_obj = paginator.page(django_page_num)
        except Exception:
            # Fallback if page out of range
            page_obj = paginator.page(1)
            
        module_dtos = []
        for module in page_obj.object_list:
            module_dtos.append({
                "moduleId": module.moduleId,
                "moduleName": module.moduleName,
                "functionalityId": module.functionality.id if module.functionality else None,
                "functionalityName": module.functionality.functionalityName if module.functionality else "",
                "actions": self.get_module_policy(module.moduleId)
            })
            
        return {
            "getTotalPages": paginator.num_pages,
            "getNumber": page_obj.number - 1,
            "getSize": paginator.per_page,
            "getTotalRecords": paginator.count,
            "modulesList": module_dtos
        }

    def all_module_list_page(self, search_key: str, page: int, size: int) -> dict:
        try:
            if search_key:
                queryset = CompanyModules.objects.filter(moduleName__icontains=search_key).order_by('moduleId')
            else:
                queryset = CompanyModules.objects.all().order_by('moduleId')
            return self.paginate_modules(queryset, page, size)
        except Exception as e:
            logger.error(f"Error all_module_list_page: {e}")
            raise Exception(str(e))

    def module_by_functionality_list_page(self, functionality_id: int, search_key: str, page: int, size: int) -> dict:
        try:
            queryset = CompanyModules.objects.filter(functionality_id=functionality_id)
            if search_key:
                queryset = queryset.filter(moduleName__icontains=search_key)
            queryset = queryset.order_by('moduleId')
            return self.paginate_modules(queryset, page, size)
        except Exception as e:
            logger.error(f"Error module_by_functionality_list_page: {e}")
            raise Exception(str(e))

    def get_all_modules(self) -> dict:
        try:
            modules = CompanyModules.objects.all().order_by('moduleId')
            module_dtos = []
            for module in modules:
                module_dtos.append({
                    "moduleId": module.moduleId,
                    "moduleName": module.moduleName,
                    "functionalityId": module.functionality.id if module.functionality else None,
                    "functionalityName": module.functionality.functionalityName if module.functionality else "",
                    "actions": self.get_module_policy(module.moduleId)
                })
            return {"modulesList": module_dtos}
        except Exception as e:
            logger.error(f"Error get_all_modules: {e}")
            raise Exception(str(e))

    def get_module_by_id(self, module_id: int) -> dict:
        try:
            module = CompanyModules.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Module not found")
                
            return {
                "moduleId": module.moduleId,
                "moduleName": module.moduleName,
                "functionalityId": module.functionality.id if module.functionality else None,
                "functionalityName": module.functionality.functionalityName if module.functionality else "",
                "actions": self.get_module_policy(module.moduleId)
            }
        except Exception as e:
            logger.error(f"Error get_module_by_id: {e}")
            raise Exception(str(e))

    def update_module_by_id(self, module_id: int, module_dto: dict) -> dict:
        try:
            module = CompanyModules.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Such Module Doesn't Exist")
                
            functionality_id = module_dto.get("functionalityId")
            functionality = CompanyFunctionality.objects.filter(id=functionality_id).first()
            if not functionality:
                raise Exception("Functionality not found.")
                
            module.moduleName = module_dto.get("moduleName") or ""
            module.functionality = functionality
            module.save()
            
            action_ids = module_dto.get("actions", [])
            self.assign_policies({
                "moduleId": module.moduleId,
                "actionIds": action_ids
            })
            
            return {
                "moduleId": module.moduleId,
                "moduleName": module.moduleName,
                "functionalityId": functionality.id,
                "functionalityName": functionality.functionalityName,
                "actions": action_ids
            }
        except Exception as e:
            logger.error(f"Error update_module_by_id: {e}")
            raise e

    def assign_policies(self, assign_dto: dict) -> None:
        try:
            module_id = assign_dto.get("moduleId")
            module = CompanyModules.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Module not found")
                
            # Delete old mappings
            CompanyModuleActions.objects.filter(module=module).delete()
            
            action_ids = assign_dto.get("actionIds", [])
            for action_id in action_ids:
                action = CompanyActions.objects.filter(actionId=action_id).first()
                if action:
                    CompanyModuleActions.objects.create(
                        module=module,
                        action=action
                    )
        except Exception as e:
            logger.error(f"Error assign_policies: {e}")
            raise Exception(str(e))

    def delete_module_by_id(self, module_id: int) -> None:
        try:
            module = CompanyModules.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Module not found")
            module.delete()
        except Exception as e:
            logger.error(f"Error delete_module_by_id: {e}")
            raise Exception(str(e))

    def get_module_policy(self, module_id: int) -> list:
        try:
            policies = CompanyModuleActions.objects.filter(module_id=module_id).order_by('action_id')
            return [p.action.actionId for p in policies if p.action]
        except Exception as e:
            logger.error(f"Error get_module_policy: {e}")
            raise Exception(str(e))
