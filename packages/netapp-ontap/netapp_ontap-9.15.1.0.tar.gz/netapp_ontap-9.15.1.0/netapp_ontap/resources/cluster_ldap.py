r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
LDAP servers are used to centrally maintain user information. LDAP configurations must be set up
to look up information stored in the LDAP directory on the external LDAP servers. This API is used to retrieve and manage
cluster LDAP server configurations.<br>
## Examples
### Retrieving the cluster LDAP information
The cluster LDAP GET request retrieves the LDAP configuration of the cluster.<br>
The following example shows how a GET request is used to retrieve the cluster LDAP information:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ClusterLdap(
    {
        "servers": ["10.10.10.10", "domainB.example.com"],
        "use_start_tls": True,
        "port": 389,
        "base_dn": "dc=domainA,dc=example,dc=com",
        "try_channel_binding": True,
        "base_scope": "subtree",
        "_links": {"self": {"href": "/api/security/authentication/cluster/ldap"}},
        "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
        "schema": "ad_idmu",
        "min_bind_level": "anonymous",
        "session_security": "none",
    }
)

```
</div>
</div>

### Creating the cluster LDAP configuration
The cluster LDAP POST operation creates an LDAP configuration for the cluster.<br>
The following example shows how to issue a POST request with all of the fields specified:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.servers = ["10.10.10.10", "domainB.example.com"]
    resource.schema = "ad_idmu"
    resource.port = 389
    resource.min_bind_level = "anonymous"
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.base_scope = "subtree"
    resource.use_start_tls = False
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

The following example shows how to issue a POST request with a number of optional fields not specified:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

### Updating the cluster LDAP configuration
The cluster LDAP PATCH request updates the LDAP configuration of the cluster.<br>
The following example shows how a PATCH request is used to update the cluster LDAP configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.servers = ["55.55.55.55"]
    resource.schema = "ad_idmu"
    resource.port = 636
    resource.use_start_tls = False
    resource.patch()

```

### Deleting the cluster LDAP configuration
The cluster LDAP DELETE request deletes the LDAP configuration of the cluster.<br>
The following example shows how a DELETE request is used to delete the cluster LDAP configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.delete()

