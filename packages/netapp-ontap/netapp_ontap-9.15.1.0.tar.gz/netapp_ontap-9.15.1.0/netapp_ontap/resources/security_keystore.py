r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A keystore describes a key-manager configuration, specifically the type of key-manager and whether the configuration is currently enabled for the configured SVM.<p/>
## Examples
---
### Retrieving information for all configured key managers
The following example shows how to retrieve information about all configured key managers.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeystore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityKeystore.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityKeystore(
        {
            "configuration": {
                "_links": {
                    "self": {
                        "href": "/api/security/azure-key-vaults/33421d82-0a8d-11ec-ae88-005056bb5955"
                    }
                },
                "name": "default",
                "uuid": "33421d82-0a8d-11ec-ae88-005056bb5955",
            },
            "uuid": "33421d82-0a8d-11ec-ae88-005056bb5955",
            "enabled": True,
            "type": "akv",
            "location": "external",
        }
    ),
    SecurityKeystore(
        {
            "configuration": {
                "_links": {
                    "self": {
                        "href": "/api/security/key-managers/46a0b20a-0a8d-11ec-ae88-005056bb5955"
                    }
                },
                "name": "default",
                "uuid": "46a0b20a-0a8d-11ec-ae88-005056bb5955",
            },
            "uuid": "46a0b20a-0a8d-11ec-ae88-005056bb5955",
            "enabled": False,
            "type": "kmip",
            "location": "external",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific keystore by its UUID
The following example shows how to retrieve information about a specific keystore.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeystore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeystore(uuid="33421d82-0a8d-11ec-ae88-005056bb5955")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityKeystore(
    {
        "configuration": {
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/33421d82-0a8d-11ec-ae88-005056bb5955"
                }
            },
            "name": "default",
            "uuid": "33421d82-0a8d-11ec-ae88-005056bb5955",
        },
        "uuid": "33421d82-0a8d-11ec-ae88-005056bb5955",
        "enabled": True,
        "type": "akv",
        "location": "external",
    }
)

```
</div>
</div>

---
### Enabling a specific keystore configuration
The following example shows how to enable a specific keystore configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeystore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeystore(uuid="33421d82-0a8d-11ec-ae88-005056bb5955")
    resource.enabled = True
    resource.patch()

```

---
### Deleting a specific keystore configuration
The following example shows how to delete a specific keystore configuration. Only an inactive configuration can be deleted.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeystore

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeystore(uuid="33421d82-0a8d-11ec-ae88-005056bb5955")
    resource.delete()

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


__all__ = ["SecurityKeystore", "SecurityKeystoreSchema"]
__pdoc__ = {
    "SecurityKeystoreSchema.resource": False,
    "SecurityKeystoreSchema.opts": False,
    "SecurityKeystore.security_keystore_show": False,
    "SecurityKeystore.security_keystore_create": False,
    "SecurityKeystore.security_keystore_modify": False,
    "SecurityKeystore.security_keystore_delete": False,
}


class SecurityKeystoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeystore object"""

    configuration = marshmallow_fields.Nested("netapp_ontap.models.security_keystore_configuration.SecurityKeystoreConfigurationSchema", data_key="configuration", unknown=EXCLUDE, allow_none=True)
    r""" The configuration field of the security_keystore."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the configuration is enabled."""

    location = marshmallow_fields.Str(
        data_key="location",
        validate=enum_validation(['onboard', 'external']),
        allow_none=True,
    )
    r""" Indicates whether the keystore is onboard or external. * 'onboard' - Onboard Key Database * 'external' - External Key Database, including KMIP and Cloud Key Management Systems


Valid choices:

* onboard
* external"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the security_keystore."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the security_keystore."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['okm', 'kmip', 'akv', 'gcp', 'aws', 'ikp']),
        allow_none=True,
    )
    r""" Type of keystore that is configured: * 'okm' - Onboard Key Manager * 'kmip' - External Key Manager * 'akv' - Azure Key Vault Key Management Service * 'gcp' - Google Cloud Platform Key Management Service * 'aws' - Amazon Web Service Key Management Service * 'ikp' - IBM Key Protect Key Management Service


Valid choices:

