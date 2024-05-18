# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetTlsPrivateKeyIdsResult',
    'AwaitableGetTlsPrivateKeyIdsResult',
    'get_tls_private_key_ids',
    'get_tls_private_key_ids_output',
]

@pulumi.output_type
class GetTlsPrivateKeyIdsResult:
    """
    A collection of values returned by getTlsPrivateKeyIds.
    """
    def __init__(__self__, id=None, ids=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        List of IDs of the TLS private keys.
        """
        return pulumi.get(self, "ids")


class AwaitableGetTlsPrivateKeyIdsResult(GetTlsPrivateKeyIdsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTlsPrivateKeyIdsResult(
            id=self.id,
            ids=self.ids)


def get_tls_private_key_ids(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTlsPrivateKeyIdsResult:
    """
    Use this data source to get the list of TLS private key identifiers in Fastly.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    demo = fastly.get_tls_private_key_ids()
    example = fastly.get_tls_private_key(id=demo_fastly_tls_private_key_ids["ids"])
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fastly:index/getTlsPrivateKeyIds:getTlsPrivateKeyIds', __args__, opts=opts, typ=GetTlsPrivateKeyIdsResult).value

    return AwaitableGetTlsPrivateKeyIdsResult(
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'))


@_utilities.lift_output_func(get_tls_private_key_ids)
def get_tls_private_key_ids_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTlsPrivateKeyIdsResult]:
    """
    Use this data source to get the list of TLS private key identifiers in Fastly.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fastly as fastly

    demo = fastly.get_tls_private_key_ids()
    example = fastly.get_tls_private_key(id=demo_fastly_tls_private_key_ids["ids"])
    ```
    """
    ...
