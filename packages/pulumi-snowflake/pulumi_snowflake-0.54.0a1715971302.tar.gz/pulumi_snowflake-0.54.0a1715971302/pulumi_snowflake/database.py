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

__all__ = ['DatabaseArgs', 'Database']

@pulumi.input_type
class DatabaseArgs:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_retention_time_in_days: Optional[pulumi.Input[int]] = None,
                 from_database: Optional[pulumi.Input[str]] = None,
                 from_replica: Optional[pulumi.Input[str]] = None,
                 from_share: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 is_transient: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 replication_configuration: Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']] = None):
        """
        The set of arguments for constructing a Database resource.
        :param pulumi.Input[str] comment: Specifies a comment for the database.
        :param pulumi.Input[int] data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        :param pulumi.Input[str] from_database: Specify a database to create a clone from.
        :param pulumi.Input[str] from_replica: Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] from_share: Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        :param pulumi.Input[bool] is_transient: Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        :param pulumi.Input[str] name: Specifies the identifier for the database; must be unique for your account.
        :param pulumi.Input['DatabaseReplicationConfigurationArgs'] replication_configuration: When set, specifies the configurations for database replication.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if data_retention_time_in_days is not None:
            pulumi.set(__self__, "data_retention_time_in_days", data_retention_time_in_days)
        if from_database is not None:
            pulumi.set(__self__, "from_database", from_database)
        if from_replica is not None:
            pulumi.set(__self__, "from_replica", from_replica)
        if from_share is not None:
            pulumi.set(__self__, "from_share", from_share)
        if is_transient is not None:
            pulumi.set(__self__, "is_transient", is_transient)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if replication_configuration is not None:
            pulumi.set(__self__, "replication_configuration", replication_configuration)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the database.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        """
        return pulumi.get(self, "data_retention_time_in_days")

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "data_retention_time_in_days", value)

    @property
    @pulumi.getter(name="fromDatabase")
    def from_database(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a database to create a clone from.
        """
        return pulumi.get(self, "from_database")

    @from_database.setter
    def from_database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_database", value)

    @property
    @pulumi.getter(name="fromReplica")
    def from_replica(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        """
        return pulumi.get(self, "from_replica")

    @from_replica.setter
    def from_replica(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_replica", value)

    @property
    @pulumi.getter(name="fromShare")
    def from_share(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        """
        return pulumi.get(self, "from_share")

    @from_share.setter
    def from_share(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "from_share", value)

    @property
    @pulumi.getter(name="isTransient")
    def is_transient(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        """
        return pulumi.get(self, "is_transient")

    @is_transient.setter
    def is_transient(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_transient", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the database; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="replicationConfiguration")
    def replication_configuration(self) -> Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']]:
        """
        When set, specifies the configurations for database replication.
        """
        return pulumi.get(self, "replication_configuration")

    @replication_configuration.setter
    def replication_configuration(self, value: Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']]):
        pulumi.set(self, "replication_configuration", value)


@pulumi.input_type
class _DatabaseState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_retention_time_in_days: Optional[pulumi.Input[int]] = None,
                 from_database: Optional[pulumi.Input[str]] = None,
                 from_replica: Optional[pulumi.Input[str]] = None,
                 from_share: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 is_transient: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 replication_configuration: Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering Database resources.
        :param pulumi.Input[str] comment: Specifies a comment for the database.
        :param pulumi.Input[int] data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        :param pulumi.Input[str] from_database: Specify a database to create a clone from.
        :param pulumi.Input[str] from_replica: Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] from_share: Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        :param pulumi.Input[bool] is_transient: Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        :param pulumi.Input[str] name: Specifies the identifier for the database; must be unique for your account.
        :param pulumi.Input['DatabaseReplicationConfigurationArgs'] replication_configuration: When set, specifies the configurations for database replication.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if data_retention_time_in_days is not None:
            pulumi.set(__self__, "data_retention_time_in_days", data_retention_time_in_days)
        if from_database is not None:
            pulumi.set(__self__, "from_database", from_database)
        if from_replica is not None:
            pulumi.set(__self__, "from_replica", from_replica)
        if from_share is not None:
            pulumi.set(__self__, "from_share", from_share)
        if is_transient is not None:
            pulumi.set(__self__, "is_transient", is_transient)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if replication_configuration is not None:
            pulumi.set(__self__, "replication_configuration", replication_configuration)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the database.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        """
        return pulumi.get(self, "data_retention_time_in_days")

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "data_retention_time_in_days", value)

    @property
    @pulumi.getter(name="fromDatabase")
    def from_database(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a database to create a clone from.
        """
        return pulumi.get(self, "from_database")

    @from_database.setter
    def from_database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_database", value)

    @property
    @pulumi.getter(name="fromReplica")
    def from_replica(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        """
        return pulumi.get(self, "from_replica")

    @from_replica.setter
    def from_replica(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_replica", value)

    @property
    @pulumi.getter(name="fromShare")
    def from_share(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        """
        return pulumi.get(self, "from_share")

    @from_share.setter
    def from_share(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "from_share", value)

    @property
    @pulumi.getter(name="isTransient")
    def is_transient(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        """
        return pulumi.get(self, "is_transient")

    @is_transient.setter
    def is_transient(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_transient", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the database; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="replicationConfiguration")
    def replication_configuration(self) -> Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']]:
        """
        When set, specifies the configurations for database replication.
        """
        return pulumi.get(self, "replication_configuration")

    @replication_configuration.setter
    def replication_configuration(self, value: Optional[pulumi.Input['DatabaseReplicationConfigurationArgs']]):
        pulumi.set(self, "replication_configuration", value)


class Database(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_retention_time_in_days: Optional[pulumi.Input[int]] = None,
                 from_database: Optional[pulumi.Input[str]] = None,
                 from_replica: Optional[pulumi.Input[str]] = None,
                 from_share: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 is_transient: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 replication_configuration: Optional[pulumi.Input[pulumi.InputType['DatabaseReplicationConfigurationArgs']]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        simple = snowflake.Database("simple",
            name="testing",
            comment="test comment",
            data_retention_time_in_days=3)
        with_replication = snowflake.Database("with_replication",
            name="testing_2",
            comment="test comment 2",
            replication_configuration=snowflake.DatabaseReplicationConfigurationArgs(
                accounts=[
                    "test_account1",
                    "test_account_2",
                ],
                ignore_edition_check=True,
            ))
        from_replica = snowflake.Database("from_replica",
            name="testing_3",
            comment="test comment",
            data_retention_time_in_days=3,
            from_replica="\\"org1\\".\\"account1\\".\\"primary_db_name\\"")
        from_share = snowflake.Database("from_share",
            name="testing_4",
            comment="test comment",
            from_share={
                "provider": "account1_locator",
                "share": "share1",
            })
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/database:Database example name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: Specifies a comment for the database.
        :param pulumi.Input[int] data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        :param pulumi.Input[str] from_database: Specify a database to create a clone from.
        :param pulumi.Input[str] from_replica: Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] from_share: Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        :param pulumi.Input[bool] is_transient: Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        :param pulumi.Input[str] name: Specifies the identifier for the database; must be unique for your account.
        :param pulumi.Input[pulumi.InputType['DatabaseReplicationConfigurationArgs']] replication_configuration: When set, specifies the configurations for database replication.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DatabaseArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_snowflake as snowflake

        simple = snowflake.Database("simple",
            name="testing",
            comment="test comment",
            data_retention_time_in_days=3)
        with_replication = snowflake.Database("with_replication",
            name="testing_2",
            comment="test comment 2",
            replication_configuration=snowflake.DatabaseReplicationConfigurationArgs(
                accounts=[
                    "test_account1",
                    "test_account_2",
                ],
                ignore_edition_check=True,
            ))
        from_replica = snowflake.Database("from_replica",
            name="testing_3",
            comment="test comment",
            data_retention_time_in_days=3,
            from_replica="\\"org1\\".\\"account1\\".\\"primary_db_name\\"")
        from_share = snowflake.Database("from_share",
            name="testing_4",
            comment="test comment",
            from_share={
                "provider": "account1_locator",
                "share": "share1",
            })
        ```

        ## Import

        ```sh
        $ pulumi import snowflake:index/database:Database example name
        ```

        :param str resource_name: The name of the resource.
        :param DatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_retention_time_in_days: Optional[pulumi.Input[int]] = None,
                 from_database: Optional[pulumi.Input[str]] = None,
                 from_replica: Optional[pulumi.Input[str]] = None,
                 from_share: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 is_transient: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 replication_configuration: Optional[pulumi.Input[pulumi.InputType['DatabaseReplicationConfigurationArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseArgs.__new__(DatabaseArgs)

            __props__.__dict__["comment"] = comment
            __props__.__dict__["data_retention_time_in_days"] = data_retention_time_in_days
            __props__.__dict__["from_database"] = from_database
            __props__.__dict__["from_replica"] = from_replica
            __props__.__dict__["from_share"] = from_share
            __props__.__dict__["is_transient"] = is_transient
            __props__.__dict__["name"] = name
            __props__.__dict__["replication_configuration"] = replication_configuration
        super(Database, __self__).__init__(
            'snowflake:index/database:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            data_retention_time_in_days: Optional[pulumi.Input[int]] = None,
            from_database: Optional[pulumi.Input[str]] = None,
            from_replica: Optional[pulumi.Input[str]] = None,
            from_share: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            is_transient: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            replication_configuration: Optional[pulumi.Input[pulumi.InputType['DatabaseReplicationConfigurationArgs']]] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: Specifies a comment for the database.
        :param pulumi.Input[int] data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        :param pulumi.Input[str] from_database: Specify a database to create a clone from.
        :param pulumi.Input[str] from_replica: Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] from_share: Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        :param pulumi.Input[bool] is_transient: Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        :param pulumi.Input[str] name: Specifies the identifier for the database; must be unique for your account.
        :param pulumi.Input[pulumi.InputType['DatabaseReplicationConfigurationArgs']] replication_configuration: When set, specifies the configurations for database replication.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DatabaseState.__new__(_DatabaseState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["data_retention_time_in_days"] = data_retention_time_in_days
        __props__.__dict__["from_database"] = from_database
        __props__.__dict__["from_replica"] = from_replica
        __props__.__dict__["from_share"] = from_share
        __props__.__dict__["is_transient"] = is_transient
        __props__.__dict__["name"] = name
        __props__.__dict__["replication_configuration"] = replication_configuration
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the database.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database. Default value for this field is set to -1, which is a fallback to use Snowflake default. For more information, see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel).
        """
        return pulumi.get(self, "data_retention_time_in_days")

    @property
    @pulumi.getter(name="fromDatabase")
    def from_database(self) -> pulumi.Output[Optional[str]]:
        """
        Specify a database to create a clone from.
        """
        return pulumi.get(self, "from_database")

    @property
    @pulumi.getter(name="fromReplica")
    def from_replica(self) -> pulumi.Output[Optional[str]]:
        """
        Specify a fully-qualified path to a database to create a replica from. A fully qualified path follows the format of `"<organization_name>"."<account_name>"."<db_name>"`. An example would be: `"myorg1"."account1"."db1"`
        """
        return pulumi.get(self, "from_replica")

    @property
    @pulumi.getter(name="fromShare")
    def from_share(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Specify a provider and a share in this map to create a database from a share. As of version 0.87.0, the provider field is the account locator.
        """
        return pulumi.get(self, "from_share")

    @property
    @pulumi.getter(name="isTransient")
    def is_transient(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.
        """
        return pulumi.get(self, "is_transient")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the identifier for the database; must be unique for your account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="replicationConfiguration")
    def replication_configuration(self) -> pulumi.Output[Optional['outputs.DatabaseReplicationConfiguration']]:
        """
        When set, specifies the configurations for database replication.
        """
        return pulumi.get(self, "replication_configuration")

