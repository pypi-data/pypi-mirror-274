r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to enable and disable OAuth 2.0 in the cluster. The PATCH request enables and disables OAuth 2.0 in the cluster.
<br />
---
## Examples
### Retrieving the OAuth 2.0 status in the cluster
The following output shows the OAuth 2.0 status of the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOauth2Global

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOauth2Global()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityOauth2Global({"enabled": False})

```
</div>
</div>

---
### Enabling the OAuth 2.0 in the cluster
The following output shows how to enable the OAuth 2.0 in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOauth2Global

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOauth2Global()
    resource.enabled = True
    resource.patch()

```

---"""

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


__all__ = ["SecurityOauth2Global", "SecurityOauth2GlobalSchema"]
__pdoc__ = {
    "SecurityOauth2GlobalSchema.resource": False,
    "SecurityOauth2GlobalSchema.opts": False,
    "SecurityOauth2Global.security_oauth2_global_show": False,
    "SecurityOauth2Global.security_oauth2_global_create": False,
    "SecurityOauth2Global.security_oauth2_global_modify": False,
    "SecurityOauth2Global.security_oauth2_global_delete": False,
}


class SecurityOauth2GlobalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityOauth2Global object"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether OAuth 2.0 is enabled or disabled globally. Default value is false."""

    @property
    def resource(self):
        return SecurityOauth2Global

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SecurityOauth2Global.get_collection(fields=field)]
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
            raise NetAppRestError("SecurityOauth2Global modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SecurityOauth2Global(Resource):
    """Allows interaction with SecurityOauth2Global objects on the host"""

    _schema = SecurityOauth2GlobalSchema
    _path = "/api/security/authentication/cluster/oauth2"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the OAuth 2.0 status.
### Related ONTAP commands
* `security oauth2 show`

### Learn more
* [`DOC /security/authentication/cluster/oauth2`](#docs-security-security_authentication_cluster_oauth2)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="security oauth2 global show")
        def security_oauth2_global_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single SecurityOauth2Global resource

            Args:
                enabled: Indicates whether OAuth 2.0 is enabled or disabled globally. Default value is false.
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = SecurityOauth2Global(
                **kwargs
            )
            resource.get()
            return [resource]


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the OAuth 2.0 status.
### Related ONTAP commands
* `security oauth2 modify`

### Learn more
* [`DOC /security/authentication/cluster/oauth2`](#docs-security-security_authentication_cluster_oauth2)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="security oauth2 global modify")
        async def security_oauth2_global_modify(
        ) -> ResourceTable:
            """Modify an instance of a SecurityOauth2Global resource

            Args:
                enabled: Indicates whether OAuth 2.0 is enabled or disabled globally. Default value is false.
                query_enabled: Indicates whether OAuth 2.0 is enabled or disabled globally. Default value is false.
            """

            kwargs = {}
            changes = {}
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled

            if enabled is not None:
                changes["enabled"] = enabled

            if hasattr(SecurityOauth2Global, "find"):
                resource = SecurityOauth2Global.find(
                    **kwargs
                )
            else:
                resource = SecurityOauth2Global()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify SecurityOauth2Global: %s" % err)



