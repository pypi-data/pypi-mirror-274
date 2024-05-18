r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Quality of Service Options
A QoS option represents a configuration detail that is used by QoS.
<br />
---
## Examples
### Retrieving a QoS option from the cluster
The following example retrieves the QoS option in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosOption

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QosOption()
    resource.get(return_timeout=0)
    print(resource)

```

---
### 2) Update a QoS option
The following example shows how to modify the background task reserve policy to 40%.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosOption

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QosOption()
    resource.background_task_reserve = 40
    resource.patch(hydrate=True, return_timeout=0)

```

----"""

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


__all__ = ["QosOption", "QosOptionSchema"]
__pdoc__ = {
    "QosOptionSchema.resource": False,
    "QosOptionSchema.opts": False,
    "QosOption.qos_option_show": False,
    "QosOption.qos_option_create": False,
    "QosOption.qos_option_modify": False,
    "QosOption.qos_option_delete": False,
}


class QosOptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosOption object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the qos_option."""

    background_task_reserve = Size(
        data_key="background_task_reserve",
        allow_none=True,
    )
    r""" Percentage reserve for critical background tasks.

Example: 33"""

    @property
    def resource(self):
        return QosOption

    gettable_fields = [
        "links",
        "background_task_reserve",
    ]
    """links,background_task_reserve,"""

    patchable_fields = [
        "background_task_reserve",
    ]
    """background_task_reserve,"""

    postable_fields = [
        "background_task_reserve",
    ]
    """background_task_reserve,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in QosOption.get_collection(fields=field)]
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
            raise NetAppRestError("QosOption modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class QosOption(Resource):
    """Allows interaction with QosOption objects on the host"""

    _schema = QosOptionSchema
    _path = "/api/storage/qos/qos-options"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves QoS options.
This option is available only at diagnostic privilege level and above.
### Related ONTAP commands
* `qos settings cluster-options show`

### Learn more
* [`DOC /storage/qos/qos-options`](#docs-storage-storage_qos_qos-options)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="qos option show")
        def qos_option_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single QosOption resource

            Args:
                background_task_reserve: Percentage reserve for critical background tasks.
            """

            kwargs = {}
            if background_task_reserve is not None:
                kwargs["background_task_reserve"] = background_task_reserve
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = QosOption(
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
        r"""Update a specific QoS option.
This option is available only at diagnostic privilege level and above.
### Related ONTAP commands
* `qos settings cluster-options modify`

### Learn more
* [`DOC /storage/qos/qos-options`](#docs-storage-storage_qos_qos-options)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="qos option modify")
        async def qos_option_modify(
        ) -> ResourceTable:
            """Modify an instance of a QosOption resource

            Args:
                background_task_reserve: Percentage reserve for critical background tasks.
                query_background_task_reserve: Percentage reserve for critical background tasks.
            """

            kwargs = {}
            changes = {}
            if query_background_task_reserve is not None:
                kwargs["background_task_reserve"] = query_background_task_reserve

            if background_task_reserve is not None:
                changes["background_task_reserve"] = background_task_reserve

            if hasattr(QosOption, "find"):
                resource = QosOption.find(
                    **kwargs
                )
            else:
                resource = QosOption()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify QosOption: %s" % err)



