# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['NetworkPolicyArgs', 'NetworkPolicy']

@pulumi.input_type
class NetworkPolicyArgs:
    def __init__(__self__, *,
                 allowed_ip_lists: pulumi.Input[Sequence[pulumi.Input[str]]],
                 blocked_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NetworkPolicy resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        :param pulumi.Input[str] comment: Specifies a comment for the network policy.
        :param pulumi.Input[str] name: Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        pulumi.set(__self__, "allowed_ip_lists", allowed_ip_lists)
        if blocked_ip_lists is not None:
            pulumi.set(__self__, "blocked_ip_lists", blocked_ip_lists)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="allowedIpLists")
    def allowed_ip_lists(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        """
        return pulumi.get(self, "allowed_ip_lists")

    @allowed_ip_lists.setter
    def allowed_ip_lists(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_ip_lists", value)

    @property
    @pulumi.getter(name="blockedIpLists")
    def blocked_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        """
        return pulumi.get(self, "blocked_ip_lists")

    @blocked_ip_lists.setter
    def blocked_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "blocked_ip_lists", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the network policy.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _NetworkPolicyState:
    def __init__(__self__, *,
                 allowed_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkPolicy resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        :param pulumi.Input[str] comment: Specifies a comment for the network policy.
        :param pulumi.Input[str] name: Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        if allowed_ip_lists is not None:
            pulumi.set(__self__, "allowed_ip_lists", allowed_ip_lists)
        if blocked_ip_lists is not None:
            pulumi.set(__self__, "blocked_ip_lists", blocked_ip_lists)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="allowedIpLists")
    def allowed_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        """
        return pulumi.get(self, "allowed_ip_lists")

    @allowed_ip_lists.setter
    def allowed_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_ip_lists", value)

    @property
    @pulumi.getter(name="blockedIpLists")
    def blocked_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        """
        return pulumi.get(self, "blocked_ip_lists")

    @blocked_ip_lists.setter
    def blocked_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "blocked_ip_lists", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the network policy.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class NetworkPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        policy = snowflake.NetworkPolicy("policy",
            name="policy",
            comment="A policy.",
            allowed_ip_lists=["192.168.0.100/24"],
            blocked_ip_lists=["192.168.0.101"])
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/networkPolicy:NetworkPolicy example policyname
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        :param pulumi.Input[str] comment: Specifies a comment for the network policy.
        :param pulumi.Input[str] name: Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        policy = snowflake.NetworkPolicy("policy",
            name="policy",
            comment="A policy.",
            allowed_ip_lists=["192.168.0.100/24"],
            blocked_ip_lists=["192.168.0.101"])
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/networkPolicy:NetworkPolicy example policyname
        ```

        :param str resource_name: The name of the resource.
        :param NetworkPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 blocked_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkPolicyArgs.__new__(NetworkPolicyArgs)

            if allowed_ip_lists is None and not opts.urn:
                raise TypeError("Missing required property 'allowed_ip_lists'")
            __props__.__dict__["allowed_ip_lists"] = allowed_ip_lists
            __props__.__dict__["blocked_ip_lists"] = blocked_ip_lists
            __props__.__dict__["comment"] = comment
            __props__.__dict__["name"] = name
        super(NetworkPolicy, __self__).__init__(
            'snowflake:index/networkPolicy:NetworkPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allowed_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            blocked_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'NetworkPolicy':
        """
        Get an existing NetworkPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        :param pulumi.Input[Sequence[pulumi.Input[str]]] blocked_ip_lists: Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        :param pulumi.Input[str] comment: Specifies a comment for the network policy.
        :param pulumi.Input[str] name: Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkPolicyState.__new__(_NetworkPolicyState)

        __props__.__dict__["allowed_ip_lists"] = allowed_ip_lists
        __props__.__dict__["blocked_ip_lists"] = blocked_ip_lists
        __props__.__dict__["comment"] = comment
        __props__.__dict__["name"] = name
        return NetworkPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedIpLists")
    def allowed_ip_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are allowed access to your Snowflake account
        """
        return pulumi.get(self, "allowed_ip_lists")

    @property
    @pulumi.getter(name="blockedIpLists")
    def blocked_ip_lists(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies one or more IPv4 addresses (CIDR notation) that are denied access to your Snowflake account\\n\\n\\n\\n**Do not** add `0.0.0.0/0` to `blocked_ip_list`
        """
        return pulumi.get(self, "blocked_ip_lists")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the network policy.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the identifier for the network policy; must be unique for the account in which the network policy is created.
        """
        return pulumi.get(self, "name")

