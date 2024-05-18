# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['MaterializedViewArgs', 'MaterializedView']

@pulumi.input_type
class MaterializedViewArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 schema: pulumi.Input[str],
                 statement: pulumi.Input[str],
                 warehouse: pulumi.Input[str],
                 comment: Optional[pulumi.Input[str]] = None,
                 is_secure: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 or_replace: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]] = None):
        """
        The set of arguments for constructing a MaterializedView resource.
        :param pulumi.Input[str] database: The database in which to create the view. Don't use the | character.
        :param pulumi.Input[str] schema: The schema in which to create the view. Don't use the | character.
        :param pulumi.Input[str] statement: Specifies the query used to create the view.
        :param pulumi.Input[str] warehouse: The warehouse name.
        :param pulumi.Input[str] comment: Specifies a comment for the view.
        :param pulumi.Input[bool] is_secure: Specifies that the view is secure.
        :param pulumi.Input[str] name: Specifies the identifier for the view; must be unique for the schema in which the view is created.
        :param pulumi.Input[bool] or_replace: Overwrites the View if it exists.
        :param pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]] tags: Definitions of a tag to associate with the resource.
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "schema", schema)
        pulumi.set(__self__, "statement", statement)
        pulumi.set(__self__, "warehouse", warehouse)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if is_secure is not None:
            pulumi.set(__self__, "is_secure", is_secure)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if or_replace is not None:
            pulumi.set(__self__, "or_replace", or_replace)
        if tags is not None:
            warnings.warn("""Use the 'snowflake_tag_association' resource instead.""", DeprecationWarning)
            pulumi.log.warn("""tags is deprecated: Use the 'snowflake_tag_association' resource instead.""")
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        The database in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Input[str]:
        """
        The schema in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter
    def statement(self) -> pulumi.Input[str]:
        """
        Specifies the query used to create the view.
        """
        return pulumi.get(self, "statement")

    @statement.setter
    def statement(self, value: pulumi.Input[str]):
        pulumi.set(self, "statement", value)

    @property
    @pulumi.getter
    def warehouse(self) -> pulumi.Input[str]:
        """
        The warehouse name.
        """
        return pulumi.get(self, "warehouse")

    @warehouse.setter
    def warehouse(self, value: pulumi.Input[str]):
        pulumi.set(self, "warehouse", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the view.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="isSecure")
    def is_secure(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies that the view is secure.
        """
        return pulumi.get(self, "is_secure")

    @is_secure.setter
    def is_secure(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_secure", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the view; must be unique for the schema in which the view is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orReplace")
    def or_replace(self) -> Optional[pulumi.Input[bool]]:
        """
        Overwrites the View if it exists.
        """
        return pulumi.get(self, "or_replace")

    @or_replace.setter
    def or_replace(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "or_replace", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]]:
        """
        Definitions of a tag to associate with the resource.
        """
        warnings.warn("""Use the 'snowflake_tag_association' resource instead.""", DeprecationWarning)
        pulumi.log.warn("""tags is deprecated: Use the 'snowflake_tag_association' resource instead.""")

        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _MaterializedViewState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 is_secure: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 or_replace: Optional[pulumi.Input[bool]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 statement: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MaterializedView resources.
        :param pulumi.Input[str] comment: Specifies a comment for the view.
        :param pulumi.Input[str] database: The database in which to create the view. Don't use the | character.
        :param pulumi.Input[bool] is_secure: Specifies that the view is secure.
        :param pulumi.Input[str] name: Specifies the identifier for the view; must be unique for the schema in which the view is created.
        :param pulumi.Input[bool] or_replace: Overwrites the View if it exists.
        :param pulumi.Input[str] schema: The schema in which to create the view. Don't use the | character.
        :param pulumi.Input[str] statement: Specifies the query used to create the view.
        :param pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]] tags: Definitions of a tag to associate with the resource.
        :param pulumi.Input[str] warehouse: The warehouse name.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if is_secure is not None:
            pulumi.set(__self__, "is_secure", is_secure)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if or_replace is not None:
            pulumi.set(__self__, "or_replace", or_replace)
        if schema is not None:
            pulumi.set(__self__, "schema", schema)
        if statement is not None:
            pulumi.set(__self__, "statement", statement)
        if tags is not None:
            warnings.warn("""Use the 'snowflake_tag_association' resource instead.""", DeprecationWarning)
            pulumi.log.warn("""tags is deprecated: Use the 'snowflake_tag_association' resource instead.""")
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if warehouse is not None:
            pulumi.set(__self__, "warehouse", warehouse)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the view.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        The database in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter(name="isSecure")
    def is_secure(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies that the view is secure.
        """
        return pulumi.get(self, "is_secure")

    @is_secure.setter
    def is_secure(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_secure", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the view; must be unique for the schema in which the view is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orReplace")
    def or_replace(self) -> Optional[pulumi.Input[bool]]:
        """
        Overwrites the View if it exists.
        """
        return pulumi.get(self, "or_replace")

    @or_replace.setter
    def or_replace(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "or_replace", value)

    @property
    @pulumi.getter
    def schema(self) -> Optional[pulumi.Input[str]]:
        """
        The schema in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter
    def statement(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the query used to create the view.
        """
        return pulumi.get(self, "statement")

    @statement.setter
    def statement(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "statement", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]]:
        """
        Definitions of a tag to associate with the resource.
        """
        warnings.warn("""Use the 'snowflake_tag_association' resource instead.""", DeprecationWarning)
        pulumi.log.warn("""tags is deprecated: Use the 'snowflake_tag_association' resource instead.""")

        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MaterializedViewTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def warehouse(self) -> Optional[pulumi.Input[str]]:
        """
        The warehouse name.
        """
        return pulumi.get(self, "warehouse")

    @warehouse.setter
    def warehouse(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "warehouse", value)


