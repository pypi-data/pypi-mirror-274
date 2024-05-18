# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

clientCertificate: Optional[str]
"""
Base64 encoded certificate to use to authenticate to the service principal.
"""

clientCertificatePassword: Optional[str]
"""
Password for a client certificate password.
"""

clientCertificatePath: Optional[str]
"""
Path to a certificate to use to authenticate to the service principal.
"""

clientId: Optional[str]
"""
The service principal client or managed service principal id which should be used.
"""

clientIdApply: Optional[str]

clientIdPlan: Optional[str]

clientSecret: Optional[str]
"""
Client secret for authenticating to a service principal.
"""

clientSecretPath: Optional[str]
"""
Path to a file containing a client secret for authenticating to a service principal.
"""

oidcAudience: Optional[str]
"""
Set the audience when requesting OIDC tokens.
"""

oidcRequestToken: Optional[str]
"""
The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID
Connect.
"""

oidcRequestUrl: Optional[str]
"""
The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal
using OpenID Connect.
"""

oidcTfcTag: Optional[str]

oidcToken: Optional[str]
"""
OIDC token to authenticate as a service principal.
"""

oidcTokenFilePath: Optional[str]
"""
OIDC token from file to authenticate as a service principal.
"""

orgServiceUrl: Optional[str]
"""
The url of the Azure DevOps instance which should be used.
"""

personalAccessToken: Optional[str]
"""
The personal access token which should be used.
"""

tenantId: Optional[str]
"""
The service principal tenant id which should be used.
"""

tenantIdApply: Optional[str]

tenantIdPlan: Optional[str]

useMsi: Optional[bool]
"""
Use an Azure Managed Service Identity.
"""

useOidc: Optional[bool]
"""
Use an OIDC token to authenticate to a service principal.
"""

