# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .account import *
from .account_grant import *
from .account_parameter import *
from .account_password_policy_attachment import *
from .alert import *
from .api_integration import *
from .database import *
from .database_grant import *
from .database_role import *
from .dynamic_table import *
from .email_notification_integration import *
from .external_function import *
from .external_oauth_integration import *
from .external_table import *
from .external_table_grant import *
from .failover_group import *
from .failover_group_grant import *
from .file_format import *
from .file_format_grant import *
from .function import *
from .function_grant import *
from .get_accounts import *
from .get_alerts import *
from .get_current_account import *
from .get_current_role import *
from .get_database import *
from .get_database_role import *
from .get_database_roles import *
from .get_databases import *
from .get_dynamic_tables import *
from .get_external_functions import *
from .get_external_tables import *
from .get_failover_groups import *
from .get_file_formats import *
from .get_functions import *
from .get_grants import *
from .get_masking_policies import *
from .get_materialized_views import *
from .get_parameters import *
from .get_pipes import *
from .get_procedures import *
from .get_resource_monitors import *
from .get_role import *
from .get_roles import *
from .get_row_access_policies import *
from .get_schemas import *
from .get_sequences import *
from .get_shares import *
from .get_stages import *
from .get_storage_integrations import *
from .get_streams import *
from .get_system_generate_scim_access_token import *
from .get_system_get_aws_sns_iam_policy import *
from .get_system_get_private_link_config import *
from .get_system_get_snowflake_platform_info import *
from .get_tables import *
from .get_tasks import *
from .get_users import *
from .get_views import *
from .get_warehouses import *
from .grant_account_role import *
from .grant_application_role import *
from .grant_database_role import *
from .grant_ownership import *
from .grant_privileges_to_account_role import *
from .grant_privileges_to_database_role import *
from .grant_privileges_to_role import *
from .grant_privileges_to_share import *
from .integration_grant import *
from .managed_account import *
from .masking_policy import *
from .masking_policy_grant import *
from .materialized_view import *
from .materialized_view_grant import *
from .network_policy import *
from .network_policy_attachment import *
from .notification_integration import *
from .oauth_integration import *
from .object_parameter import *
from .password_policy import *
from .pipe import *
from .pipe_grant import *
from .procedure import *
from .procedure_grant import *
from .provider import *
from .resource_monitor import *
from .resource_monitor_grant import *
from .role import *
from .role_grants import *
from .role_ownership_grant import *
from .row_access_policy import *
from .row_access_policy_grant import *
from .saml_integration import *
from .schema import *
from .schema_grant import *
from .scim_integration import *
from .sequence import *
from .sequence_grant import *
from .session_parameter import *
from .share import *
from .stage import *
from .stage_grant import *
from .storage_integration import *
from .stream import *
from .stream_grant import *
from .table import *
from .table_column_masking_policy_application import *
from .table_constraint import *
from .table_grant import *
from .tag import *
from .tag_association import *
from .tag_grant import *
from .tag_masking_policy_association import *
from .task import *
from .task_grant import *
from .unsafe_execute import *
from .user import *
from .user_grant import *
from .user_ownership_grant import *
from .user_password_policy_attachment import *
from .user_public_keys import *
from .view import *
from .view_grant import *
from .warehouse import *
from .warehouse_grant import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_snowflake.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_snowflake.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "snowflake",
  "mod": "index/account",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/account:Account": "Account"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/accountGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/accountGrant:AccountGrant": "AccountGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/accountParameter",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/accountParameter:AccountParameter": "AccountParameter"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/accountPasswordPolicyAttachment",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/accountPasswordPolicyAttachment:AccountPasswordPolicyAttachment": "AccountPasswordPolicyAttachment"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/alert",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/alert:Alert": "Alert"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/apiIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/apiIntegration:ApiIntegration": "ApiIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/database",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/database:Database": "Database"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/databaseGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/databaseGrant:DatabaseGrant": "DatabaseGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/databaseRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/databaseRole:DatabaseRole": "DatabaseRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/dynamicTable",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/dynamicTable:DynamicTable": "DynamicTable"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/emailNotificationIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/emailNotificationIntegration:EmailNotificationIntegration": "EmailNotificationIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/externalFunction",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/externalFunction:ExternalFunction": "ExternalFunction"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/externalOauthIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/externalOauthIntegration:ExternalOauthIntegration": "ExternalOauthIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/externalTable",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/externalTable:ExternalTable": "ExternalTable"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/externalTableGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/externalTableGrant:ExternalTableGrant": "ExternalTableGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/failoverGroup",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/failoverGroup:FailoverGroup": "FailoverGroup"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/failoverGroupGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/failoverGroupGrant:FailoverGroupGrant": "FailoverGroupGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/fileFormat",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/fileFormat:FileFormat": "FileFormat"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/fileFormatGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/fileFormatGrant:FileFormatGrant": "FileFormatGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/function",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/function:Function": "Function"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/functionGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/functionGrant:FunctionGrant": "FunctionGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantAccountRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantAccountRole:GrantAccountRole": "GrantAccountRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantApplicationRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantApplicationRole:GrantApplicationRole": "GrantApplicationRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantDatabaseRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantDatabaseRole:GrantDatabaseRole": "GrantDatabaseRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantOwnership",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantOwnership:GrantOwnership": "GrantOwnership"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantPrivilegesToAccountRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantPrivilegesToAccountRole:GrantPrivilegesToAccountRole": "GrantPrivilegesToAccountRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantPrivilegesToDatabaseRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantPrivilegesToDatabaseRole:GrantPrivilegesToDatabaseRole": "GrantPrivilegesToDatabaseRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantPrivilegesToRole",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantPrivilegesToRole:GrantPrivilegesToRole": "GrantPrivilegesToRole"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/grantPrivilegesToShare",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/grantPrivilegesToShare:GrantPrivilegesToShare": "GrantPrivilegesToShare"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/integrationGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/integrationGrant:IntegrationGrant": "IntegrationGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/managedAccount",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/managedAccount:ManagedAccount": "ManagedAccount"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/maskingPolicy",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/maskingPolicy:MaskingPolicy": "MaskingPolicy"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/maskingPolicyGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/maskingPolicyGrant:MaskingPolicyGrant": "MaskingPolicyGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/materializedView",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/materializedView:MaterializedView": "MaterializedView"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/materializedViewGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/materializedViewGrant:MaterializedViewGrant": "MaterializedViewGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/networkPolicy",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/networkPolicy:NetworkPolicy": "NetworkPolicy"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/networkPolicyAttachment",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/networkPolicyAttachment:NetworkPolicyAttachment": "NetworkPolicyAttachment"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/notificationIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/notificationIntegration:NotificationIntegration": "NotificationIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/oauthIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/oauthIntegration:OauthIntegration": "OauthIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/objectParameter",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/objectParameter:ObjectParameter": "ObjectParameter"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/passwordPolicy",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/passwordPolicy:PasswordPolicy": "PasswordPolicy"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/pipe",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/pipe:Pipe": "Pipe"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/pipeGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/pipeGrant:PipeGrant": "PipeGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/procedure",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/procedure:Procedure": "Procedure"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/procedureGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/procedureGrant:ProcedureGrant": "ProcedureGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/resourceMonitor",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/resourceMonitor:ResourceMonitor": "ResourceMonitor"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/resourceMonitorGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/resourceMonitorGrant:ResourceMonitorGrant": "ResourceMonitorGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/role",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/role:Role": "Role"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/roleGrants",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/roleGrants:RoleGrants": "RoleGrants"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/roleOwnershipGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/roleOwnershipGrant:RoleOwnershipGrant": "RoleOwnershipGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/rowAccessPolicy",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/rowAccessPolicy:RowAccessPolicy": "RowAccessPolicy"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/rowAccessPolicyGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/rowAccessPolicyGrant:RowAccessPolicyGrant": "RowAccessPolicyGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/samlIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/samlIntegration:SamlIntegration": "SamlIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/schema",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/schema:Schema": "Schema"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/schemaGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/schemaGrant:SchemaGrant": "SchemaGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/scimIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/scimIntegration:ScimIntegration": "ScimIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/sequence",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/sequence:Sequence": "Sequence"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/sequenceGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/sequenceGrant:SequenceGrant": "SequenceGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/sessionParameter",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/sessionParameter:SessionParameter": "SessionParameter"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/share",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/share:Share": "Share"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/stage",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/stage:Stage": "Stage"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/stageGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/stageGrant:StageGrant": "StageGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/storageIntegration",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/storageIntegration:StorageIntegration": "StorageIntegration"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/stream",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/stream:Stream": "Stream"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/streamGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/streamGrant:StreamGrant": "StreamGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/table",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/table:Table": "Table"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tableColumnMaskingPolicyApplication",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tableColumnMaskingPolicyApplication:TableColumnMaskingPolicyApplication": "TableColumnMaskingPolicyApplication"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tableConstraint",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tableConstraint:TableConstraint": "TableConstraint"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tableGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tableGrant:TableGrant": "TableGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tag",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tag:Tag": "Tag"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tagAssociation",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tagAssociation:TagAssociation": "TagAssociation"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tagGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tagGrant:TagGrant": "TagGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/tagMaskingPolicyAssociation",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/tagMaskingPolicyAssociation:TagMaskingPolicyAssociation": "TagMaskingPolicyAssociation"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/task",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/task:Task": "Task"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/taskGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/taskGrant:TaskGrant": "TaskGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/unsafeExecute",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/unsafeExecute:UnsafeExecute": "UnsafeExecute"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/user",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/user:User": "User"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/userGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/userGrant:UserGrant": "UserGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/userOwnershipGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/userOwnershipGrant:UserOwnershipGrant": "UserOwnershipGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/userPasswordPolicyAttachment",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/userPasswordPolicyAttachment:UserPasswordPolicyAttachment": "UserPasswordPolicyAttachment"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/userPublicKeys",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/userPublicKeys:UserPublicKeys": "UserPublicKeys"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/view",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/view:View": "View"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/viewGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/viewGrant:ViewGrant": "ViewGrant"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/warehouse",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/warehouse:Warehouse": "Warehouse"
  }
 },
 {
  "pkg": "snowflake",
  "mod": "index/warehouseGrant",
  "fqn": "pulumi_snowflake",
  "classes": {
   "snowflake:index/warehouseGrant:WarehouseGrant": "WarehouseGrant"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "snowflake",
  "token": "pulumi:providers:snowflake",
  "fqn": "pulumi_snowflake",
  "class": "Provider"
 }
]
"""
)
