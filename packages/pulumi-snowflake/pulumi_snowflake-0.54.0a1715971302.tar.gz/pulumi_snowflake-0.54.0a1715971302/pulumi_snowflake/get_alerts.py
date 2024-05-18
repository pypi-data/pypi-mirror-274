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
    'GetAlertsResult',
    'AwaitableGetAlertsResult',
    'get_alerts',
    'get_alerts_output',
]

@pulumi.output_type
class GetAlertsResult:
    """
    A collection of values returned by getAlerts.
    """
    def __init__(__self__, alerts=None, database=None, id=None, pattern=None, schema=None):
        if alerts and not isinstance(alerts, list):
            raise TypeError("Expected argument 'alerts' to be a list")
        pulumi.set(__self__, "alerts", alerts)
        if database and not isinstance(database, str):
            raise TypeError("Expected argument 'database' to be a str")
        pulumi.set(__self__, "database", database)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if pattern and not isinstance(pattern, str):
            raise TypeError("Expected argument 'pattern' to be a str")
        pulumi.set(__self__, "pattern", pattern)
        if schema and not isinstance(schema, str):
            raise TypeError("Expected argument 'schema' to be a str")
        pulumi.set(__self__, "schema", schema)

    @property
    @pulumi.getter
    def alerts(self) -> Sequence['outputs.GetAlertsAlertResult']:
        """
        Lists alerts for the current/specified database or schema, or across the entire account.
        """
        return pulumi.get(self, "alerts")

    @property
    @pulumi.getter
    def database(self) -> Optional[str]:
        """
        The database from which to return the alerts from.
        """
        return pulumi.get(self, "database")

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
    def schema(self) -> Optional[str]:
        """
        The schema from which to return the alerts from.
        """
        return pulumi.get(self, "schema")


class AwaitableGetAlertsResult(GetAlertsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAlertsResult(
            alerts=self.alerts,
            database=self.database,
            id=self.id,
            pattern=self.pattern,
            schema=self.schema)


def get_alerts(database: Optional[str] = None,
               pattern: Optional[str] = None,
               schema: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAlertsResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_alerts(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the alerts from.
    :param str pattern: Filters the command output by object name.
    :param str schema: The schema from which to return the alerts from.
    """
    __args__ = dict()
    __args__['database'] = database
    __args__['pattern'] = pattern
    __args__['schema'] = schema
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getAlerts:getAlerts', __args__, opts=opts, typ=GetAlertsResult).value

    return AwaitableGetAlertsResult(
        alerts=pulumi.get(__ret__, 'alerts'),
        database=pulumi.get(__ret__, 'database'),
        id=pulumi.get(__ret__, 'id'),
        pattern=pulumi.get(__ret__, 'pattern'),
        schema=pulumi.get(__ret__, 'schema'))


@_utilities.lift_output_func(get_alerts)
def get_alerts_output(database: Optional[pulumi.Input[Optional[str]]] = None,
                      pattern: Optional[pulumi.Input[Optional[str]]] = None,
                      schema: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAlertsResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_alerts(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the alerts from.
    :param str pattern: Filters the command output by object name.
    :param str schema: The schema from which to return the alerts from.
    """
    ...
