# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ManagedAccountArgs', 'ManagedAccount']

@pulumi.input_type
class ManagedAccountArgs:
    def __init__(__self__, *,
                 admin_name: pulumi.Input[str],
                 admin_password: pulumi.Input[str],
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedAccount resource.
        :param pulumi.Input[str] admin_name: Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        :param pulumi.Input[str] admin_password: Password for the initial user in the managed account.
        :param pulumi.Input[str] comment: Specifies a comment for the managed account.
        :param pulumi.Input[str] name: Identifier for the managed account; must be unique for your account.
        :param pulumi.Input[str] type: Specifies the type of managed account.
        """
        pulumi.set(__self__, "admin_name", admin_name)
        pulumi.set(__self__, "admin_password", admin_password)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="adminName")
    def admin_name(self) -> pulumi.Input[str]:
        """
        Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        """
        return pulumi.get(self, "admin_name")

    @admin_name.setter
    def admin_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_name", value)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Input[str]:
        """
        Password for the initial user in the managed account.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the managed account.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier for the managed account; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of managed account.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _ManagedAccountState:
    def __init__(__self__, *,
                 admin_name: Optional[pulumi.Input[str]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 cloud: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 created_on: Optional[pulumi.Input[str]] = None,
                 locator: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedAccount resources.
        :param pulumi.Input[str] admin_name: Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        :param pulumi.Input[str] admin_password: Password for the initial user in the managed account.
        :param pulumi.Input[str] cloud: Cloud in which the managed account is located.
        :param pulumi.Input[str] comment: Specifies a comment for the managed account.
        :param pulumi.Input[str] created_on: Date and time when the managed account was created.
        :param pulumi.Input[str] locator: Display name of the managed account.
        :param pulumi.Input[str] name: Identifier for the managed account; must be unique for your account.
        :param pulumi.Input[str] region: Snowflake Region in which the managed account is located.
        :param pulumi.Input[str] type: Specifies the type of managed account.
        :param pulumi.Input[str] url: URL for accessing the managed account, particularly through the web interface.
        """
        if admin_name is not None:
            pulumi.set(__self__, "admin_name", admin_name)
        if admin_password is not None:
            pulumi.set(__self__, "admin_password", admin_password)
        if cloud is not None:
            pulumi.set(__self__, "cloud", cloud)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if created_on is not None:
            pulumi.set(__self__, "created_on", created_on)
        if locator is not None:
            pulumi.set(__self__, "locator", locator)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="adminName")
    def admin_name(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        """
        return pulumi.get(self, "admin_name")

    @admin_name.setter
    def admin_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "admin_name", value)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for the initial user in the managed account.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter
    def cloud(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud in which the managed account is located.
        """
        return pulumi.get(self, "cloud")

    @cloud.setter
    def cloud(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the managed account.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time when the managed account was created.
        """
        return pulumi.get(self, "created_on")

    @created_on.setter
    def created_on(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_on", value)

    @property
    @pulumi.getter
    def locator(self) -> Optional[pulumi.Input[str]]:
        """
        Display name of the managed account.
        """
        return pulumi.get(self, "locator")

    @locator.setter
    def locator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "locator", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier for the managed account; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Snowflake Region in which the managed account is located.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of managed account.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        URL for accessing the managed account, particularly through the web interface.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


class ManagedAccount(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_name: Optional[pulumi.Input[str]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import snowflake:index/managedAccount:ManagedAccount example name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] admin_name: Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        :param pulumi.Input[str] admin_password: Password for the initial user in the managed account.
        :param pulumi.Input[str] comment: Specifies a comment for the managed account.
        :param pulumi.Input[str] name: Identifier for the managed account; must be unique for your account.
        :param pulumi.Input[str] type: Specifies the type of managed account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedAccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import snowflake:index/managedAccount:ManagedAccount example name
        ```

        :param str resource_name: The name of the resource.
        :param ManagedAccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedAccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_name: Optional[pulumi.Input[str]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedAccountArgs.__new__(ManagedAccountArgs)

            if admin_name is None and not opts.urn:
                raise TypeError("Missing required property 'admin_name'")
            __props__.__dict__["admin_name"] = admin_name
            if admin_password is None and not opts.urn:
                raise TypeError("Missing required property 'admin_password'")
            __props__.__dict__["admin_password"] = None if admin_password is None else pulumi.Output.secret(admin_password)
            __props__.__dict__["comment"] = comment
            __props__.__dict__["name"] = name
            __props__.__dict__["type"] = type
            __props__.__dict__["cloud"] = None
            __props__.__dict__["created_on"] = None
            __props__.__dict__["locator"] = None
            __props__.__dict__["region"] = None
            __props__.__dict__["url"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["adminPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ManagedAccount, __self__).__init__(
            'snowflake:index/managedAccount:ManagedAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin_name: Optional[pulumi.Input[str]] = None,
            admin_password: Optional[pulumi.Input[str]] = None,
            cloud: Optional[pulumi.Input[str]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            created_on: Optional[pulumi.Input[str]] = None,
            locator: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'ManagedAccount':
        """
        Get an existing ManagedAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] admin_name: Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        :param pulumi.Input[str] admin_password: Password for the initial user in the managed account.
        :param pulumi.Input[str] cloud: Cloud in which the managed account is located.
        :param pulumi.Input[str] comment: Specifies a comment for the managed account.
        :param pulumi.Input[str] created_on: Date and time when the managed account was created.
        :param pulumi.Input[str] locator: Display name of the managed account.
        :param pulumi.Input[str] name: Identifier for the managed account; must be unique for your account.
        :param pulumi.Input[str] region: Snowflake Region in which the managed account is located.
        :param pulumi.Input[str] type: Specifies the type of managed account.
        :param pulumi.Input[str] url: URL for accessing the managed account, particularly through the web interface.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedAccountState.__new__(_ManagedAccountState)

        __props__.__dict__["admin_name"] = admin_name
        __props__.__dict__["admin_password"] = admin_password
        __props__.__dict__["cloud"] = cloud
        __props__.__dict__["comment"] = comment
        __props__.__dict__["created_on"] = created_on
        __props__.__dict__["locator"] = locator
        __props__.__dict__["name"] = name
        __props__.__dict__["region"] = region
        __props__.__dict__["type"] = type
        __props__.__dict__["url"] = url
        return ManagedAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adminName")
    def admin_name(self) -> pulumi.Output[str]:
        """
        Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the account.
        """
        return pulumi.get(self, "admin_name")

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Output[str]:
        """
        Password for the initial user in the managed account.
        """
        return pulumi.get(self, "admin_password")

    @property
    @pulumi.getter
    def cloud(self) -> pulumi.Output[str]:
        """
        Cloud in which the managed account is located.
        """
        return pulumi.get(self, "cloud")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the managed account.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> pulumi.Output[str]:
        """
        Date and time when the managed account was created.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter
    def locator(self) -> pulumi.Output[str]:
        """
        Display name of the managed account.
        """
        return pulumi.get(self, "locator")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Identifier for the managed account; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        Snowflake Region in which the managed account is located.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of managed account.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        URL for accessing the managed account, particularly through the web interface.
        """
        return pulumi.get(self, "url")

