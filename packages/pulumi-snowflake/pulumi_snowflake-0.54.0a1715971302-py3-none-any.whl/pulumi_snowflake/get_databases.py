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
    'GetDatabasesResult',
    'AwaitableGetDatabasesResult',
    'get_databases',
    'get_databases_output',
]

@pulumi.output_type
class GetDatabasesResult:
    """
    A collection of values returned by getDatabases.
    """
    def __init__(__self__, databases=None, history=None, id=None, pattern=None, starts_with=None, terse=None):
        if databases and not isinstance(databases, list):
            raise TypeError("Expected argument 'databases' to be a list")
        pulumi.set(__self__, "databases", databases)
        if history and not isinstance(history, bool):
            raise TypeError("Expected argument 'history' to be a bool")
        pulumi.set(__self__, "history", history)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if pattern and not isinstance(pattern, str):
            raise TypeError("Expected argument 'pattern' to be a str")
        pulumi.set(__self__, "pattern", pattern)
        if starts_with and not isinstance(starts_with, str):
            raise TypeError("Expected argument 'starts_with' to be a str")
        pulumi.set(__self__, "starts_with", starts_with)
        if terse and not isinstance(terse, bool):
            raise TypeError("Expected argument 'terse' to be a bool")
        pulumi.set(__self__, "terse", terse)

    @property
    @pulumi.getter
    def databases(self) -> Sequence['outputs.GetDatabasesDatabaseResult']:
        """
        Snowflake databases
        """
        return pulumi.get(self, "databases")

    @property
    @pulumi.getter
    def history(self) -> Optional[bool]:
        """
        Optionally includes dropped databases that have not yet been purged The output also includes an additional `dropped_on` column
        """
        return pulumi.get(self, "history")

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
        Optionally filters the databases by a pattern
        """
        return pulumi.get(self, "pattern")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[str]:
        """
        Optionally filters the databases by a pattern
        """
        return pulumi.get(self, "starts_with")

    @property
    @pulumi.getter
    def terse(self) -> Optional[bool]:
        """
        Optionally returns only the columns `created_on` and `name` in the results
        """
        return pulumi.get(self, "terse")


class AwaitableGetDatabasesResult(GetDatabasesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabasesResult(
            databases=self.databases,
            history=self.history,
            id=self.id,
            pattern=self.pattern,
            starts_with=self.starts_with,
            terse=self.terse)


def get_databases(history: Optional[bool] = None,
                  pattern: Optional[str] = None,
                  starts_with: Optional[str] = None,
                  terse: Optional[bool] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatabasesResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_databases()
    ```


    :param bool history: Optionally includes dropped databases that have not yet been purged The output also includes an additional `dropped_on` column
    :param str pattern: Optionally filters the databases by a pattern
    :param str starts_with: Optionally filters the databases by a pattern
    :param bool terse: Optionally returns only the columns `created_on` and `name` in the results
    """
    __args__ = dict()
    __args__['history'] = history
    __args__['pattern'] = pattern
    __args__['startsWith'] = starts_with
    __args__['terse'] = terse
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getDatabases:getDatabases', __args__, opts=opts, typ=GetDatabasesResult).value

    return AwaitableGetDatabasesResult(
        databases=pulumi.get(__ret__, 'databases'),
        history=pulumi.get(__ret__, 'history'),
        id=pulumi.get(__ret__, 'id'),
        pattern=pulumi.get(__ret__, 'pattern'),
        starts_with=pulumi.get(__ret__, 'starts_with'),
        terse=pulumi.get(__ret__, 'terse'))


@_utilities.lift_output_func(get_databases)
def get_databases_output(history: Optional[pulumi.Input[Optional[bool]]] = None,
                         pattern: Optional[pulumi.Input[Optional[str]]] = None,
                         starts_with: Optional[pulumi.Input[Optional[str]]] = None,
                         terse: Optional[pulumi.Input[Optional[bool]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDatabasesResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    this = snowflake.get_databases()
    ```


    :param bool history: Optionally includes dropped databases that have not yet been purged The output also includes an additional `dropped_on` column
    :param str pattern: Optionally filters the databases by a pattern
    :param str starts_with: Optionally filters the databases by a pattern
    :param bool terse: Optionally returns only the columns `created_on` and `name` in the results
    """
    ...
