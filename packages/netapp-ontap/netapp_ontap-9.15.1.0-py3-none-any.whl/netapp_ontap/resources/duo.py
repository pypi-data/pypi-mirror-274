r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures the Duo profile for an SVM.
Specify the owner UUID. The owner UUID corresponds to the UUID of the SVM containing the Duo profile and can be obtained from the response body of the GET request performed on the API “/api/svm/svms".
## Examples
### Retrieving the specific configured Duo profile of the cluster or SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Duo(
    {
        "comment": "Duo profile for Cserver",
        "fail_mode": "safe",
        "integration_key": "AAAA1A11A1AAA1AAA111",
        "owner": {"name": "cluster-1", "uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"},
        "api_host": "api-******.duosecurity.com",
        "status": "Ok",
        "auto_push": True,
        "fingerprint": "xxxxxxxxxc8f58b1d52317e1212e9f067a958c387e5e2axxxxxxxxxxxxxxxxxx",
        "is_enabled": True,
        "max_prompts": 1,
        "push_info": True,
    }
)

```
</div>
</div>

### Modifying the Duo profile
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
    resource.comment = "Testing"
    resource.auto_push = False
    resource.patch()

```

### Deleting the Duo profile
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
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


__all__ = ["Duo", "DuoSchema"]
__pdoc__ = {
    "DuoSchema.resource": False,
    "DuoSchema.opts": False,
    "Duo.duo_show": False,
    "Duo.duo_create": False,
    "Duo.duo_modify": False,
    "Duo.duo_delete": False,
}


class DuoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Duo object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the duo."""

    api_host = marshmallow_fields.Str(
        data_key="api_host",
        allow_none=True,
    )
    r""" The URL at which the Duo API is hosted.

Example: api-****.duo.com"""

    auto_push = marshmallow_fields.Boolean(
        data_key="auto_push",
        allow_none=True,
    )
    r""" Automatically sends a push notification for authentication when using Duo.

