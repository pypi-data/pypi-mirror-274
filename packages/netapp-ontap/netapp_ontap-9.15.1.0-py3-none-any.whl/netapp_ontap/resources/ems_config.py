r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This endpoint is used to configure general parameters of the Event Management System (EMS).
## Examples
### Configuring the system-wide email parameters
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsConfig()
    resource.mail_from = "administrator@mycompany.com"
    resource.mail_server = "mycompany.com"
    resource.mail_server_user = "smtp"
    resource.patch()

```

### Retrieving the EMS configuration
The following example retrieves EMS configuration for the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsConfig()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
EmsConfig(
    {
        "pubsub_enabled": True,
        "_links": {"self": {"href": "/api/support/ems"}},
        "mail_from": "admin@localhost",
        "mail_server": "localhost",
    }
)

```
</div>
</div>
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


__all__ = ["EmsConfig", "EmsConfigSchema"]
__pdoc__ = {
    "EmsConfigSchema.resource": False,
    "EmsConfigSchema.opts": False,
    "EmsConfig.ems_config_show": False,
    "EmsConfig.ems_config_create": False,
    "EmsConfig.ems_config_modify": False,
    "EmsConfig.ems_config_delete": False,
}


class EmsConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsConfig object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_config."""

    mail_from = marshmallow_fields.Str(
        data_key="mail_from",
        allow_none=True,
    )
    r""" Mail from

Example: administrator@mycompany.com"""

    mail_server = marshmallow_fields.Str(
        data_key="mail_server",
        allow_none=True,
    )
    r""" Mail server (SMTP)

Example: mail.mycompany.com"""

    mail_server_password = marshmallow_fields.Str(
        data_key="mail_server_password",
        allow_none=True,
    )
    r""" Password for Mail server (SMTP)

Example: password"""

    mail_server_user = marshmallow_fields.Str(
        data_key="mail_server_user",
        allow_none=True,
    )
    r""" Username for Mail server (SMTP)

Example: user"""

    proxy_password = marshmallow_fields.Str(
        data_key="proxy_password",
        allow_none=True,
    )
    r""" Password for HTTP/HTTPS proxy

Example: password"""

    proxy_url = marshmallow_fields.Str(
        data_key="proxy_url",
        allow_none=True,
    )
    r""" HTTP/HTTPS proxy URL

