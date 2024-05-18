r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Retrieves cluster-wide storage details across the different tiers.
Storage details include storage efficiency, block storage and cloud storage information.
---
Example
### Retrieving cluster-wide storage details
The following example shows the details returned for a GET request on cluster-wide storage:
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSpace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSpace()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ClusterSpace(
    {
        "efficiency_without_snapshots": {
            "logical_used": 167936,
            "savings": 0,
            "ratio": 1.0,
        },
        "block_storage": {
            "inactive_data": 0,
            "physical_used": 1838284800,
            "available": 49855799296,
            "used": 6269812736,
            "medias": [
                {
                    "efficiency_without_snapshots": {
                        "logical_used": 0,
                        "savings": 0,
                        "ratio": 1.0,
                    },
                    "physical_used": 1832886272,
                    "available": 3728039936,
                    "used": 6163390464,
                    "efficiency": {"logical_used": 0, "savings": 0, "ratio": 1.0},
                    "type": "ssd",
                    "size": 9891430400,
                    "efficiency_without_snapshots_flexclones": {
                        "logical_used": 0,
                        "savings": 0,
                        "ratio": 1.0,
                    },
                },
                {
                    "efficiency_without_snapshots": {
                        "logical_used": 167936,
                        "savings": 0,
                        "ratio": 1.0,
                    },
                    "physical_used": 5398528,
                    "available": 46127759360,
                    "used": 106422272,
                    "efficiency": {
                        "logical_used": 1212416,
                        "savings": 282624,
                        "ratio": 1.303964757709251,
                    },
                    "type": "vmdisk",
                    "size": 46234181632,
                    "efficiency_without_snapshots_flexclones": {
                        "logical_used": 167936,
                        "savings": 0,
                        "ratio": 1.0,
                    },
                },
            ],
            "size": 56125612032,
        },
        "efficiency": {
            "logical_used": 1212416,
            "savings": 143360,
            "ratio": 1.134099616858238,
        },
        "efficiency_without_snapshots_flexclones": {
            "logical_used": 167936,
            "savings": 0,
            "ratio": 1.0,
        },
    }
)

```
</div>
</div>

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


__all__ = ["ClusterSpace", "ClusterSpaceSchema"]
__pdoc__ = {
    "ClusterSpaceSchema.resource": False,
    "ClusterSpaceSchema.opts": False,
    "ClusterSpace.cluster_space_show": False,
    "ClusterSpace.cluster_space_create": False,
    "ClusterSpace.cluster_space_modify": False,
    "ClusterSpace.cluster_space_delete": False,
}


class ClusterSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpace object"""

    block_storage = marshmallow_fields.Nested("netapp_ontap.models.cluster_space_block_storage.ClusterSpaceBlockStorageSchema", data_key="block_storage", unknown=EXCLUDE, allow_none=True)
    r""" The block_storage field of the cluster_space."""

    cloud_storage = marshmallow_fields.Nested("netapp_ontap.models.cluster_space_cloud_storage.ClusterSpaceCloudStorageSchema", data_key="cloud_storage", unknown=EXCLUDE, allow_none=True)
    r""" The cloud_storage field of the cluster_space."""

    efficiency = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency field of the cluster_space."""

    efficiency_without_snapshots = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency_without_snapshots", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency_without_snapshots field of the cluster_space."""

    efficiency_without_snapshots_flexclones = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency_without_snapshots_flexclones", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency_without_snapshots_flexclones field of the cluster_space."""

    @property
    def resource(self):
        return ClusterSpace

    gettable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,"""

    patchable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,"""

    postable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ClusterSpace.get_collection(fields=field)]
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
            raise NetAppRestError("ClusterSpace modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ClusterSpace(Resource):
    r""" Provides information on cluster-wide storage details across the different tiers. Storage details include storage efficiency, block storage and cloud storage information. """

    _schema = ClusterSpaceSchema
    _path = "/api/storage/cluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves cluster-wide storage details across the different tiers. By default, this endpoint returns all fields.
Storage details include storage efficiency, block storage and cloud storage information.
Supports the following roles: admin, and readonly.

### Learn more
* [`DOC /storage/cluster`](#docs-storage-storage_cluster)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="cluster space show")
        def cluster_space_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single ClusterSpace resource

            Args:
            """

            kwargs = {}
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = ClusterSpace(
                **kwargs
            )
            resource.get()
            return [resource]





