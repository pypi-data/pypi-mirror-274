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
    'GetSecretstoresResult',
    'AwaitableGetSecretstoresResult',
    'get_secretstores',
    'get_secretstores_output',
]

@pulumi.output_type
class GetSecretstoresResult:
    """
    A collection of values returned by getSecretstores.
    """
    def __init__(__self__, id=None, stores=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if stores and not isinstance(stores, list):
            raise TypeError("Expected argument 'stores' to be a list")
        pulumi.set(__self__, "stores", stores)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def stores(self) -> Sequence['outputs.GetSecretstoresStoreResult']:
        """
        List of all Secrets Stores.
        """
        return pulumi.get(self, "stores")


class AwaitableGetSecretstoresResult(GetSecretstoresResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecretstoresResult(
            id=self.id,
            stores=self.stores)


def get_secretstores(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecretstoresResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fastly:index/getSecretstores:getSecretstores', __args__, opts=opts, typ=GetSecretstoresResult).value

    return AwaitableGetSecretstoresResult(
        id=pulumi.get(__ret__, 'id'),
        stores=pulumi.get(__ret__, 'stores'))


@_utilities.lift_output_func(get_secretstores)
def get_secretstores_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecretstoresResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
