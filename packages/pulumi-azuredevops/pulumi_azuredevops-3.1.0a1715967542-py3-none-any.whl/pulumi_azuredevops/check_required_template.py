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

__all__ = ['CheckRequiredTemplateArgs', 'CheckRequiredTemplate']

@pulumi.input_type
class CheckRequiredTemplateArgs:
    def __init__(__self__, *,
                 project_id: pulumi.Input[str],
                 required_templates: pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]],
                 target_resource_id: pulumi.Input[str],
                 target_resource_type: pulumi.Input[str]):
        """
        The set of arguments for constructing a CheckRequiredTemplate resource.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]] required_templates: One or more `required_template` blocks documented below.
        :param pulumi.Input[str] target_resource_id: The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[str] target_resource_type: The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        """
        pulumi.set(__self__, "project_id", project_id)
        pulumi.set(__self__, "required_templates", required_templates)
        pulumi.set(__self__, "target_resource_id", target_resource_id)
        pulumi.set(__self__, "target_resource_type", target_resource_type)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        The project ID. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="requiredTemplates")
    def required_templates(self) -> pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]]:
        """
        One or more `required_template` blocks documented below.
        """
        return pulumi.get(self, "required_templates")

    @required_templates.setter
    def required_templates(self, value: pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]]):
        pulumi.set(self, "required_templates", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Input[str]:
        """
        The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_resource_id", value)

    @property
    @pulumi.getter(name="targetResourceType")
    def target_resource_type(self) -> pulumi.Input[str]:
        """
        The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_type")

    @target_resource_type.setter
    def target_resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_resource_type", value)


@pulumi.input_type
class _CheckRequiredTemplateState:
    def __init__(__self__, *,
                 project_id: Optional[pulumi.Input[str]] = None,
                 required_templates: Optional[pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 target_resource_type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering CheckRequiredTemplate resources.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]] required_templates: One or more `required_template` blocks documented below.
        :param pulumi.Input[str] target_resource_id: The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[str] target_resource_type: The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[int] version: The version of the check.
        """
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if required_templates is not None:
            pulumi.set(__self__, "required_templates", required_templates)
        if target_resource_id is not None:
            pulumi.set(__self__, "target_resource_id", target_resource_id)
        if target_resource_type is not None:
            pulumi.set(__self__, "target_resource_type", target_resource_type)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        The project ID. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="requiredTemplates")
    def required_templates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]]]:
        """
        One or more `required_template` blocks documented below.
        """
        return pulumi.get(self, "required_templates")

    @required_templates.setter
    def required_templates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CheckRequiredTemplateRequiredTemplateArgs']]]]):
        pulumi.set(self, "required_templates", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_resource_id", value)

    @property
    @pulumi.getter(name="targetResourceType")
    def target_resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_type")

    @target_resource_type.setter
    def target_resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_resource_type", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        The version of the check.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


class CheckRequiredTemplate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 required_templates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CheckRequiredTemplateRequiredTemplateArgs']]]]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 target_resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Required Template Check.

        ## Example Usage

        ### Protect a service connection

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example", name="Example Project")
        example_service_endpoint_generic = azuredevops.ServiceEndpointGeneric("example",
            project_id=example.id,
            server_url="https://some-server.example.com",
            username="username",
            password="password",
            service_endpoint_name="Example Generic",
            description="Managed by Terraform")
        example_check_required_template = azuredevops.CheckRequiredTemplate("example",
            project_id=example.id,
            target_resource_id=example_service_endpoint_generic.id,
            target_resource_type="endpoint",
            required_templates=[azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                repository_type="azuregit",
                repository_name="project/repository",
                repository_ref="refs/heads/main",
                template_path="template/path.yml",
            )])
        ```

        ### Protect an environment

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example", name="Example Project")
        example_environment = azuredevops.Environment("example",
            project_id=example.id,
            name="Example Environment")
        example_check_required_template = azuredevops.CheckRequiredTemplate("example",
            project_id=example.id,
            target_resource_id=example_environment.id,
            target_resource_type="environment",
            required_templates=[
                azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                    repository_name="project/repository",
                    repository_ref="refs/heads/main",
                    template_path="template/path.yml",
                ),
                azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                    repository_name="project/repository",
                    repository_ref="refs/heads/main",
                    template_path="template/alternate-path.yml",
                ),
            ])
        ```

        ## Import

        Importing this resource is not supported.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CheckRequiredTemplateRequiredTemplateArgs']]]] required_templates: One or more `required_template` blocks documented below.
        :param pulumi.Input[str] target_resource_id: The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[str] target_resource_type: The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CheckRequiredTemplateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Required Template Check.

        ## Example Usage

        ### Protect a service connection

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example", name="Example Project")
        example_service_endpoint_generic = azuredevops.ServiceEndpointGeneric("example",
            project_id=example.id,
            server_url="https://some-server.example.com",
            username="username",
            password="password",
            service_endpoint_name="Example Generic",
            description="Managed by Terraform")
        example_check_required_template = azuredevops.CheckRequiredTemplate("example",
            project_id=example.id,
            target_resource_id=example_service_endpoint_generic.id,
            target_resource_type="endpoint",
            required_templates=[azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                repository_type="azuregit",
                repository_name="project/repository",
                repository_ref="refs/heads/main",
                template_path="template/path.yml",
            )])
        ```

        ### Protect an environment

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example", name="Example Project")
        example_environment = azuredevops.Environment("example",
            project_id=example.id,
            name="Example Environment")
        example_check_required_template = azuredevops.CheckRequiredTemplate("example",
            project_id=example.id,
            target_resource_id=example_environment.id,
            target_resource_type="environment",
            required_templates=[
                azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                    repository_name="project/repository",
                    repository_ref="refs/heads/main",
                    template_path="template/path.yml",
                ),
                azuredevops.CheckRequiredTemplateRequiredTemplateArgs(
                    repository_name="project/repository",
                    repository_ref="refs/heads/main",
                    template_path="template/alternate-path.yml",
                ),
            ])
        ```

        ## Import

        Importing this resource is not supported.

        :param str resource_name: The name of the resource.
        :param CheckRequiredTemplateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CheckRequiredTemplateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 required_templates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CheckRequiredTemplateRequiredTemplateArgs']]]]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 target_resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CheckRequiredTemplateArgs.__new__(CheckRequiredTemplateArgs)

            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            if required_templates is None and not opts.urn:
                raise TypeError("Missing required property 'required_templates'")
            __props__.__dict__["required_templates"] = required_templates
            if target_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_id'")
            __props__.__dict__["target_resource_id"] = target_resource_id
            if target_resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_type'")
            __props__.__dict__["target_resource_type"] = target_resource_type
            __props__.__dict__["version"] = None
        super(CheckRequiredTemplate, __self__).__init__(
            'azuredevops:index/checkRequiredTemplate:CheckRequiredTemplate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            required_templates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CheckRequiredTemplateRequiredTemplateArgs']]]]] = None,
            target_resource_id: Optional[pulumi.Input[str]] = None,
            target_resource_type: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'CheckRequiredTemplate':
        """
        Get an existing CheckRequiredTemplate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CheckRequiredTemplateRequiredTemplateArgs']]]] required_templates: One or more `required_template` blocks documented below.
        :param pulumi.Input[str] target_resource_id: The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[str] target_resource_type: The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        :param pulumi.Input[int] version: The version of the check.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CheckRequiredTemplateState.__new__(_CheckRequiredTemplateState)

        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["required_templates"] = required_templates
        __props__.__dict__["target_resource_id"] = target_resource_id
        __props__.__dict__["target_resource_type"] = target_resource_type
        __props__.__dict__["version"] = version
        return CheckRequiredTemplate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        The project ID. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="requiredTemplates")
    def required_templates(self) -> pulumi.Output[Sequence['outputs.CheckRequiredTemplateRequiredTemplate']]:
        """
        One or more `required_template` blocks documented below.
        """
        return pulumi.get(self, "required_templates")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource being protected by the check. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @property
    @pulumi.getter(name="targetResourceType")
    def target_resource_type(self) -> pulumi.Output[str]:
        """
        The type of resource being protected by the check. Valid values: `endpoint`, `environment`, `queue`, `repository`, `securefile`, `variablegroup`. Changing this forces a new Required Template Check to be created.
        """
        return pulumi.get(self, "target_resource_type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        The version of the check.
        """
        return pulumi.get(self, "version")