Example: true"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment for the Duo profile."""

    fail_mode = marshmallow_fields.Str(
        data_key="fail_mode",
        validate=enum_validation(['safe', 'secure']),
        allow_none=True,
    )
    r""" Determines the behavior of the system when it cannot communicate with the Duo service.

Valid choices:

* safe
* secure"""

    fingerprint = marshmallow_fields.Str(
        data_key="fingerprint",
        allow_none=True,
    )
    r""" The SHA fingerprint corresponding to the Duo secret key."""

    http_proxy = marshmallow_fields.Str(
        data_key="http_proxy",
        allow_none=True,
    )
    r""" Specifies the HTTP proxy server to be used when connecting to the Duo service.

Example: IPaddress:port"""

    integration_key = marshmallow_fields.Str(
        data_key="integration_key",
        allow_none=True,
    )
    r""" The Integration Key associated with the Duo profile."""

    is_enabled = marshmallow_fields.Boolean(
        data_key="is_enabled",
        allow_none=True,
    )
    r""" Indicates whether the Duo authentication feature is active or inactive.

Example: true"""

    max_prompts = Size(
        data_key="max_prompts",
        validate=integer_validation(minimum=1, maximum=3),
        allow_none=True,
    )
    r""" The maximum number of authentication attempts allowed for a user before the process is terminated.

Example: 1"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the duo."""

    push_info = marshmallow_fields.Boolean(
        data_key="push_info",
        allow_none=True,
    )
    r""" Additional information sent along with the push notification for Duo authentication.

Example: true"""

    secret_key = marshmallow_fields.Str(
        data_key="secret_key",
        allow_none=True,
    )
    r""" The Secret Key associated with the Duo profile."""

    status = marshmallow_fields.Str(
        data_key="status",
        allow_none=True,
    )
    r""" Information on the reachability status of Duo.

Example: OK"""

    @property
    def resource(self):
        return Duo

    gettable_fields = [
        "links",
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "fingerprint",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "push_info",
        "status",
    ]
    """links,api_host,auto_push,comment,fail_mode,fingerprint,http_proxy,integration_key,is_enabled,max_prompts,owner.links,owner.name,owner.uuid,push_info,status,"""

    patchable_fields = [
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.name",
        "owner.uuid",
        "push_info",
        "secret_key",
    ]
    """api_host,auto_push,comment,fail_mode,http_proxy,integration_key,is_enabled,max_prompts,owner.name,owner.uuid,push_info,secret_key,"""

    postable_fields = [
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.name",
        "owner.uuid",
        "push_info",
        "secret_key",
    ]
    """api_host,auto_push,comment,fail_mode,http_proxy,integration_key,is_enabled,max_prompts,owner.name,owner.uuid,push_info,secret_key,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Duo.get_collection(fields=field)]
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
            raise NetAppRestError("Duo modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Duo(Resource):
    r""" Duo profile for the SVM or cluster-management server (Cserver). """

    _schema = DuoSchema
    _path = "/api/security/authentication/duo/profiles"
    _keys = ["owner.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the configured Duo profiles.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duo show")
        def duo_show(
            fields: List[Choices.define(["api_host", "auto_push", "comment", "fail_mode", "fingerprint", "http_proxy", "integration_key", "is_enabled", "max_prompts", "push_info", "secret_key", "status", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Duo resources

            Args:
                api_host: The URL at which the Duo API is hosted.
                auto_push: Automatically sends a push notification for authentication when using Duo.
                comment: Comment for the Duo profile.
                fail_mode: Determines the behavior of the system when it cannot communicate with the Duo service.
                fingerprint: The SHA fingerprint corresponding to the Duo secret key.
                http_proxy: Specifies the HTTP proxy server to be used when connecting to the Duo service.
                integration_key: The Integration Key associated with the Duo profile.
                is_enabled: Indicates whether the Duo authentication feature is active or inactive.
                max_prompts: The maximum number of authentication attempts allowed for a user before the process is terminated.
                push_info: Additional information sent along with the push notification for Duo authentication.
                secret_key: The Secret Key associated with the Duo profile.
                status: Information on the reachability status of Duo.
            """

            kwargs = {}
            if api_host is not None:
                kwargs["api_host"] = api_host
            if auto_push is not None:
                kwargs["auto_push"] = auto_push
            if comment is not None:
                kwargs["comment"] = comment
            if fail_mode is not None:
                kwargs["fail_mode"] = fail_mode
            if fingerprint is not None:
                kwargs["fingerprint"] = fingerprint
            if http_proxy is not None:
                kwargs["http_proxy"] = http_proxy
            if integration_key is not None:
                kwargs["integration_key"] = integration_key
            if is_enabled is not None:
                kwargs["is_enabled"] = is_enabled
            if max_prompts is not None:
                kwargs["max_prompts"] = max_prompts
            if push_info is not None:
                kwargs["push_info"] = push_info
            if secret_key is not None:
                kwargs["secret_key"] = secret_key
            if status is not None:
                kwargs["status"] = status
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Duo.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Duo resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent Duo resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Duo"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo profile for a cluster or an SVM.
### Related ONTAP commands
* `security login duo modify`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Duo"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Duo"], NetAppResponse]:
        r"""Creates a Duo profile.
### Related ONTAP commands
* `security login duo create`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Duo"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Duo profile of the SVM or cluster.
### Related ONTAP commands
* `security login duo delete`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the configured Duo profiles.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Duo profile configured for the cluster or an SVM.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a Duo profile.
### Related ONTAP commands
* `security login duo create`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duo create")
        async def duo_create(
        ) -> ResourceTable:
            """Create an instance of a Duo resource

            Args:
                links: 
                api_host: The URL at which the Duo API is hosted.
                auto_push: Automatically sends a push notification for authentication when using Duo.
                comment: Comment for the Duo profile.
                fail_mode: Determines the behavior of the system when it cannot communicate with the Duo service.
                fingerprint: The SHA fingerprint corresponding to the Duo secret key.
                http_proxy: Specifies the HTTP proxy server to be used when connecting to the Duo service.
                integration_key: The Integration Key associated with the Duo profile.
                is_enabled: Indicates whether the Duo authentication feature is active or inactive.
                max_prompts: The maximum number of authentication attempts allowed for a user before the process is terminated.
                owner: 
                push_info: Additional information sent along with the push notification for Duo authentication.
                secret_key: The Secret Key associated with the Duo profile.
                status: Information on the reachability status of Duo.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if api_host is not None:
                kwargs["api_host"] = api_host
            if auto_push is not None:
                kwargs["auto_push"] = auto_push
            if comment is not None:
                kwargs["comment"] = comment
            if fail_mode is not None:
                kwargs["fail_mode"] = fail_mode
            if fingerprint is not None:
                kwargs["fingerprint"] = fingerprint
            if http_proxy is not None:
                kwargs["http_proxy"] = http_proxy
            if integration_key is not None:
                kwargs["integration_key"] = integration_key
            if is_enabled is not None:
                kwargs["is_enabled"] = is_enabled
            if max_prompts is not None:
                kwargs["max_prompts"] = max_prompts
            if owner is not None:
                kwargs["owner"] = owner
            if push_info is not None:
                kwargs["push_info"] = push_info
            if secret_key is not None:
                kwargs["secret_key"] = secret_key
            if status is not None:
                kwargs["status"] = status

            resource = Duo(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create Duo: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo profile for a cluster or an SVM.
### Related ONTAP commands
* `security login duo modify`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duo modify")
        async def duo_modify(
        ) -> ResourceTable:
            """Modify an instance of a Duo resource

            Args:
                api_host: The URL at which the Duo API is hosted.
                query_api_host: The URL at which the Duo API is hosted.
                auto_push: Automatically sends a push notification for authentication when using Duo.
                query_auto_push: Automatically sends a push notification for authentication when using Duo.
                comment: Comment for the Duo profile.
                query_comment: Comment for the Duo profile.
                fail_mode: Determines the behavior of the system when it cannot communicate with the Duo service.
                query_fail_mode: Determines the behavior of the system when it cannot communicate with the Duo service.
                fingerprint: The SHA fingerprint corresponding to the Duo secret key.
                query_fingerprint: The SHA fingerprint corresponding to the Duo secret key.
                http_proxy: Specifies the HTTP proxy server to be used when connecting to the Duo service.
                query_http_proxy: Specifies the HTTP proxy server to be used when connecting to the Duo service.
                integration_key: The Integration Key associated with the Duo profile.
                query_integration_key: The Integration Key associated with the Duo profile.
                is_enabled: Indicates whether the Duo authentication feature is active or inactive.
                query_is_enabled: Indicates whether the Duo authentication feature is active or inactive.
                max_prompts: The maximum number of authentication attempts allowed for a user before the process is terminated.
                query_max_prompts: The maximum number of authentication attempts allowed for a user before the process is terminated.
                push_info: Additional information sent along with the push notification for Duo authentication.
                query_push_info: Additional information sent along with the push notification for Duo authentication.
                secret_key: The Secret Key associated with the Duo profile.
                query_secret_key: The Secret Key associated with the Duo profile.
                status: Information on the reachability status of Duo.
                query_status: Information on the reachability status of Duo.
            """

            kwargs = {}
            changes = {}
            if query_api_host is not None:
                kwargs["api_host"] = query_api_host
            if query_auto_push is not None:
                kwargs["auto_push"] = query_auto_push
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_fail_mode is not None:
                kwargs["fail_mode"] = query_fail_mode
            if query_fingerprint is not None:
                kwargs["fingerprint"] = query_fingerprint
            if query_http_proxy is not None:
                kwargs["http_proxy"] = query_http_proxy
            if query_integration_key is not None:
                kwargs["integration_key"] = query_integration_key
            if query_is_enabled is not None:
                kwargs["is_enabled"] = query_is_enabled
            if query_max_prompts is not None:
                kwargs["max_prompts"] = query_max_prompts
            if query_push_info is not None:
                kwargs["push_info"] = query_push_info
            if query_secret_key is not None:
                kwargs["secret_key"] = query_secret_key
            if query_status is not None:
                kwargs["status"] = query_status

            if api_host is not None:
                changes["api_host"] = api_host
            if auto_push is not None:
                changes["auto_push"] = auto_push
            if comment is not None:
                changes["comment"] = comment
            if fail_mode is not None:
                changes["fail_mode"] = fail_mode
            if fingerprint is not None:
                changes["fingerprint"] = fingerprint
            if http_proxy is not None:
                changes["http_proxy"] = http_proxy
            if integration_key is not None:
                changes["integration_key"] = integration_key
            if is_enabled is not None:
                changes["is_enabled"] = is_enabled
            if max_prompts is not None:
                changes["max_prompts"] = max_prompts
            if push_info is not None:
                changes["push_info"] = push_info
            if secret_key is not None:
                changes["secret_key"] = secret_key
            if status is not None:
                changes["status"] = status

            if hasattr(Duo, "find"):
                resource = Duo.find(
                    **kwargs
                )
            else:
                resource = Duo()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify Duo: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Duo profile of the SVM or cluster.
### Related ONTAP commands
* `security login duo delete`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duo delete")
        async def duo_delete(
        ) -> None:
            """Delete an instance of a Duo resource

            Args:
                api_host: The URL at which the Duo API is hosted.
                auto_push: Automatically sends a push notification for authentication when using Duo.
                comment: Comment for the Duo profile.
                fail_mode: Determines the behavior of the system when it cannot communicate with the Duo service.
                fingerprint: The SHA fingerprint corresponding to the Duo secret key.
                http_proxy: Specifies the HTTP proxy server to be used when connecting to the Duo service.
                integration_key: The Integration Key associated with the Duo profile.
                is_enabled: Indicates whether the Duo authentication feature is active or inactive.
                max_prompts: The maximum number of authentication attempts allowed for a user before the process is terminated.
                push_info: Additional information sent along with the push notification for Duo authentication.
                secret_key: The Secret Key associated with the Duo profile.
                status: Information on the reachability status of Duo.
            """

            kwargs = {}
            if api_host is not None:
                kwargs["api_host"] = api_host
            if auto_push is not None:
                kwargs["auto_push"] = auto_push
            if comment is not None:
                kwargs["comment"] = comment
            if fail_mode is not None:
                kwargs["fail_mode"] = fail_mode
            if fingerprint is not None:
                kwargs["fingerprint"] = fingerprint
            if http_proxy is not None:
                kwargs["http_proxy"] = http_proxy
            if integration_key is not None:
                kwargs["integration_key"] = integration_key
            if is_enabled is not None:
                kwargs["is_enabled"] = is_enabled
            if max_prompts is not None:
                kwargs["max_prompts"] = max_prompts
            if push_info is not None:
                kwargs["push_info"] = push_info
            if secret_key is not None:
                kwargs["secret_key"] = secret_key
            if status is not None:
                kwargs["status"] = status

            if hasattr(Duo, "find"):
                resource = Duo.find(
                    **kwargs
                )
            else:
                resource = Duo()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete Duo: %s" % err)


