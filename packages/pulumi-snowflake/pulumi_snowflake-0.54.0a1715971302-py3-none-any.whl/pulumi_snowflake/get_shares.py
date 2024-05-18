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

__all__ = [
    'GetSharesResult',
    'AwaitableGetSharesResult',
    'get_shares',
    'get_shares_output',
]

@pulumi.output_type
class GetSharesResult:
    """
    A collection of values returned by getShares.
    """
    def __init__(__self__, id=None, pattern=None, shares=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if pattern and not isinstance(pattern, str):
            raise TypeError("Expected argument 'pattern' to be a str")
        pulumi.set(__self__, "pattern", pattern)
        if shares and not isinstance(shares, list):
            raise TypeError("Expected argument 'shares' to be a list")
        pulumi.set(__self__, "shares", shares)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def pattern(self) -> Optional[str]:
        """
        Filters the command output by object name.
        """
        return pulumi.get(self, "pattern")

    @property
    @pulumi.getter
    def shares(self) -> Sequence['outputs.GetSharesShareResult']:
        """
        List of all the shares available in the system.
        """
        return pulumi.get(self, "shares")


class AwaitableGetSharesResult(GetSharesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharesResult(
            id=self.id,
            pattern=self.pattern,
            shares=self.shares)


def get_shares(pattern: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharesResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_shares()
    ad = snowflake.get_shares(pattern="usage")
    ```


    :param str pattern: Filters the command output by object name.
    """
    __args__ = dict()
    __args__['pattern'] = pattern
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getShares:getShares', __args__, opts=opts, typ=GetSharesResult).value

    return AwaitableGetSharesResult(
        id=pulumi.get(__ret__, 'id'),
        pattern=pulumi.get(__ret__, 'pattern'),
        shares=pulumi.get(__ret__, 'shares'))


@_utilities.lift_output_func(get_shares)
def get_shares_output(pattern: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSharesResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_shares()
    ad = snowflake.get_shares(pattern="usage")
    ```


    :param str pattern: Filters the command output by object name.
    """
    ...
