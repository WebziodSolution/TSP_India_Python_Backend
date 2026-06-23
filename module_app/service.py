import logging
from django.core.paginator import Paginator
from common.models import Module, Functionality, Actions, ModuleActions

logger = logging.getLogger(__name__)

class ModuleService:

    def get_module_policy(self, module_id: int) -> list:
        try:
            policies = ModuleActions.objects.filter(module_id=module_id).order_by('action_id')
            return [p.action.actionId for p in policies if p.action]
        except Exception as e:
            logger.error(f"Error get_module_policy: {e}")
            raise Exception(str(e))

    def createModule(self, dto: dict) -> dict:
        try:
            func_id = dto.get("functionalityId")
            functionality = Functionality.objects.filter(id=func_id).first()
            if not functionality:
                raise Exception("Functionality not found.")

            module = Module(
                moduleName=dto.get("moduleName"),
                functionality=functionality
            )
            module.save()

            action_ids = dto.get("actions", [])
            self.assignPolicies({
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
            logger.error(f"Error createModule: {e}")
            raise Exception(str(e))

    def paginate_modules(self, queryset, page: int, size: int) -> dict:
        paginator = Paginator(queryset, size if size > 0 else 10)
        django_page_num = page + 1
        
        try:
            page_obj = paginator.page(django_page_num)
        except Exception:
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

    def allModuleListPage(self, search_key: str, page: int, size: int) -> dict:
        try:
            if search_key:
                queryset = Module.objects.filter(moduleName__icontains=search_key).order_by('moduleId')
            else:
                queryset = Module.objects.all().order_by('moduleId')
            return self.paginate_modules(queryset, page, size)
        except Exception as e:
            logger.error(f"Error allModuleListPage: {e}")
            raise Exception(str(e))

    def moduleByFunctionalityListPage(self, functionality_id: int, search_key: str, page: int, size: int) -> dict:
        try:
            queryset = Module.objects.filter(functionality_id=functionality_id)
            if search_key:
                queryset = queryset.filter(moduleName__icontains=search_key)
            queryset = queryset.order_by('moduleId')
            return self.paginate_modules(queryset, page, size)
        except Exception as e:
            logger.error(f"Error moduleByFunctionalityListPage: {e}")
            raise Exception(str(e))

    def getAllModules(self) -> dict:
        try:
            modules = Module.objects.all().order_by('moduleId')
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
            logger.error(f"Error getAllModules: {e}")
            raise Exception(str(e))

    def getModuleById(self, module_id: int) -> dict:
        try:
            module = Module.objects.filter(moduleId=module_id).first()
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
            logger.error(f"Error getModuleById: {e}")
            raise Exception(str(e))

    def updateModuleById(self, module_id: int, dto: dict) -> dict:
        try:
            module = Module.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Such Module Doesn't Exist")
                
            func_id = dto.get("functionalityId")
            functionality = Functionality.objects.filter(id=func_id).first()
            if not functionality:
                raise Exception("Functionality not found.")
                
            module.moduleName = dto.get("moduleName")
            module.functionality = functionality
            module.save()
            
            action_ids = dto.get("actions", [])
            self.assignPolicies({
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
            logger.error(f"Error updateModuleById: {e}")
            raise e

    def assignPolicies(self, assign_dto: dict) -> None:
        try:
            module_id = assign_dto.get("moduleId")
            module = Module.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Module not found")
                
            ModuleActions.objects.filter(module=module).delete()
            
            action_ids = assign_dto.get("actionIds", [])
            for action_id in action_ids:
                action = Actions.objects.filter(actionId=action_id).first()
                if action:
                    ModuleActions.objects.create(
                        module=module,
                        action=action
                    )
        except Exception as e:
            logger.error(f"Error assignPolicies: {e}")
            raise Exception(str(e))

    def deleteModuleById(self, module_id: int) -> None:
        try:
            module = Module.objects.filter(moduleId=module_id).first()
            if not module:
                raise Exception("Module not found")
            module.delete()
        except Exception as e:
            logger.error(f"Error deleteModuleById: {e}")
            raise Exception(str(e))
