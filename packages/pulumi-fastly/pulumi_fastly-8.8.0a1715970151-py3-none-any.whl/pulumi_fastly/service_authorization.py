# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ServiceAuthorizationArgs', 'ServiceAuthorization']

@pulumi.input_type
class ServiceAuthorizationArgs:
    def __init__(__self__, *,
                 permission: pulumi.Input[str],
                 service_id: pulumi.Input[str],
                 user_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ServiceAuthorization resource.
        :param pulumi.Input[str] permission: The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        :param pulumi.Input[str] service_id: The ID of the service to grant permissions for.
        :param pulumi.Input[str] user_id: The ID of the user which will receive the granted permissions.
        """
        pulumi.set(__self__, "permission", permission)
        pulumi.set(__self__, "service_id", service_id)
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Input[str]:
        """
        The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: pulumi.Input[str]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Input[str]:
        """
        The ID of the service to grant permissions for.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        The ID of the user which will receive the granted permissions.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)


@pulumi.input_type
class _ServiceAuthorizationState:
    def __init__(__self__, *,
                 permission: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceAuthorization resources.
        :param pulumi.Input[str] permission: The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        :param pulumi.Input[str] service_id: The ID of the service to grant permissions for.
        :param pulumi.Input[str] user_id: The ID of the user which will receive the granted permissions.
        """
        if permission is not None:
            pulumi.set(__self__, "permission", permission)
        if service_id is not None:
            pulumi.set(__self__, "service_id", service_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def permission(self) -> Optional[pulumi.Input[str]]:
        """
        The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the service to grant permissions for.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the user which will receive the granted permissions.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class ServiceAuthorization(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Configures authorization with granular permissions to services. Users can be granted rights for services on different levels.

        The Service Authorization resource requires a user id, service id and an optional permission.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_fastly as fastly

        demo = fastly.ServiceVcl("demo")
        user = fastly.User("user")
        auth = fastly.ServiceAuthorization("auth",
            service_id=demo.id,
            user_id=user.id,
            permission="purge_all")
        ```

        ## Import

        A Fastly Service Authorization can be imported using their user ID, e.g.

        ```sh
        $ pulumi import fastly:index/serviceAuthorization:ServiceAuthorization demo xxxxxxxxxxxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] permission: The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        :param pulumi.Input[str] service_id: The ID of the service to grant permissions for.
        :param pulumi.Input[str] user_id: The ID of the user which will receive the granted permissions.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceAuthorizationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Configures authorization with granular permissions to services. Users can be granted rights for services on different levels.

        The Service Authorization resource requires a user id, service id and an optional permission.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_fastly as fastly

        demo = fastly.ServiceVcl("demo")
        user = fastly.User("user")
        auth = fastly.ServiceAuthorization("auth",
            service_id=demo.id,
            user_id=user.id,
            permission="purge_all")
        ```

        ## Import

        A Fastly Service Authorization can be imported using their user ID, e.g.

        ```sh
        $ pulumi import fastly:index/serviceAuthorization:ServiceAuthorization demo xxxxxxxxxxxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param ServiceAuthorizationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceAuthorizationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceAuthorizationArgs.__new__(ServiceAuthorizationArgs)

            if permission is None and not opts.urn:
                raise TypeError("Missing required property 'permission'")
            __props__.__dict__["permission"] = permission
            if service_id is None and not opts.urn:
                raise TypeError("Missing required property 'service_id'")
            __props__.__dict__["service_id"] = service_id
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
        super(ServiceAuthorization, __self__).__init__(
            'fastly:index/serviceAuthorization:ServiceAuthorization',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            permission: Optional[pulumi.Input[str]] = None,
            service_id: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'ServiceAuthorization':
        """
        Get an existing ServiceAuthorization resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] permission: The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        :param pulumi.Input[str] service_id: The ID of the service to grant permissions for.
        :param pulumi.Input[str] user_id: The ID of the user which will receive the granted permissions.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceAuthorizationState.__new__(_ServiceAuthorizationState)

        __props__.__dict__["permission"] = permission
        __props__.__dict__["service_id"] = service_id
        __props__.__dict__["user_id"] = user_id
        return ServiceAuthorization(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Output[str]:
        """
        The permissions to grant the user. Can be `full`, `read_only`, `purge_select` or `purge_all`.
        """
        return pulumi.get(self, "permission")

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Output[str]:
        """
        The ID of the service to grant permissions for.
        """
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        The ID of the user which will receive the granted permissions.
        """
        return pulumi.get(self, "user_id")

