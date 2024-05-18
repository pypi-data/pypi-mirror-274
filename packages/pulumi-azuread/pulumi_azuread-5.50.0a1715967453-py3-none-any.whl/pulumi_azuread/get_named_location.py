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
    'GetNamedLocationResult',
    'AwaitableGetNamedLocationResult',
    'get_named_location',
    'get_named_location_output',
]

@pulumi.output_type
class GetNamedLocationResult:
    """
    A collection of values returned by getNamedLocation.
    """
    def __init__(__self__, countries=None, display_name=None, id=None, ips=None):
        if countries and not isinstance(countries, list):
            raise TypeError("Expected argument 'countries' to be a list")
        pulumi.set(__self__, "countries", countries)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ips and not isinstance(ips, list):
            raise TypeError("Expected argument 'ips' to be a list")
        pulumi.set(__self__, "ips", ips)

    @property
    @pulumi.getter
    def countries(self) -> Sequence['outputs.GetNamedLocationCountryResult']:
        return pulumi.get(self, "countries")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ips(self) -> Sequence['outputs.GetNamedLocationIpResult']:
        return pulumi.get(self, "ips")


class AwaitableGetNamedLocationResult(GetNamedLocationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamedLocationResult(
            countries=self.countries,
            display_name=self.display_name,
            id=self.id,
            ips=self.ips)


def get_named_location(display_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamedLocationResult:
    """
    Gets information about a Named Location within Azure Active Directory.

    ## API Permissions

    The following API permissions are required in order to use this data source.

    When authenticated with a service principal, this resource requires the following application roles: `Policy.Read.All`

    When authenticated with a user principal, this resource requires one of the following directory roles: `Conditional Access Administrator` or `Global Reader`

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_named_location(display_name="My Named Location")
    ```

    ## Attributes Reference

    The following attributes are exported:

    * `country` - A `country` block as documented below, which describes a country-based named location.
    * `id` - The ID of the named location.
    * `ip` - An `ip` block as documented below, which describes an IP-based named location.
    * 
    ***

    `country` block exports the following:

    * `countries_and_regions` - List of countries and/or regions in two-letter format specified by ISO 3166-2.
    * `include_unknown_countries_and_regions` - Whether IP addresses that don't map to a country or region are included in the named location.

    ***

    `ip` block exports the following:

    * `ip_ranges` - List of IP address ranges in IPv4 CIDR format (e.g. `1.2.3.4/32`) or any allowable IPv6 format from IETF RFC596.
    * `trusted` - Whether the named location is trusted.


    :param str display_name: Specifies the display named of the named location to look up.
    """
    __args__ = dict()
    __args__['displayName'] = display_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azuread:index/getNamedLocation:getNamedLocation', __args__, opts=opts, typ=GetNamedLocationResult).value

    return AwaitableGetNamedLocationResult(
        countries=pulumi.get(__ret__, 'countries'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        ips=pulumi.get(__ret__, 'ips'))


@_utilities.lift_output_func(get_named_location)
def get_named_location_output(display_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNamedLocationResult]:
    """
    Gets information about a Named Location within Azure Active Directory.

    ## API Permissions

    The following API permissions are required in order to use this data source.

    When authenticated with a service principal, this resource requires the following application roles: `Policy.Read.All`

    When authenticated with a user principal, this resource requires one of the following directory roles: `Conditional Access Administrator` or `Global Reader`

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_named_location(display_name="My Named Location")
    ```

    ## Attributes Reference

    The following attributes are exported:

    * `country` - A `country` block as documented below, which describes a country-based named location.
    * `id` - The ID of the named location.
    * `ip` - An `ip` block as documented below, which describes an IP-based named location.
    * 
    ***

    `country` block exports the following:

    * `countries_and_regions` - List of countries and/or regions in two-letter format specified by ISO 3166-2.
    * `include_unknown_countries_and_regions` - Whether IP addresses that don't map to a country or region are included in the named location.

    ***

    `ip` block exports the following:

    * `ip_ranges` - List of IP address ranges in IPv4 CIDR format (e.g. `1.2.3.4/32`) or any allowable IPv6 format from IETF RFC596.
    * `trusted` - Whether the named location is trusted.


    :param str display_name: Specifies the display named of the named location to look up.
    """
    ...
