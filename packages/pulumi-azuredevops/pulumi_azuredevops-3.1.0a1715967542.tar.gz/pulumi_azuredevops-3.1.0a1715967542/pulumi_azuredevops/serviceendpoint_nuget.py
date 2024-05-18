# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ServiceendpointNugetArgs', 'ServiceendpointNuget']

@pulumi.input_type
class ServiceendpointNugetArgs:
    def __init__(__self__, *,
                 feed_url: pulumi.Input[str],
                 project_id: pulumi.Input[str],
                 service_endpoint_name: pulumi.Input[str],
                 api_key: Optional[pulumi.Input[str]] = None,
                 authorization: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 personal_access_token: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceendpointNuget resource.
        :param pulumi.Input[str] feed_url: The URL for the feed. This will generally end with `index.json`.
        :param pulumi.Input[str] project_id: The ID of the project.
        :param pulumi.Input[str] service_endpoint_name: The Service Endpoint name.
        :param pulumi.Input[str] api_key: The API Key used to connect to the endpoint.
        :param pulumi.Input[str] password: The account password used to connect to the endpoint
               
               > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        :param pulumi.Input[str] personal_access_token: The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        :param pulumi.Input[str] username: The account username used to connect to the endpoint.
        """
        pulumi.set(__self__, "feed_url", feed_url)
        pulumi.set(__self__, "project_id", project_id)
        pulumi.set(__self__, "service_endpoint_name", service_endpoint_name)
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if authorization is not None:
            pulumi.set(__self__, "authorization", authorization)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if personal_access_token is not None:
            pulumi.set(__self__, "personal_access_token", personal_access_token)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="feedUrl")
    def feed_url(self) -> pulumi.Input[str]:
        """
        The URL for the feed. This will generally end with `index.json`.
        """
        return pulumi.get(self, "feed_url")

    @feed_url.setter
    def feed_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "feed_url", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        The ID of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="serviceEndpointName")
    def service_endpoint_name(self) -> pulumi.Input[str]:
        """
        The Service Endpoint name.
        """
        return pulumi.get(self, "service_endpoint_name")

    @service_endpoint_name.setter
    def service_endpoint_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_endpoint_name", value)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The API Key used to connect to the endpoint.
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter
    def authorization(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "authorization")

    @authorization.setter
    def authorization(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "authorization", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The account password used to connect to the endpoint

        > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="personalAccessToken")
    def personal_access_token(self) -> Optional[pulumi.Input[str]]:
        """
        The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        """
        return pulumi.get(self, "personal_access_token")

    @personal_access_token.setter
    def personal_access_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "personal_access_token", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The account username used to connect to the endpoint.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _ServiceendpointNugetState:
    def __init__(__self__, *,
                 api_key: Optional[pulumi.Input[str]] = None,
                 authorization: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 feed_url: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 personal_access_token: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_endpoint_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceendpointNuget resources.
        :param pulumi.Input[str] api_key: The API Key used to connect to the endpoint.
        :param pulumi.Input[str] feed_url: The URL for the feed. This will generally end with `index.json`.
        :param pulumi.Input[str] password: The account password used to connect to the endpoint
               
               > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        :param pulumi.Input[str] personal_access_token: The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        :param pulumi.Input[str] project_id: The ID of the project.
        :param pulumi.Input[str] service_endpoint_name: The Service Endpoint name.
        :param pulumi.Input[str] username: The account username used to connect to the endpoint.
        """
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if authorization is not None:
            pulumi.set(__self__, "authorization", authorization)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if feed_url is not None:
            pulumi.set(__self__, "feed_url", feed_url)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if personal_access_token is not None:
            pulumi.set(__self__, "personal_access_token", personal_access_token)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if service_endpoint_name is not None:
            pulumi.set(__self__, "service_endpoint_name", service_endpoint_name)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The API Key used to connect to the endpoint.
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter
    def authorization(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "authorization")

    @authorization.setter
    def authorization(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "authorization", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="feedUrl")
    def feed_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL for the feed. This will generally end with `index.json`.
        """
        return pulumi.get(self, "feed_url")

    @feed_url.setter
    def feed_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "feed_url", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The account password used to connect to the endpoint

        > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="personalAccessToken")
    def personal_access_token(self) -> Optional[pulumi.Input[str]]:
        """
        The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        """
        return pulumi.get(self, "personal_access_token")

    @personal_access_token.setter
    def personal_access_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "personal_access_token", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="serviceEndpointName")
    def service_endpoint_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Service Endpoint name.
        """
        return pulumi.get(self, "service_endpoint_name")

    @service_endpoint_name.setter
    def service_endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_endpoint_name", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The account username used to connect to the endpoint.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class ServiceendpointNuget(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_key: Optional[pulumi.Input[str]] = None,
                 authorization: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 feed_url: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 personal_access_token: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_endpoint_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a NuGet service endpoint within Azure DevOps.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example",
            name="Example Project",
            visibility="private",
            version_control="Git",
            work_item_template="Agile",
            description="Managed by Terraform")
        example_serviceendpoint_nuget = azuredevops.ServiceendpointNuget("example",
            project_id=example.id,
            api_key="apikey",
            service_endpoint_name="Example NuGet",
            description="Managed by Terraform")
        ```

        ## Relevant Links

        - [Azure DevOps Service REST API 7.0 - Agent Pools](https://docs.microsoft.com/en-us/rest/api/azure/devops/serviceendpoint/endpoints?view=azure-devops-rest-7.0)

        ## Import

        Azure DevOps Service Endpoint NuGet can be imported using **projectID/serviceEndpointID** or **projectName/serviceEndpointID**

        ```sh
        $ pulumi import azuredevops:index/serviceendpointNuget:ServiceendpointNuget example 00000000-0000-0000-0000-000000000000/00000000-0000-0000-0000-000000000000
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The API Key used to connect to the endpoint.
        :param pulumi.Input[str] feed_url: The URL for the feed. This will generally end with `index.json`.
        :param pulumi.Input[str] password: The account password used to connect to the endpoint
               
               > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        :param pulumi.Input[str] personal_access_token: The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        :param pulumi.Input[str] project_id: The ID of the project.
        :param pulumi.Input[str] service_endpoint_name: The Service Endpoint name.
        :param pulumi.Input[str] username: The account username used to connect to the endpoint.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceendpointNugetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a NuGet service endpoint within Azure DevOps.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azuredevops as azuredevops

        example = azuredevops.Project("example",
            name="Example Project",
            visibility="private",
            version_control="Git",
            work_item_template="Agile",
            description="Managed by Terraform")
        example_serviceendpoint_nuget = azuredevops.ServiceendpointNuget("example",
            project_id=example.id,
            api_key="apikey",
            service_endpoint_name="Example NuGet",
            description="Managed by Terraform")
        ```

        ## Relevant Links

        - [Azure DevOps Service REST API 7.0 - Agent Pools](https://docs.microsoft.com/en-us/rest/api/azure/devops/serviceendpoint/endpoints?view=azure-devops-rest-7.0)

        ## Import

        Azure DevOps Service Endpoint NuGet can be imported using **projectID/serviceEndpointID** or **projectName/serviceEndpointID**

        ```sh
        $ pulumi import azuredevops:index/serviceendpointNuget:ServiceendpointNuget example 00000000-0000-0000-0000-000000000000/00000000-0000-0000-0000-000000000000
        ```

        :param str resource_name: The name of the resource.
        :param ServiceendpointNugetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceendpointNugetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_key: Optional[pulumi.Input[str]] = None,
                 authorization: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 feed_url: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 personal_access_token: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_endpoint_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceendpointNugetArgs.__new__(ServiceendpointNugetArgs)

            __props__.__dict__["api_key"] = None if api_key is None else pulumi.Output.secret(api_key)
            __props__.__dict__["authorization"] = authorization
            __props__.__dict__["description"] = description
            if feed_url is None and not opts.urn:
                raise TypeError("Missing required property 'feed_url'")
            __props__.__dict__["feed_url"] = feed_url
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            __props__.__dict__["personal_access_token"] = None if personal_access_token is None else pulumi.Output.secret(personal_access_token)
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            if service_endpoint_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_endpoint_name'")
            __props__.__dict__["service_endpoint_name"] = service_endpoint_name
            __props__.__dict__["username"] = username
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["apiKey", "password", "personalAccessToken"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ServiceendpointNuget, __self__).__init__(
            'azuredevops:index/serviceendpointNuget:ServiceendpointNuget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key: Optional[pulumi.Input[str]] = None,
            authorization: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            description: Optional[pulumi.Input[str]] = None,
            feed_url: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            personal_access_token: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            service_endpoint_name: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'ServiceendpointNuget':
        """
        Get an existing ServiceendpointNuget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The API Key used to connect to the endpoint.
        :param pulumi.Input[str] feed_url: The URL for the feed. This will generally end with `index.json`.
        :param pulumi.Input[str] password: The account password used to connect to the endpoint
               
               > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        :param pulumi.Input[str] personal_access_token: The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        :param pulumi.Input[str] project_id: The ID of the project.
        :param pulumi.Input[str] service_endpoint_name: The Service Endpoint name.
        :param pulumi.Input[str] username: The account username used to connect to the endpoint.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceendpointNugetState.__new__(_ServiceendpointNugetState)

        __props__.__dict__["api_key"] = api_key
        __props__.__dict__["authorization"] = authorization
        __props__.__dict__["description"] = description
        __props__.__dict__["feed_url"] = feed_url
        __props__.__dict__["password"] = password
        __props__.__dict__["personal_access_token"] = personal_access_token
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["service_endpoint_name"] = service_endpoint_name
        __props__.__dict__["username"] = username
        return ServiceendpointNuget(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> pulumi.Output[Optional[str]]:
        """
        The API Key used to connect to the endpoint.
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter
    def authorization(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "authorization")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="feedUrl")
    def feed_url(self) -> pulumi.Output[str]:
        """
        The URL for the feed. This will generally end with `index.json`.
        """
        return pulumi.get(self, "feed_url")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The account password used to connect to the endpoint

        > **Note** Only one of `api_key` or `personal_access_token` or  `username`, `password` can be set at the same time.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="personalAccessToken")
    def personal_access_token(self) -> pulumi.Output[Optional[str]]:
        """
        The Personal access token used to  connect to the endpoint. Personal access tokens are applicable only for NuGet feeds hosted on other Azure DevOps Services organizations or Azure DevOps Server 2019 (or later).
        """
        return pulumi.get(self, "personal_access_token")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        The ID of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="serviceEndpointName")
    def service_endpoint_name(self) -> pulumi.Output[str]:
        """
        The Service Endpoint name.
        """
        return pulumi.get(self, "service_endpoint_name")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[Optional[str]]:
        """
        The account username used to connect to the endpoint.
        """
        return pulumi.get(self, "username")

