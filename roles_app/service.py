import logging
from django.core.paginator import Paginator
from common.models import Roles, Functionality, Module, ModuleActions, RoleModuleActions, Actions

logger = logging.getLogger(__name__)

class RoleService:

    def getAllRolesList(self) -> list:
        try:
            roles = Roles.objects.all().order_by('roleId')
            dtos = []
            for r in roles:
                dtos.append({
                    "roleId": r.roleId,
                    "roleName": r.roleName
                })
            return dtos
        except Exception as e:
            logger.error(f"Error getAllRolesList: {e}")
            raise Exception(str(e))

    def createRole(self, dto: dict) -> dict:
        try:
            role = Roles(roleName=dto.get("roleName"))
            role.save()
            
            roles_actions = dto.get("rolesActions", {})
            self.savePolicy(role.roleId, roles_actions)
            
            return {
                "roleId": role.roleId,
                "roleName": role.roleName,
                "rolesActions": roles_actions
            }
        except Exception as e:
            logger.error(f"Error createRole: {e}")
            raise Exception(str(e))

    def paginate_roles(self, queryset, page: int, size: int) -> dict:
        paginator = Paginator(queryset, size if size > 0 else 10)
        django_page_num = page + 1
        
        try:
            page_obj = paginator.page(django_page_num)
        except Exception:
            page_obj = paginator.page(1)
            
        dtos = []
        for role in page_obj.object_list:
            dtos.append({
                "roleId": role.roleId,
                "roleName": role.roleName,
                "rolesActions": self.getPolicy(role.roleId)
            })
            
        return {
            "getTotalPages": paginator.num_pages,
            "getNumber": page_obj.number - 1,
            "getSize": paginator.per_page,
            "getTotalRecords": paginator.count,
            "rolesList": dtos
        }

    def rolesList(self, search_key: str, page: int, size: int) -> dict:
        try:
            if search_key:
                queryset = Roles.objects.filter(roleName__icontains=search_key).order_by('roleId')
            else:
                queryset = Roles.objects.all().order_by('roleId')
            return self.paginate_roles(queryset, page, size)
        except Exception as e:
            logger.error(f"Error rolesList: {e}")
            raise Exception(str(e))

    def getAllRoles(self) -> dict:
        try:
            role_list = Roles.objects.exclude(roleName__iexact="owner").order_by('roleId')
            dtos = []
            for role in role_list:
                dtos.append({
                    "roleId": role.roleId,
                    "roleName": role.roleName
                })
            return {"rolesList": dtos}
        except Exception as e:
            logger.error(f"Error getAllRoles: {e}")
            raise Exception(str(e))

    def getRoleById(self, role_id: int) -> dict:
        try:
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
            return {
                "roleId": role.roleId,
                "roleName": role.roleName,
                "rolesActions": self.getPolicy(role.roleId)
            }
        except Exception as e:
            logger.error(f"Error getRoleById: {e}")
            raise Exception(str(e))

    def updateById(self, role_id: int, dto: dict) -> dict:
        try:
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Such Role Doesn't Exist")
                
            role.roleName = dto.get("roleName")
            role.save()
            
            roles_actions = dto.get("rolesActions", {})
            self.savePolicy(role.roleId, roles_actions)
            
            return {
                "roleId": role.roleId,
                "roleName": role.roleName,
                "rolesActions": roles_actions
            }
        except Exception as e:
            logger.error(f"Error updateById: {e}")
            raise e

    def deleteRoleById(self, role_id: int) -> None:
        try:
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
            role.delete()
        except Exception as e:
            logger.error(f"Error deleteRoleById: {e}")
            raise Exception(str(e))

    def getPolicy(self, role_id: int) -> dict:
        try:
            functionalities = []
            func_list = Functionality.objects.all().order_by('id')
            for func in func_list:
                modules = []
                module_list = Module.objects.filter(functionality_id=func.id).order_by('moduleId')
                for module in module_list:
                    module_assigned_policy = list(
                        ModuleActions.objects.filter(module=module).values_list('action_id', flat=True).order_by('action_id')
                    )
                    
                    role_assigned_policy = []
                    if role_id != 0:
                        role_assigned_policy = list(
                            RoleModuleActions.objects.filter(
                                role_id=role_id,
                                moduleActions__module=module
                            ).values_list('moduleActions__action_id', flat=True).order_by('moduleActions__action_id')
                        )
                        
                    modules.append({
                        "moduleId": module.moduleId,
                        "moduleName": module.moduleName,
                        "moduleAssignedActions": module_assigned_policy,
                        "roleAssignedActions": role_assigned_policy
                    })
                    
                functionalities.append({
                    "functionalityId": func.id,
                    "functionalityName": func.functionalityName,
                    "modules": modules
                })
                
            return {"functionalities": functionalities}
        except Exception as e:
            logger.error(f"Error getPolicy: {e}")
            raise Exception(str(e))

    def savePolicy(self, role_id: int, roles_actions_dto: dict) -> dict:
        try:
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
                
            RoleModuleActions.objects.filter(role=role).delete()
            
            functionalities = roles_actions_dto.get("functionalities", [])
            for func_data in functionalities:
                modules = func_data.get("modules", [])
                for mod_data in modules:
                    role_assigned = mod_data.get("roleAssignedActions", [])
                    module_id = mod_data.get("moduleId")
                    for action_id in role_assigned:
                        module_action = ModuleActions.objects.filter(module_id=module_id, action_id=action_id).first()
                        if module_action:
                            RoleModuleActions.objects.create(
                                role=role,
                                moduleActions=module_action
                            )
            return roles_actions_dto
        except Exception as e:
            logger.error(f"Error savePolicy: {e}")
            raise Exception(str(e))