```
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    RECLINE_INSTALLED = False
    import recline
    from recline.arg_types.choices import Choices
    from recline.commands import ReclineCommandError
    from netapp_ontap.resource_table import ResourceTable
    RECLINE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["ClusterLdap", "ClusterLdapSchema"]
__pdoc__ = {
    "ClusterLdapSchema.resource": False,
    "ClusterLdapSchema.opts": False,
    "ClusterLdap.cluster_ldap_show": False,
    "ClusterLdap.cluster_ldap_create": False,
    "ClusterLdap.cluster_ldap_modify": False,
    "ClusterLdap.cluster_ldap_delete": False,
}


class ClusterLdapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterLdap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster_ldap."""

    base_dn = marshmallow_fields.Str(
        data_key="base_dn",
        allow_none=True,
    )
    r""" Specifies the default base DN for all searches."""

    base_scope = marshmallow_fields.Str(
        data_key="base_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP queries:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    bind_as_cifs_server = marshmallow_fields.Boolean(
        data_key="bind_as_cifs_server",
        allow_none=True,
    )
    r""" Specifies whether or not CIFS server's credentials are used to bind to the LDAP server."""

    bind_dn = marshmallow_fields.Str(
        data_key="bind_dn",
        allow_none=True,
    )
    r""" Specifies the user that binds to the LDAP servers."""

    bind_password = marshmallow_fields.Str(
        data_key="bind_password",
        allow_none=True,
    )
    r""" Specifies the bind password for the LDAP servers."""

    group_dn = marshmallow_fields.Str(
        data_key="group_dn",
        allow_none=True,
    )
    r""" Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups."""

    group_membership_filter = marshmallow_fields.Str(
        data_key="group_membership_filter",
        allow_none=True,
    )
    r""" Specifies the custom filter used for group membership lookups from an LDAP server."""

    group_scope = marshmallow_fields.Str(
        data_key="group_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for group lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    is_netgroup_byhost_enabled = marshmallow_fields.Boolean(
        data_key="is_netgroup_byhost_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not netgroup by host querying is enabled."""

    is_owner = marshmallow_fields.Boolean(
        data_key="is_owner",
        allow_none=True,
    )
    r""" Specifies whether or not the SVM owns the LDAP client configuration."""

    ldaps_enabled = marshmallow_fields.Boolean(
        data_key="ldaps_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not LDAPS is enabled."""

    min_bind_level = marshmallow_fields.Str(
        data_key="min_bind_level",
        validate=enum_validation(['anonymous', 'simple', 'sasl']),
        allow_none=True,
    )
    r""" The minimum bind authentication level. Possible values are:

* anonymous - anonymous bind
* simple - simple bind
* sasl - Simple Authentication and Security Layer (SASL) bind


Valid choices:

* anonymous
* simple
* sasl"""

    netgroup_byhost_dn = marshmallow_fields.Str(
        data_key="netgroup_byhost_dn",
        allow_none=True,
    )
    r""" Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups."""

    netgroup_byhost_scope = marshmallow_fields.Str(
        data_key="netgroup_byhost_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for netgroup by host lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    netgroup_dn = marshmallow_fields.Str(
        data_key="netgroup_dn",
        allow_none=True,
    )
    r""" Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups."""

    netgroup_scope = marshmallow_fields.Str(
        data_key="netgroup_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for netgroup lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    port = Size(
        data_key="port",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" The port used to connect to the LDAP Servers.

Example: 389"""

    query_timeout = Size(
        data_key="query_timeout",
        allow_none=True,
    )
    r""" Specifies the maximum time to wait for a query response from the LDAP server, in seconds."""

    schema = marshmallow_fields.Str(
        data_key="schema",
        allow_none=True,
    )
    r""" The name of the schema template used by the SVM.

* AD-IDMU - Active Directory Identity Management for UNIX
* AD-SFU - Active Directory Services for UNIX
* MS-AD-BIS - Active Directory Identity Management for UNIX
* RFC-2307 - Schema based on RFC 2307
* Custom schema"""

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" The servers field of the cluster_ldap."""

    session_security = marshmallow_fields.Str(
        data_key="session_security",
        validate=enum_validation(['none', 'sign', 'seal']),
        allow_none=True,
    )
    r""" Specifies the level of security to be used for LDAP communications:

* none - no signing or sealing
* sign - sign LDAP traffic
* seal - seal and sign LDAP traffic


Valid choices:

* none
* sign
* seal"""

    skip_config_validation = marshmallow_fields.Boolean(
        data_key="skip_config_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified LDAP configuration is disabled."""

    status = marshmallow_fields.Nested("netapp_ontap.models.ldap_status.LdapStatusSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" The status field of the cluster_ldap."""

    try_channel_binding = marshmallow_fields.Boolean(
        data_key="try_channel_binding",
        allow_none=True,
    )
    r""" Specifies whether or not channel binding is attempted in the case of TLS/LDAPS."""

    use_start_tls = marshmallow_fields.Boolean(
        data_key="use_start_tls",
        allow_none=True,
    )
    r""" Specifies whether or not to use Start TLS over LDAP connections."""

    user_dn = marshmallow_fields.Str(
        data_key="user_dn",
        allow_none=True,
    )
    r""" Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups."""

    user_scope = marshmallow_fields.Str(
        data_key="user_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
        allow_none=True,
    )
    r""" Specifies the default search scope for LDAP for user lookups:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree"""

    @property
    def resource(self):
        return ClusterLdap

    gettable_fields = [
        "links",
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "is_owner",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "query_timeout",
        "schema",
        "servers",
        "session_security",
        "status",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """links,base_dn,base_scope,bind_as_cifs_server,bind_dn,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,is_owner,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,query_timeout,schema,servers,session_security,status,try_channel_binding,use_start_tls,user_dn,user_scope,"""

    patchable_fields = [
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "bind_password",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "query_timeout",
        "schema",
        "servers",
        "session_security",
        "skip_config_validation",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """base_dn,base_scope,bind_as_cifs_server,bind_dn,bind_password,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,query_timeout,schema,servers,session_security,skip_config_validation,try_channel_binding,use_start_tls,user_dn,user_scope,"""

    postable_fields = [
        "base_dn",
        "base_scope",
        "bind_as_cifs_server",
        "bind_dn",
        "bind_password",
        "group_dn",
        "group_membership_filter",
        "group_scope",
        "is_netgroup_byhost_enabled",
        "ldaps_enabled",
        "min_bind_level",
        "netgroup_byhost_dn",
        "netgroup_byhost_scope",
        "netgroup_dn",
        "netgroup_scope",
        "port",
        "query_timeout",
        "schema",
        "servers",
        "session_security",
        "skip_config_validation",
        "try_channel_binding",
        "use_start_tls",
        "user_dn",
        "user_scope",
    ]
    """base_dn,base_scope,bind_as_cifs_server,bind_dn,bind_password,group_dn,group_membership_filter,group_scope,is_netgroup_byhost_enabled,ldaps_enabled,min_bind_level,netgroup_byhost_dn,netgroup_byhost_scope,netgroup_dn,netgroup_scope,port,query_timeout,schema,servers,session_security,skip_config_validation,try_channel_binding,use_start_tls,user_dn,user_scope,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ClusterLdap.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("ClusterLdap modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ClusterLdap(Resource):
    """Allows interaction with ClusterLdap objects on the host"""

    _schema = ClusterLdapSchema
    _path = "/api/security/authentication/cluster/ldap"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster LDAP configuration.
### Related ONTAP commands
  * `ldap show`
  * `ldap check -vserver vs0`
  * `ldap check-ipv6 -vserver vs0`
### Important notes
  * The status.code, status.dn_message, status.message, and status.state fields have the same status fields that are returned using the "ldap check" CLI command.
  * Refer to the ipv4 or ipv6 objects available in the status field to get specific information about the code, dn_messages, or message and state information for ipv4 or ipv6.

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="cluster ldap show")
        def cluster_ldap_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single ClusterLdap resource

            Args:
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_as_cifs_server: Specifies whether or not CIFS server's credentials are used to bind to the LDAP server. 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                group_dn: Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.
                group_membership_filter: Specifies the custom filter used for group membership lookups from an LDAP server. 
                group_scope: Specifies the default search scope for LDAP for group lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                is_netgroup_byhost_enabled: Specifies whether or not netgroup by host querying is enabled. 
                is_owner: Specifies whether or not the SVM owns the LDAP client configuration. 
                ldaps_enabled: Specifies whether or not LDAPS is enabled. 
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                netgroup_byhost_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.
                netgroup_byhost_scope: Specifies the default search scope for LDAP for netgroup by host lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                netgroup_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.
                netgroup_scope: Specifies the default search scope for LDAP for netgroup lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                port: The port used to connect to the LDAP Servers.
                query_timeout: Specifies the maximum time to wait for a query response from the LDAP server, in seconds. 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                skip_config_validation: Indicates whether or not the validation for the specified LDAP configuration is disabled. 
                try_channel_binding: Specifies whether or not channel binding is attempted in the case of TLS/LDAPS. 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                user_dn: Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.
                user_scope: Specifies the default search scope for LDAP for user lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
            """

            kwargs = {}
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_as_cifs_server is not None:
                kwargs["bind_as_cifs_server"] = bind_as_cifs_server
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if group_dn is not None:
                kwargs["group_dn"] = group_dn
            if group_membership_filter is not None:
                kwargs["group_membership_filter"] = group_membership_filter
            if group_scope is not None:
                kwargs["group_scope"] = group_scope
            if is_netgroup_byhost_enabled is not None:
                kwargs["is_netgroup_byhost_enabled"] = is_netgroup_byhost_enabled
            if is_owner is not None:
                kwargs["is_owner"] = is_owner
            if ldaps_enabled is not None:
                kwargs["ldaps_enabled"] = ldaps_enabled
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if netgroup_byhost_dn is not None:
                kwargs["netgroup_byhost_dn"] = netgroup_byhost_dn
            if netgroup_byhost_scope is not None:
                kwargs["netgroup_byhost_scope"] = netgroup_byhost_scope
            if netgroup_dn is not None:
                kwargs["netgroup_dn"] = netgroup_dn
            if netgroup_scope is not None:
                kwargs["netgroup_scope"] = netgroup_scope
            if port is not None:
                kwargs["port"] = port
            if query_timeout is not None:
                kwargs["query_timeout"] = query_timeout
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if try_channel_binding is not None:
                kwargs["try_channel_binding"] = try_channel_binding
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls
            if user_dn is not None:
                kwargs["user_dn"] = user_dn
            if user_scope is not None:
                kwargs["user_scope"] = user_scope
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = ClusterLdap(
                **kwargs
            )
            resource.get()
            return [resource]

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""A cluster can have only one LDAP configuration. IPv6 must be enabled if IPv6 family addresses are specified.
### Required properties
* `servers` - List of LDAP servers used for this client configuration.
### Recommended optional properties
* `schema` - Schema template name.
* `port` - Port used to connect to the LDAP Servers.
* `ldaps_enabled` - Specifies whether or not LDAPS is enabled.
* `min_bind_level` - Minimum bind authentication level.
* `bind_dn` - Specifies the user that binds to the LDAP servers.
* `base_dn` - Specifies the default base DN for all searches.
* `bind_password` - Specifies the bind password for the LDAP servers.
* `base_scope` - Specifies the default search scope for LDAP queries.
* `use_start_tls` - Specifies whether or not to use Start TLS over LDAP connections.
* `session_security` - Specifies the level of security to be used for LDAP communications.
* `bind_as_cifs_server` - Indicates if CIFS server's credentials are used to bind to the LDAP server.
* `query_timeout` - Maximum time to wait for a query response from the LDAP server, in seconds.
* `user_dn` - User Distinguished Name (DN) used as the starting point in the LDAP directory tree for user lookups.
* `user_scope` - Default search scope for LDAP for user lookups.
* `group_dn` - Group Distinguished Name (DN) used as the starting point in the LDAP directory tree for group lookups.
* `group_scope` - Default search scope for LDAP for group lookups.
* `netgroup_dn` - Netgroup Distinguished Name (DN) used as the starting point in the LDAP directory tree for netgroup lookups.
* `netgroup_scope` - Default search scope for LDAP for netgroup lookups.
* `netgroup_byhost_dn` - Netgroup Distinguished Name (DN) used as the starting point in the LDAP directory tree for netgroup by host lookups.
* `netgroup_byhost_scope` - Default search scope for LDAP for netgroup by host lookups.
* `is_netgroup_byhost_enabled` - Specifies whether netgroup by host querying is enabled.
* `group_membership_filter` - Custom filter used for group membership lookup from an LDAP server.
* `skip_config_validation` - Indicates whether or not the validation for the specified LDAP configuration is disabled.
### Default property values
* `schema` - _RFC-2307_
* `port` - _389_
* `ldaps_enabled` - _false_
* `min_bind_level` - _simple_
* `base_scope` - _subtree_
* `use_start_tls` - _false_
* `session_security` - _none_
* `query_timeout` - _3_
* `user_scope` - _subtree_
* `group_scope` - _subtree_
* `netgroup_scope` - _subtree_
* `netgroup_byhost_scope` - _subtree_
* `is_netgroup_byhost_enabled` - _false_
* `skip_config_validation` - _false_
* `try_channel_binding` - _true_
<br/>
Configuring more than one LDAP server is recommended to avoid a single point of failure. Both FQDNs and IP addresses are supported for the `servers` property.
The LDAP servers are validated as part of this operation. LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server is invalid.
3. The server is unreachable.<br/>

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="cluster ldap create")
        async def cluster_ldap_create(
        ) -> ResourceTable:
            """Create an instance of a ClusterLdap resource

            Args:
                links: 
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_as_cifs_server: Specifies whether or not CIFS server's credentials are used to bind to the LDAP server. 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                group_dn: Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.
                group_membership_filter: Specifies the custom filter used for group membership lookups from an LDAP server. 
                group_scope: Specifies the default search scope for LDAP for group lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                is_netgroup_byhost_enabled: Specifies whether or not netgroup by host querying is enabled. 
                is_owner: Specifies whether or not the SVM owns the LDAP client configuration. 
                ldaps_enabled: Specifies whether or not LDAPS is enabled. 
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                netgroup_byhost_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.
                netgroup_byhost_scope: Specifies the default search scope for LDAP for netgroup by host lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                netgroup_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.
                netgroup_scope: Specifies the default search scope for LDAP for netgroup lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                port: The port used to connect to the LDAP Servers.
                query_timeout: Specifies the maximum time to wait for a query response from the LDAP server, in seconds. 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                skip_config_validation: Indicates whether or not the validation for the specified LDAP configuration is disabled. 
                status: 
                try_channel_binding: Specifies whether or not channel binding is attempted in the case of TLS/LDAPS. 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                user_dn: Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.
                user_scope: Specifies the default search scope for LDAP for user lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_as_cifs_server is not None:
                kwargs["bind_as_cifs_server"] = bind_as_cifs_server
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if group_dn is not None:
                kwargs["group_dn"] = group_dn
            if group_membership_filter is not None:
                kwargs["group_membership_filter"] = group_membership_filter
            if group_scope is not None:
                kwargs["group_scope"] = group_scope
            if is_netgroup_byhost_enabled is not None:
                kwargs["is_netgroup_byhost_enabled"] = is_netgroup_byhost_enabled
            if is_owner is not None:
                kwargs["is_owner"] = is_owner
            if ldaps_enabled is not None:
                kwargs["ldaps_enabled"] = ldaps_enabled
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if netgroup_byhost_dn is not None:
                kwargs["netgroup_byhost_dn"] = netgroup_byhost_dn
            if netgroup_byhost_scope is not None:
                kwargs["netgroup_byhost_scope"] = netgroup_byhost_scope
            if netgroup_dn is not None:
                kwargs["netgroup_dn"] = netgroup_dn
            if netgroup_scope is not None:
                kwargs["netgroup_scope"] = netgroup_scope
            if port is not None:
                kwargs["port"] = port
            if query_timeout is not None:
                kwargs["query_timeout"] = query_timeout
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if status is not None:
                kwargs["status"] = status
            if try_channel_binding is not None:
                kwargs["try_channel_binding"] = try_channel_binding
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls
            if user_dn is not None:
                kwargs["user_dn"] = user_dn
            if user_scope is not None:
                kwargs["user_scope"] = user_scope

            resource = ClusterLdap(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create ClusterLdap: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Both mandatory and optional parameters of the LDAP configuration can be updated.
IPv6 must be enabled if IPv6 family addresses are specified. Configuring more than one LDAP server is recommended to avoid a single point of failure. Both FQDNs and IP addresses are supported for the `servers` property.
The LDAP servers are validated as part of this operation. LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server is invalid.
3. The server is unreachable. <br/>

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="cluster ldap modify")
        async def cluster_ldap_modify(
        ) -> ResourceTable:
            """Modify an instance of a ClusterLdap resource

            Args:
                base_dn: Specifies the default base DN for all searches.
                query_base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_as_cifs_server: Specifies whether or not CIFS server's credentials are used to bind to the LDAP server. 
                query_bind_as_cifs_server: Specifies whether or not CIFS server's credentials are used to bind to the LDAP server. 
                bind_dn: Specifies the user that binds to the LDAP servers.
                query_bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                query_bind_password: Specifies the bind password for the LDAP servers.
                group_dn: Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.
                query_group_dn: Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.
                group_membership_filter: Specifies the custom filter used for group membership lookups from an LDAP server. 
                query_group_membership_filter: Specifies the custom filter used for group membership lookups from an LDAP server. 
                group_scope: Specifies the default search scope for LDAP for group lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_group_scope: Specifies the default search scope for LDAP for group lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                is_netgroup_byhost_enabled: Specifies whether or not netgroup by host querying is enabled. 
                query_is_netgroup_byhost_enabled: Specifies whether or not netgroup by host querying is enabled. 
                is_owner: Specifies whether or not the SVM owns the LDAP client configuration. 
                query_is_owner: Specifies whether or not the SVM owns the LDAP client configuration. 
                ldaps_enabled: Specifies whether or not LDAPS is enabled. 
                query_ldaps_enabled: Specifies whether or not LDAPS is enabled. 
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                query_min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                netgroup_byhost_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.
                query_netgroup_byhost_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.
                netgroup_byhost_scope: Specifies the default search scope for LDAP for netgroup by host lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_netgroup_byhost_scope: Specifies the default search scope for LDAP for netgroup by host lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                netgroup_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.
                query_netgroup_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.
                netgroup_scope: Specifies the default search scope for LDAP for netgroup lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_netgroup_scope: Specifies the default search scope for LDAP for netgroup lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                port: The port used to connect to the LDAP Servers.
                query_port: The port used to connect to the LDAP Servers.
                query_timeout: Specifies the maximum time to wait for a query response from the LDAP server, in seconds. 
                query_query_timeout: Specifies the maximum time to wait for a query response from the LDAP server, in seconds. 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                query_schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                query_servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                query_session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                skip_config_validation: Indicates whether or not the validation for the specified LDAP configuration is disabled. 
                query_skip_config_validation: Indicates whether or not the validation for the specified LDAP configuration is disabled. 
                try_channel_binding: Specifies whether or not channel binding is attempted in the case of TLS/LDAPS. 
                query_try_channel_binding: Specifies whether or not channel binding is attempted in the case of TLS/LDAPS. 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                query_use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                user_dn: Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.
                query_user_dn: Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.
                user_scope: Specifies the default search scope for LDAP for user lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_user_scope: Specifies the default search scope for LDAP for user lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
            """

            kwargs = {}
            changes = {}
            if query_base_dn is not None:
                kwargs["base_dn"] = query_base_dn
            if query_base_scope is not None:
                kwargs["base_scope"] = query_base_scope
            if query_bind_as_cifs_server is not None:
                kwargs["bind_as_cifs_server"] = query_bind_as_cifs_server
            if query_bind_dn is not None:
                kwargs["bind_dn"] = query_bind_dn
            if query_bind_password is not None:
                kwargs["bind_password"] = query_bind_password
            if query_group_dn is not None:
                kwargs["group_dn"] = query_group_dn
            if query_group_membership_filter is not None:
                kwargs["group_membership_filter"] = query_group_membership_filter
            if query_group_scope is not None:
                kwargs["group_scope"] = query_group_scope
            if query_is_netgroup_byhost_enabled is not None:
                kwargs["is_netgroup_byhost_enabled"] = query_is_netgroup_byhost_enabled
            if query_is_owner is not None:
                kwargs["is_owner"] = query_is_owner
            if query_ldaps_enabled is not None:
                kwargs["ldaps_enabled"] = query_ldaps_enabled
            if query_min_bind_level is not None:
                kwargs["min_bind_level"] = query_min_bind_level
            if query_netgroup_byhost_dn is not None:
                kwargs["netgroup_byhost_dn"] = query_netgroup_byhost_dn
            if query_netgroup_byhost_scope is not None:
                kwargs["netgroup_byhost_scope"] = query_netgroup_byhost_scope
            if query_netgroup_dn is not None:
                kwargs["netgroup_dn"] = query_netgroup_dn
            if query_netgroup_scope is not None:
                kwargs["netgroup_scope"] = query_netgroup_scope
            if query_port is not None:
                kwargs["port"] = query_port
            if query_query_timeout is not None:
                kwargs["query_timeout"] = query_query_timeout
            if query_schema is not None:
                kwargs["schema"] = query_schema
            if query_servers is not None:
                kwargs["servers"] = query_servers
            if query_session_security is not None:
                kwargs["session_security"] = query_session_security
            if query_skip_config_validation is not None:
                kwargs["skip_config_validation"] = query_skip_config_validation
            if query_try_channel_binding is not None:
                kwargs["try_channel_binding"] = query_try_channel_binding
            if query_use_start_tls is not None:
                kwargs["use_start_tls"] = query_use_start_tls
            if query_user_dn is not None:
                kwargs["user_dn"] = query_user_dn
            if query_user_scope is not None:
                kwargs["user_scope"] = query_user_scope

            if base_dn is not None:
                changes["base_dn"] = base_dn
            if base_scope is not None:
                changes["base_scope"] = base_scope
            if bind_as_cifs_server is not None:
                changes["bind_as_cifs_server"] = bind_as_cifs_server
            if bind_dn is not None:
                changes["bind_dn"] = bind_dn
            if bind_password is not None:
                changes["bind_password"] = bind_password
            if group_dn is not None:
                changes["group_dn"] = group_dn
            if group_membership_filter is not None:
                changes["group_membership_filter"] = group_membership_filter
            if group_scope is not None:
                changes["group_scope"] = group_scope
            if is_netgroup_byhost_enabled is not None:
                changes["is_netgroup_byhost_enabled"] = is_netgroup_byhost_enabled
            if is_owner is not None:
                changes["is_owner"] = is_owner
            if ldaps_enabled is not None:
                changes["ldaps_enabled"] = ldaps_enabled
            if min_bind_level is not None:
                changes["min_bind_level"] = min_bind_level
            if netgroup_byhost_dn is not None:
                changes["netgroup_byhost_dn"] = netgroup_byhost_dn
            if netgroup_byhost_scope is not None:
                changes["netgroup_byhost_scope"] = netgroup_byhost_scope
            if netgroup_dn is not None:
                changes["netgroup_dn"] = netgroup_dn
            if netgroup_scope is not None:
                changes["netgroup_scope"] = netgroup_scope
            if port is not None:
                changes["port"] = port
            if query_timeout is not None:
                changes["query_timeout"] = query_timeout
            if schema is not None:
                changes["schema"] = schema
            if servers is not None:
                changes["servers"] = servers
            if session_security is not None:
                changes["session_security"] = session_security
            if skip_config_validation is not None:
                changes["skip_config_validation"] = skip_config_validation
            if try_channel_binding is not None:
                changes["try_channel_binding"] = try_channel_binding
            if use_start_tls is not None:
                changes["use_start_tls"] = use_start_tls
            if user_dn is not None:
                changes["user_dn"] = user_dn
            if user_scope is not None:
                changes["user_scope"] = user_scope

            if hasattr(ClusterLdap, "find"):
                resource = ClusterLdap.find(
                    **kwargs
                )
            else:
                resource = ClusterLdap()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify ClusterLdap: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the LDAP configuration of the cluster.

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="cluster ldap delete")
        async def cluster_ldap_delete(
        ) -> None:
            """Delete an instance of a ClusterLdap resource

            Args:
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_as_cifs_server: Specifies whether or not CIFS server's credentials are used to bind to the LDAP server. 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                group_dn: Specifies the group Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for group lookups.
                group_membership_filter: Specifies the custom filter used for group membership lookups from an LDAP server. 
                group_scope: Specifies the default search scope for LDAP for group lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                is_netgroup_byhost_enabled: Specifies whether or not netgroup by host querying is enabled. 
                is_owner: Specifies whether or not the SVM owns the LDAP client configuration. 
                ldaps_enabled: Specifies whether or not LDAPS is enabled. 
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                netgroup_byhost_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup by host lookups.
                netgroup_byhost_scope: Specifies the default search scope for LDAP for netgroup by host lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                netgroup_dn: Specifies the netgroup Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for netgroup lookups.
                netgroup_scope: Specifies the default search scope for LDAP for netgroup lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                port: The port used to connect to the LDAP Servers.
                query_timeout: Specifies the maximum time to wait for a query response from the LDAP server, in seconds. 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                skip_config_validation: Indicates whether or not the validation for the specified LDAP configuration is disabled. 
                try_channel_binding: Specifies whether or not channel binding is attempted in the case of TLS/LDAPS. 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                user_dn: Specifies the user Distinguished Name (DN) that is used as the starting point in the LDAP directory tree for user lookups.
                user_scope: Specifies the default search scope for LDAP for user lookups: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
            """

            kwargs = {}
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_as_cifs_server is not None:
                kwargs["bind_as_cifs_server"] = bind_as_cifs_server
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if group_dn is not None:
                kwargs["group_dn"] = group_dn
            if group_membership_filter is not None:
                kwargs["group_membership_filter"] = group_membership_filter
            if group_scope is not None:
                kwargs["group_scope"] = group_scope
            if is_netgroup_byhost_enabled is not None:
                kwargs["is_netgroup_byhost_enabled"] = is_netgroup_byhost_enabled
            if is_owner is not None:
                kwargs["is_owner"] = is_owner
            if ldaps_enabled is not None:
                kwargs["ldaps_enabled"] = ldaps_enabled
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if netgroup_byhost_dn is not None:
                kwargs["netgroup_byhost_dn"] = netgroup_byhost_dn
            if netgroup_byhost_scope is not None:
                kwargs["netgroup_byhost_scope"] = netgroup_byhost_scope
            if netgroup_dn is not None:
                kwargs["netgroup_dn"] = netgroup_dn
            if netgroup_scope is not None:
                kwargs["netgroup_scope"] = netgroup_scope
            if port is not None:
                kwargs["port"] = port
            if query_timeout is not None:
                kwargs["query_timeout"] = query_timeout
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if try_channel_binding is not None:
                kwargs["try_channel_binding"] = try_channel_binding
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls
            if user_dn is not None:
                kwargs["user_dn"] = user_dn
            if user_scope is not None:
                kwargs["user_scope"] = user_scope

            if hasattr(ClusterLdap, "find"):
                resource = ClusterLdap.find(
                    **kwargs
                )
            else:
                resource = ClusterLdap()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete ClusterLdap: %s" % err)


