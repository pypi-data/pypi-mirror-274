# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AdministrativeUnitMemberArgs', 'AdministrativeUnitMember']

@pulumi.input_type
class AdministrativeUnitMemberArgs:
    def __init__(__self__, *,
                 administrative_unit_object_id: Optional[pulumi.Input[str]] = None,
                 member_object_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AdministrativeUnitMember resource.
        :param pulumi.Input[str] administrative_unit_object_id: The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] member_object_id: The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        if administrative_unit_object_id is not None:
            pulumi.set(__self__, "administrative_unit_object_id", administrative_unit_object_id)
        if member_object_id is not None:
            pulumi.set(__self__, "member_object_id", member_object_id)

    @property
    @pulumi.getter(name="administrativeUnitObjectId")
    def administrative_unit_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "administrative_unit_object_id")

    @administrative_unit_object_id.setter
    def administrative_unit_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "administrative_unit_object_id", value)

    @property
    @pulumi.getter(name="memberObjectId")
    def member_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "member_object_id")

    @member_object_id.setter
    def member_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member_object_id", value)


@pulumi.input_type
class _AdministrativeUnitMemberState:
    def __init__(__self__, *,
                 administrative_unit_object_id: Optional[pulumi.Input[str]] = None,
                 member_object_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AdministrativeUnitMember resources.
        :param pulumi.Input[str] administrative_unit_object_id: The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] member_object_id: The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        if administrative_unit_object_id is not None:
            pulumi.set(__self__, "administrative_unit_object_id", administrative_unit_object_id)
        if member_object_id is not None:
            pulumi.set(__self__, "member_object_id", member_object_id)

    @property
    @pulumi.getter(name="administrativeUnitObjectId")
    def administrative_unit_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "administrative_unit_object_id")

    @administrative_unit_object_id.setter
    def administrative_unit_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "administrative_unit_object_id", value)

    @property
    @pulumi.getter(name="memberObjectId")
    def member_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "member_object_id")

    @member_object_id.setter
    def member_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member_object_id", value)


class AdministrativeUnitMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrative_unit_object_id: Optional[pulumi.Input[str]] = None,
                 member_object_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a single administrative unit membership within Azure Active Directory.

        > **Warning** Do not use this resource at the same time as the `members` property of the `AdministrativeUnit` resource for the same administrative unit. Doing so will cause a conflict and administrative unit members will be removed.

        ## API Permissions

        The following API permissions are required in order to use this resource.

        When authenticated with a service principal, this resource requires one of the following application roles: `AdministrativeUnit.ReadWrite.All` or `Directory.ReadWrite.All`

        When authenticated with a user principal, this resource requires one of the following directory roles: `Privileged Role Administrator` or `Global Administrator`

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azuread as azuread

        example = azuread.get_user(user_principal_name="jdoe@example.com")
        example_administrative_unit = azuread.AdministrativeUnit("example", display_name="Example-AU")
        example_administrative_unit_member = azuread.AdministrativeUnitMember("example",
            administrative_unit_object_id=example_administrative_unit.id,
            member_object_id=example.id)
        ```

        ## Import

        Administrative unit members can be imported using the object ID of the administrative unit and the object ID of the member, e.g.

        ```sh
        $ pulumi import azuread:index/administrativeUnitMember:AdministrativeUnitMember example 00000000-0000-0000-0000-000000000000/member/11111111-1111-1111-1111-111111111111
        ```

        -> This ID format is unique to Terraform and is composed of the Administrative Unit Object ID and the target Member Object ID in the format `{AdministrativeUnitObjectID}/member/{MemberObjectID}`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrative_unit_object_id: The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] member_object_id: The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AdministrativeUnitMemberArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a single administrative unit membership within Azure Active Directory.

        > **Warning** Do not use this resource at the same time as the `members` property of the `AdministrativeUnit` resource for the same administrative unit. Doing so will cause a conflict and administrative unit members will be removed.

        ## API Permissions

        The following API permissions are required in order to use this resource.

        When authenticated with a service principal, this resource requires one of the following application roles: `AdministrativeUnit.ReadWrite.All` or `Directory.ReadWrite.All`

        When authenticated with a user principal, this resource requires one of the following directory roles: `Privileged Role Administrator` or `Global Administrator`

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azuread as azuread

        example = azuread.get_user(user_principal_name="jdoe@example.com")
        example_administrative_unit = azuread.AdministrativeUnit("example", display_name="Example-AU")
        example_administrative_unit_member = azuread.AdministrativeUnitMember("example",
            administrative_unit_object_id=example_administrative_unit.id,
            member_object_id=example.id)
        ```

        ## Import

        Administrative unit members can be imported using the object ID of the administrative unit and the object ID of the member, e.g.

        ```sh
        $ pulumi import azuread:index/administrativeUnitMember:AdministrativeUnitMember example 00000000-0000-0000-0000-000000000000/member/11111111-1111-1111-1111-111111111111
        ```

        -> This ID format is unique to Terraform and is composed of the Administrative Unit Object ID and the target Member Object ID in the format `{AdministrativeUnitObjectID}/member/{MemberObjectID}`.

        :param str resource_name: The name of the resource.
        :param AdministrativeUnitMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AdministrativeUnitMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrative_unit_object_id: Optional[pulumi.Input[str]] = None,
                 member_object_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AdministrativeUnitMemberArgs.__new__(AdministrativeUnitMemberArgs)

            __props__.__dict__["administrative_unit_object_id"] = administrative_unit_object_id
            __props__.__dict__["member_object_id"] = member_object_id
        super(AdministrativeUnitMember, __self__).__init__(
            'azuread:index/administrativeUnitMember:AdministrativeUnitMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            administrative_unit_object_id: Optional[pulumi.Input[str]] = None,
            member_object_id: Optional[pulumi.Input[str]] = None) -> 'AdministrativeUnitMember':
        """
        Get an existing AdministrativeUnitMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrative_unit_object_id: The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] member_object_id: The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AdministrativeUnitMemberState.__new__(_AdministrativeUnitMemberState)

        __props__.__dict__["administrative_unit_object_id"] = administrative_unit_object_id
        __props__.__dict__["member_object_id"] = member_object_id
        return AdministrativeUnitMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administrativeUnitObjectId")
    def administrative_unit_object_id(self) -> pulumi.Output[Optional[str]]:
        """
        The object ID of the administrative unit you want to add the member to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "administrative_unit_object_id")

    @property
    @pulumi.getter(name="memberObjectId")
    def member_object_id(self) -> pulumi.Output[Optional[str]]:
        """
        The object ID of the user or group you want to add as a member of the administrative unit. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "member_object_id")