class MaterializedView(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 is_secure: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 or_replace: Optional[pulumi.Input[bool]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 statement: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MaterializedViewTagArgs']]]]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        view = snowflake.MaterializedView("view",
            database="db",
            schema="schema",
            name="view",
            warehouse="warehouse",
            comment="comment",
            statement="select * from foo;\\n",
            or_replace=False,
            is_secure=False)
        ```

        ## Import

        format is database name | schema name | view name

        ```sh
        $ pulumi import snowflake:index/materializedView:MaterializedView example 'dbName|schemaName|viewName'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: Specifies a comment for the view.
        :param pulumi.Input[str] database: The database in which to create the view. Don't use the | character.
        :param pulumi.Input[bool] is_secure: Specifies that the view is secure.
        :param pulumi.Input[str] name: Specifies the identifier for the view; must be unique for the schema in which the view is created.
        :param pulumi.Input[bool] or_replace: Overwrites the View if it exists.
        :param pulumi.Input[str] schema: The schema in which to create the view. Don't use the | character.
        :param pulumi.Input[str] statement: Specifies the query used to create the view.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MaterializedViewTagArgs']]]] tags: Definitions of a tag to associate with the resource.
        :param pulumi.Input[str] warehouse: The warehouse name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MaterializedViewArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        view = snowflake.MaterializedView("view",
            database="db",
            schema="schema",
            name="view",
            warehouse="warehouse",
            comment="comment",
            statement="select * from foo;\\n",
            or_replace=False,
            is_secure=False)
        ```

        ## Import

        format is database name | schema name | view name

        ```sh
        $ pulumi import snowflake:index/materializedView:MaterializedView example 'dbName|schemaName|viewName'
        ```

        :param str resource_name: The name of the resource.
        :param MaterializedViewArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MaterializedViewArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 is_secure: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 or_replace: Optional[pulumi.Input[bool]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 statement: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MaterializedViewTagArgs']]]]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MaterializedViewArgs.__new__(MaterializedViewArgs)

            __props__.__dict__["comment"] = comment
            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            __props__.__dict__["is_secure"] = is_secure
            __props__.__dict__["name"] = name
            __props__.__dict__["or_replace"] = or_replace
            if schema is None and not opts.urn:
                raise TypeError("Missing required property 'schema'")
            __props__.__dict__["schema"] = schema
            if statement is None and not opts.urn:
                raise TypeError("Missing required property 'statement'")
            __props__.__dict__["statement"] = statement
            __props__.__dict__["tags"] = tags
            if warehouse is None and not opts.urn:
                raise TypeError("Missing required property 'warehouse'")
            __props__.__dict__["warehouse"] = warehouse
        super(MaterializedView, __self__).__init__(
            'snowflake:index/materializedView:MaterializedView',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            database: Optional[pulumi.Input[str]] = None,
            is_secure: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            or_replace: Optional[pulumi.Input[bool]] = None,
            schema: Optional[pulumi.Input[str]] = None,
            statement: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MaterializedViewTagArgs']]]]] = None,
            warehouse: Optional[pulumi.Input[str]] = None) -> 'MaterializedView':
        """
        Get an existing MaterializedView resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: Specifies a comment for the view.
        :param pulumi.Input[str] database: The database in which to create the view. Don't use the | character.
        :param pulumi.Input[bool] is_secure: Specifies that the view is secure.
        :param pulumi.Input[str] name: Specifies the identifier for the view; must be unique for the schema in which the view is created.
        :param pulumi.Input[bool] or_replace: Overwrites the View if it exists.
        :param pulumi.Input[str] schema: The schema in which to create the view. Don't use the | character.
        :param pulumi.Input[str] statement: Specifies the query used to create the view.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MaterializedViewTagArgs']]]] tags: Definitions of a tag to associate with the resource.
        :param pulumi.Input[str] warehouse: The warehouse name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MaterializedViewState.__new__(_MaterializedViewState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["database"] = database
        __props__.__dict__["is_secure"] = is_secure
        __props__.__dict__["name"] = name
        __props__.__dict__["or_replace"] = or_replace
        __props__.__dict__["schema"] = schema
        __props__.__dict__["statement"] = statement
        __props__.__dict__["tags"] = tags
        __props__.__dict__["warehouse"] = warehouse
        return MaterializedView(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the view.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The database in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter(name="isSecure")
    def is_secure(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies that the view is secure.
        """
        return pulumi.get(self, "is_secure")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the identifier for the view; must be unique for the schema in which the view is created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orReplace")
    def or_replace(self) -> pulumi.Output[Optional[bool]]:
        """
        Overwrites the View if it exists.
        """
        return pulumi.get(self, "or_replace")

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Output[str]:
        """
        The schema in which to create the view. Don't use the | character.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter
    def statement(self) -> pulumi.Output[str]:
        """
        Specifies the query used to create the view.
        """
        return pulumi.get(self, "statement")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.MaterializedViewTag']]]:
        """
        Definitions of a tag to associate with the resource.
        """
        warnings.warn("""Use the 'snowflake_tag_association' resource instead.""", DeprecationWarning)
        pulumi.log.warn("""tags is deprecated: Use the 'snowflake_tag_association' resource instead.""")

        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def warehouse(self) -> pulumi.Output[str]:
        """
        The warehouse name.
        """
        return pulumi.get(self, "warehouse")

