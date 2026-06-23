import logging
from django.db import transaction
from django.core.paginator import Paginator
from common.models import (
    CompanyEmployeeRoles,
    CompanyDetails,
    CompanyFunctionality,
    CompanyModules,
    CompanyModuleActions,
    CompanyRoleModuleActions,
)

logger = logging.getLogger(__name__)

class CompanyEmployeeRoleService:
    def get_all_roles_list(self) -> list:
        try:
            roles = CompanyEmployeeRoles.objects.all().order_by('roleId')
            role_dto_list = []
            for role in roles:
                role_dto_list.append({
                    "roleName": role.roleName,
                    "roleId": role.roleId
                })
            return role_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_roles_list: {e}")
            raise Exception(str(e))

    def roles_list(self, search_key: str, page: int, size: int) -> dict:
        try:
            if search_key:
                queryset = CompanyEmployeeRoles.objects.filter(roleName__icontains=search_key).order_by('roleId')
            else:
                queryset = CompanyEmployeeRoles.objects.all().order_by('roleId')
            
            paginator = Paginator(queryset, size if size > 0 else 10)
            django_page_num = page + 1
            
            try:
                page_obj = paginator.page(django_page_num)
            except Exception:
                page_obj = paginator.page(1)
                
            roles_dtos = []
            for role in page_obj.object_list:
                roles_dto = {
                    "roleId": role.roleId,
                    "companyId": role.companyDetails.id if role.companyDetails else None,
                    "roleName": role.roleName,
                    "rolesActions": self.get_policy(role.roleId)
                }
                roles_dtos.append(roles_dto)
                
            return {
                "getTotalPages": paginator.num_pages,
                "getNumber": page_obj.number - 1,
                "getSize": paginator.per_page,
                "getTotalRecords": paginator.count,
                "rolesList": roles_dtos
            }
        except Exception as e:
            logger.error(f"Error in roles_list: {e}")
            raise Exception(str(e))

    def get_all_roles(self) -> dict:
        try:
            # Query roles except Owner (case-insensitive exclude)
            role_list = CompanyEmployeeRoles.objects.exclude(roleName__iexact="owner").order_by('roleId')
            roles_dtos = []
            for role in role_list:
                roles_dtos.append({
                    "roleId": role.roleId,
                    "companyId": role.companyDetails.id if role.companyDetails else None,
                    "roleName": role.roleName
                })
            return {"rolesList": roles_dtos}
        except Exception as e:
            logger.error(f"Error in get_all_roles: {e}")
            raise Exception(str(e))

    def get_all_roles_by_company_id(self, company_id: int) -> list:
        try:
            company_employee_roles_list = CompanyEmployeeRoles.objects.filter(companyDetails_id=company_id).order_by('roleId')
            company_employee_roles_dto_list = []
            for role in company_employee_roles_list:
                company_employee_roles_dto_list.append(self.get_role(role.roleId))
            return company_employee_roles_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_roles_by_company_id: {e}")
            raise Exception(str(e))

    def get_role(self, id: int) -> dict:
        try:
            role = CompanyEmployeeRoles.objects.filter(roleId=id).first()
            if not role:
                raise Exception("Role not found")
            
            return {
                "roleId": role.roleId,
                "companyId": role.companyDetails.id if role.companyDetails else None,
                "roleName": role.roleName,
                "rolesActions": self.get_policy(id)
            }
        except Exception as e:
            logger.error(f"Error in get_role: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def create_role(self, company_employee_roles_dto: dict) -> dict:
        try:
            company_id = company_employee_roles_dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
                
            role = CompanyEmployeeRoles(
                companyDetails=company_details,
                roleName=company_employee_roles_dto.get("roleName")
            )
            role.save()
            
            roles_actions = company_employee_roles_dto.get("rolesActions")
            if roles_actions:
                self.save_policy(role.roleId, roles_actions)
                
            return {
                "roleId": role.roleId,
                "companyId": company_details.id,
                "roleName": role.roleName,
                "rolesActions": roles_actions
            }
        except Exception as e:
            logger.error(f"Error in create_role: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def update_role(self, id: int, company_employee_roles_dto: dict) -> dict:
        try:
            company_id = company_employee_roles_dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
                
            role = CompanyEmployeeRoles.objects.filter(roleId=id).first()
            if not role:
                raise Exception("Role not found")
                
            role.companyDetails = company_details
            role.roleName = company_employee_roles_dto.get("roleName")
            role.save()
            
            roles_actions = company_employee_roles_dto.get("rolesActions")
            if roles_actions:
                self.save_policy(id, roles_actions)
                
            return {
                "roleId": role.roleId,
                "companyId": company_details.id,
                "roleName": role.roleName,
                "rolesActions": roles_actions
            }
        except Exception as e:
            logger.error(f"Error in update_role: {e}")
            raise Exception(str(e))

    def delete_role(self, id: int) -> None:
        try:
            role = CompanyEmployeeRoles.objects.filter(roleId=id).first()
            if not role:
                raise Exception("Role not found")
            role.delete()
        except Exception as e:
            logger.error(f"Error in delete_role: {e}")
            raise Exception(str(e))

    def get_policy(self, role_id: int) -> dict:
        try:
            if role_id != 0:
                role = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
                if not role:
                    raise Exception("No such Role Exist")

            functionalities = []
            functionality_list = CompanyFunctionality.objects.all().order_by('id')
            
            for functionality in functionality_list:
                modules = []
                module_list = CompanyModules.objects.filter(functionality=functionality).order_by('moduleId')
                
                for module in module_list:
                    module_policies = CompanyModuleActions.objects.filter(module=module)
                    module_assigned_policy = sorted([
                        mp.action.actionId for mp in module_policies if mp.action
                    ])
                    
                    if role_id == 0:
                        role_assigned_policy = []
                    else:
                        role_module_actions = CompanyRoleModuleActions.objects.filter(
                            role_id=role_id,
                            moduleActions__module=module
                        )
                        role_assigned_policy = sorted(list(set([
                            rma.moduleActions.action.actionId
                            for rma in role_module_actions
                            if rma.moduleActions and rma.moduleActions.action
                        ])))
                        
                    modules.append({
                        "moduleId": module.moduleId,
                        "moduleName": module.moduleName,
                        "moduleAssignedActions": module_assigned_policy,
                        "roleAssignedActions": role_assigned_policy
                    })
                    
                functionalities.append({
                    "functionalityId": functionality.id,
                    "functionalityName": functionality.functionalityName,
                    "modules": modules
                })
                
            return {
                "functionalities": functionalities
            }
        except Exception as e:
            logger.error(f"Error in get_policy for role {role_id}: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def save_policy(self, role_id: int, role_action_dto: dict) -> dict:
        try:
            role = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
                
            CompanyRoleModuleActions.objects.filter(role=role).delete()
            
            functionalities = role_action_dto.get("functionalities", [])
            for func_data in functionalities:
                modules = func_data.get("modules", [])
                for mod_data in modules:
                    module_id = mod_data.get("moduleId")
                    role_assigned_actions = mod_data.get("roleAssignedActions", [])
                    if role_assigned_actions:
                        for action_id in role_assigned_actions:
                            module_policy = CompanyModuleActions.objects.filter(
                                module_id=module_id,
                                action_id=action_id
                            ).first()
                            if module_policy:
                                CompanyRoleModuleActions.objects.create(
                                    role=role,
                                    moduleActions=module_policy
                                )
            return role_action_dto
        except Exception as e:
            logger.error(f"Error in save_policy for role {role_id}: {e}")
            raise Exception(str(e))