* okm
* kmip
* akv
* gcp
* aws
* ikp"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the security_keystore."""

    @property
    def resource(self):
        return SecurityKeystore

    gettable_fields = [
        "configuration",
        "enabled",
        "location",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """configuration,enabled,location,scope,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "enabled",
        "scope",
    ]
    """enabled,scope,"""

    postable_fields = [
        "scope",
    ]
    """scope,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SecurityKeystore.get_collection(fields=field)]
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
            raise NetAppRestError("SecurityKeystore modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SecurityKeystore(Resource):
    """Allows interaction with SecurityKeystore objects on the host"""

    _schema = SecurityKeystoreSchema
    _path = "/api/security/key-stores"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves keystores.
### Related ONTAP commands
* `security key-manager show-key-store`
* `security key-manager keystore show`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="security keystore show")
        def security_keystore_show(
            fields: List[Choices.define(["enabled", "location", "scope", "type", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SecurityKeystore resources

            Args:
                enabled: Indicates whether the configuration is enabled.
                location: Indicates whether the keystore is onboard or external. * 'onboard' - Onboard Key Database * 'external' - External Key Database, including KMIP and Cloud Key Management Systems 
                scope: 
                type: Type of keystore that is configured: * 'okm' - Onboard Key Manager * 'kmip' - External Key Manager * 'akv' - Azure Key Vault Key Management Service * 'gcp' - Google Cloud Platform Key Management Service * 'aws' - Amazon Web Service Key Management Service * 'ikp' - IBM Key Protect Key Management Service 
                uuid: 
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if location is not None:
                kwargs["location"] = location
            if scope is not None:
                kwargs["scope"] = scope
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SecurityKeystore.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityKeystore resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityKeystore resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityKeystore"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Enables a keystore configuration
### Related ONTAP commands
* `security key-manager keystore enable`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityKeystore"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an inactive keystore configuration.
### Related ONTAP commands
* `security key-manager keystore delete`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves keystores.
### Related ONTAP commands
* `security key-manager show-key-store`
* `security key-manager keystore show`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of the keystore configuration with the specified UUID.
### Related ONTAP commands
* `security key-manager keystore show`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Enables a keystore configuration
### Related ONTAP commands
* `security key-manager keystore enable`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="security keystore modify")
        async def security_keystore_modify(
        ) -> ResourceTable:
            """Modify an instance of a SecurityKeystore resource

            Args:
                enabled: Indicates whether the configuration is enabled.
                query_enabled: Indicates whether the configuration is enabled.
                location: Indicates whether the keystore is onboard or external. * 'onboard' - Onboard Key Database * 'external' - External Key Database, including KMIP and Cloud Key Management Systems 
                query_location: Indicates whether the keystore is onboard or external. * 'onboard' - Onboard Key Database * 'external' - External Key Database, including KMIP and Cloud Key Management Systems 
                scope: 
                query_scope: 
                type: Type of keystore that is configured: * 'okm' - Onboard Key Manager * 'kmip' - External Key Manager * 'akv' - Azure Key Vault Key Management Service * 'gcp' - Google Cloud Platform Key Management Service * 'aws' - Amazon Web Service Key Management Service * 'ikp' - IBM Key Protect Key Management Service 
                query_type: Type of keystore that is configured: * 'okm' - Onboard Key Manager * 'kmip' - External Key Manager * 'akv' - Azure Key Vault Key Management Service * 'gcp' - Google Cloud Platform Key Management Service * 'aws' - Amazon Web Service Key Management Service * 'ikp' - IBM Key Protect Key Management Service 
                uuid: 
                query_uuid: 
            """

            kwargs = {}
            changes = {}
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled
            if query_location is not None:
                kwargs["location"] = query_location
            if query_scope is not None:
                kwargs["scope"] = query_scope
            if query_type is not None:
                kwargs["type"] = query_type
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if enabled is not None:
                changes["enabled"] = enabled
            if location is not None:
                changes["location"] = location
            if scope is not None:
                changes["scope"] = scope
            if type is not None:
                changes["type"] = type
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(SecurityKeystore, "find"):
                resource = SecurityKeystore.find(
                    **kwargs
                )
            else:
                resource = SecurityKeystore()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify SecurityKeystore: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an inactive keystore configuration.
### Related ONTAP commands
* `security key-manager keystore delete`

### Learn more
* [`DOC /security/key-stores`](#docs-security-security_key-stores)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="security keystore delete")
        async def security_keystore_delete(
        ) -> None:
            """Delete an instance of a SecurityKeystore resource

            Args:
                enabled: Indicates whether the configuration is enabled.
                location: Indicates whether the keystore is onboard or external. * 'onboard' - Onboard Key Database * 'external' - External Key Database, including KMIP and Cloud Key Management Systems 
                scope: 
                type: Type of keystore that is configured: * 'okm' - Onboard Key Manager * 'kmip' - External Key Manager * 'akv' - Azure Key Vault Key Management Service * 'gcp' - Google Cloud Platform Key Management Service * 'aws' - Amazon Web Service Key Management Service * 'ikp' - IBM Key Protect Key Management Service 
                uuid: 
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if location is not None:
                kwargs["location"] = location
            if scope is not None:
                kwargs["scope"] = scope
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(SecurityKeystore, "find"):
                resource = SecurityKeystore.find(
                    **kwargs
                )
            else:
                resource = SecurityKeystore()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete SecurityKeystore: %s" % err)


