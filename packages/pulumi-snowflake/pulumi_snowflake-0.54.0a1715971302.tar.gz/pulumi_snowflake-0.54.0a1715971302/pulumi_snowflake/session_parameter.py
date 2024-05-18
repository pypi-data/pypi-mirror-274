# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['SessionParameterArgs', 'SessionParameter']

@pulumi.input_type
class SessionParameterArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str],
                 on_account: Optional[pulumi.Input[bool]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SessionParameter resource.
        :param pulumi.Input[str] key: Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        :param pulumi.Input[str] value: Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        :param pulumi.Input[bool] on_account: If true, the session parameter will be set on the account level.
        :param pulumi.Input[str] user: The user to set the session parameter for. Required if on_account is false
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)
        if on_account is not None:
            pulumi.set(__self__, "on_account", on_account)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="onAccount")
    def on_account(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the session parameter will be set on the account level.
        """
        return pulumi.get(self, "on_account")

    @on_account.setter
    def on_account(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "on_account", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The user to set the session parameter for. Required if on_account is false
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


@pulumi.input_type
class _SessionParameterState:
    def __init__(__self__, *,
                 key: Optional[pulumi.Input[str]] = None,
                 on_account: Optional[pulumi.Input[bool]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SessionParameter resources.
        :param pulumi.Input[str] key: Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        :param pulumi.Input[bool] on_account: If true, the session parameter will be set on the account level.
        :param pulumi.Input[str] user: The user to set the session parameter for. Required if on_account is false
        :param pulumi.Input[str] value: Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        if key is not None:
            pulumi.set(__self__, "key", key)
        if on_account is not None:
            pulumi.set(__self__, "on_account", on_account)
        if user is not None:
            pulumi.set(__self__, "user", user)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="onAccount")
    def on_account(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the session parameter will be set on the account level.
        """
        return pulumi.get(self, "on_account")

    @on_account.setter
    def on_account(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "on_account", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The user to set the session parameter for. Required if on_account is false
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class SessionParameter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 on_account: Optional[pulumi.Input[bool]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        s = snowflake.SessionParameter("s",
            key="AUTOCOMMIT",
            value="false",
            user="TEST_USER")
        s2 = snowflake.SessionParameter("s2",
            key="BINARY_OUTPUT_FORMAT",
            value="BASE64",
            on_account=True)
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/sessionParameter:SessionParameter s <parameter_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key: Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        :param pulumi.Input[bool] on_account: If true, the session parameter will be set on the account level.
        :param pulumi.Input[str] user: The user to set the session parameter for. Required if on_account is false
        :param pulumi.Input[str] value: Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SessionParameterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        s = snowflake.SessionParameter("s",
            key="AUTOCOMMIT",
            value="false",
            user="TEST_USER")
        s2 = snowflake.SessionParameter("s2",
            key="BINARY_OUTPUT_FORMAT",
            value="BASE64",
            on_account=True)
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/sessionParameter:SessionParameter s <parameter_name>
        ```

        :param str resource_name: The name of the resource.
        :param SessionParameterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SessionParameterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 on_account: Optional[pulumi.Input[bool]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SessionParameterArgs.__new__(SessionParameterArgs)

            if key is None and not opts.urn:
                raise TypeError("Missing required property 'key'")
            __props__.__dict__["key"] = key
            __props__.__dict__["on_account"] = on_account
            __props__.__dict__["user"] = user
            if value is None and not opts.urn:
                raise TypeError("Missing required property 'value'")
            __props__.__dict__["value"] = value
        super(SessionParameter, __self__).__init__(
            'snowflake:index/sessionParameter:SessionParameter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            key: Optional[pulumi.Input[str]] = None,
            on_account: Optional[pulumi.Input[bool]] = None,
            user: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[str]] = None) -> 'SessionParameter':
        """
        Get an existing SessionParameter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key: Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        :param pulumi.Input[bool] on_account: If true, the session parameter will be set on the account level.
        :param pulumi.Input[str] user: The user to set the session parameter for. Required if on_account is false
        :param pulumi.Input[str] value: Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SessionParameterState.__new__(_SessionParameterState)

        __props__.__dict__["key"] = key
        __props__.__dict__["on_account"] = on_account
        __props__.__dict__["user"] = user
        __props__.__dict__["value"] = value
        return SessionParameter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        Name of session parameter. Valid values are those in [session parameters](https://docs.snowflake.com/en/sql-reference/parameters.html#session-parameters).
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="onAccount")
    def on_account(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, the session parameter will be set on the account level.
        """
        return pulumi.get(self, "on_account")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[Optional[str]]:
        """
        The user to set the session parameter for. Required if on_account is false
        """
        return pulumi.get(self, "user")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[str]:
        """
        Value of session parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation.
        """
        return pulumi.get(self, "value")