Example: https://proxyserver.mycompany.com"""

    proxy_user = marshmallow_fields.Str(
        data_key="proxy_user",
        allow_none=True,
    )
    r""" User name for HTTP/HTTPS proxy

Example: proxy_user"""

    pubsub_enabled = marshmallow_fields.Boolean(
        data_key="pubsub_enabled",
        allow_none=True,
    )
    r""" Is Publish/Subscribe Messaging Enabled?

Example: true"""

    @property
    def resource(self):
        return EmsConfig

    gettable_fields = [
        "links",
        "mail_from",
        "mail_server",
        "mail_server_user",
        "proxy_url",
        "proxy_user",
        "pubsub_enabled",
    ]
    """links,mail_from,mail_server,mail_server_user,proxy_url,proxy_user,pubsub_enabled,"""

    patchable_fields = [
        "mail_from",
        "mail_server",
        "mail_server_password",
        "mail_server_user",
        "proxy_password",
        "proxy_url",
        "proxy_user",
        "pubsub_enabled",
    ]
    """mail_from,mail_server,mail_server_password,mail_server_user,proxy_password,proxy_url,proxy_user,pubsub_enabled,"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in EmsConfig.get_collection(fields=field)]
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
            raise NetAppRestError("EmsConfig modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class EmsConfig(Resource):
    """Allows interaction with EmsConfig objects on the host"""

    _schema = EmsConfigSchema
    _path = "/api/support/ems"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the EMS configuration.
### Related ONTAP commands
* `event config show`

### Learn more
* [`DOC /support/ems`](#docs-support-support_ems)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems config show")
        def ems_config_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single EmsConfig resource

            Args:
                mail_from: Mail from
                mail_server: Mail server (SMTP)
                mail_server_password: Password for Mail server (SMTP)
                mail_server_user: Username for Mail server (SMTP)
                proxy_password: Password for HTTP/HTTPS proxy
                proxy_url: HTTP/HTTPS proxy URL
                proxy_user: User name for HTTP/HTTPS proxy
                pubsub_enabled: Is Publish/Subscribe Messaging Enabled?
            """

            kwargs = {}
            if mail_from is not None:
                kwargs["mail_from"] = mail_from
            if mail_server is not None:
                kwargs["mail_server"] = mail_server
            if mail_server_password is not None:
                kwargs["mail_server_password"] = mail_server_password
            if mail_server_user is not None:
                kwargs["mail_server_user"] = mail_server_user
            if proxy_password is not None:
                kwargs["proxy_password"] = proxy_password
            if proxy_url is not None:
                kwargs["proxy_url"] = proxy_url
            if proxy_user is not None:
                kwargs["proxy_user"] = proxy_user
            if pubsub_enabled is not None:
                kwargs["pubsub_enabled"] = pubsub_enabled
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = EmsConfig(
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
        r"""Updates the EMS configuration.
### Related ONTAP commands
* `event config modify`

### Learn more
* [`DOC /support/ems`](#docs-support-support_ems)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems config modify")
        async def ems_config_modify(
        ) -> ResourceTable:
            """Modify an instance of a EmsConfig resource

            Args:
                mail_from: Mail from
                query_mail_from: Mail from
                mail_server: Mail server (SMTP)
                query_mail_server: Mail server (SMTP)
                mail_server_password: Password for Mail server (SMTP)
                query_mail_server_password: Password for Mail server (SMTP)
                mail_server_user: Username for Mail server (SMTP)
                query_mail_server_user: Username for Mail server (SMTP)
                proxy_password: Password for HTTP/HTTPS proxy
                query_proxy_password: Password for HTTP/HTTPS proxy
                proxy_url: HTTP/HTTPS proxy URL
                query_proxy_url: HTTP/HTTPS proxy URL
                proxy_user: User name for HTTP/HTTPS proxy
                query_proxy_user: User name for HTTP/HTTPS proxy
                pubsub_enabled: Is Publish/Subscribe Messaging Enabled?
                query_pubsub_enabled: Is Publish/Subscribe Messaging Enabled?
            """

            kwargs = {}
            changes = {}
            if query_mail_from is not None:
                kwargs["mail_from"] = query_mail_from
            if query_mail_server is not None:
                kwargs["mail_server"] = query_mail_server
            if query_mail_server_password is not None:
                kwargs["mail_server_password"] = query_mail_server_password
            if query_mail_server_user is not None:
                kwargs["mail_server_user"] = query_mail_server_user
            if query_proxy_password is not None:
                kwargs["proxy_password"] = query_proxy_password
            if query_proxy_url is not None:
                kwargs["proxy_url"] = query_proxy_url
            if query_proxy_user is not None:
                kwargs["proxy_user"] = query_proxy_user
            if query_pubsub_enabled is not None:
                kwargs["pubsub_enabled"] = query_pubsub_enabled

            if mail_from is not None:
                changes["mail_from"] = mail_from
            if mail_server is not None:
                changes["mail_server"] = mail_server
            if mail_server_password is not None:
                changes["mail_server_password"] = mail_server_password
            if mail_server_user is not None:
                changes["mail_server_user"] = mail_server_user
            if proxy_password is not None:
                changes["proxy_password"] = proxy_password
            if proxy_url is not None:
                changes["proxy_url"] = proxy_url
            if proxy_user is not None:
                changes["proxy_user"] = proxy_user
            if pubsub_enabled is not None:
                changes["pubsub_enabled"] = pubsub_enabled

            if hasattr(EmsConfig, "find"):
                resource = EmsConfig.find(
                    **kwargs
                )
            else:
                resource = EmsConfig()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify EmsConfig: %s" % err)



