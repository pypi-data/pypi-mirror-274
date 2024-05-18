r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to restore a directory from a volume Snapshot copy without having to use data copy. The directory in the Snapshot copy contains sub-directories and files.<br/>
When a directory from a volume Snapshot copy is restored, all the directory entries (dentries) in the source should remain as they are (except for the junction path inodes). The dentries in the restored directory contain new inodes which are in the AFS (Active File System).<br/>
The newly created inodes in the AFS have the same attributes as those in the source Snapshot copy.<br/>
## Directory restore API
The following API is used to perform the following operations:

* POST      /api/storage/directory-restore"""

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


__all__ = ["DirectoryRestore", "DirectoryRestoreSchema"]
__pdoc__ = {
    "DirectoryRestoreSchema.resource": False,
    "DirectoryRestoreSchema.opts": False,
    "DirectoryRestore.directory_restore_show": False,
    "DirectoryRestore.directory_restore_create": False,
    "DirectoryRestore.directory_restore_modify": False,
    "DirectoryRestore.directory_restore_delete": False,
}


class DirectoryRestoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DirectoryRestore object"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Source from where the directory is restored.

Example: src_file1, dir1/src_file2, ./.snapshot/snap1/src_file3"""

    restore_path = marshmallow_fields.Str(
        data_key="restore_path",
        allow_none=True,
    )
    r""" Destination directory where the new directory tree is created.

Example: dest_file1, dir1/dest_file2"""

    snapshot = marshmallow_fields.Str(
        data_key="snapshot",
        allow_none=True,
    )
    r""" Name of the volume Snapshot copy from which the directory is restored."""

    volume = marshmallow_fields.Str(
        data_key="volume",
        allow_none=True,
    )
    r""" Name of the volume from which the Snapshot copy is used for directory restore."""

    vserver = marshmallow_fields.Str(
        data_key="vserver",
        allow_none=True,
    )
    r""" Name of the SVM."""

    @property
    def resource(self):
        return DirectoryRestore

    gettable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

    patchable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

    postable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in DirectoryRestore.get_collection(fields=field)]
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
            raise NetAppRestError("DirectoryRestore modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class DirectoryRestore(Resource):
    r""" Restores a directory from a volume Snapshot copy. """

    _schema = DirectoryRestoreSchema
    _path = "/api/storage/directory-restore"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["DirectoryRestore"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DirectoryRestore"], NetAppResponse]:
        r"""Restores the source directory from the volume Snapshot copy on the destination directory.
### Required Properties
* `vserver`
* `volume.name`
* `snapshot.name`
* `source_path`
* `restore_path`
### Related ONTAP commands
* `volume snapshot directory-restore start`
```
# The API:
/api/storage/directory-restore
# The call:
curl -X POST "https://<mgmt_ip>/api/storage/directory-restore" -H "accept: application/hal+json" -d '{"svm":"vs1", "volume": "vol1", "snapshot": "sp1", "path": "/aaaa", "restore_path": "/bbbb"}'
# The response:
{
  "job": {
    "uuid": "23b5ff3a-4743-11ee-a08d-005056bb9d00",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/23b5ff3a-4743-11ee-a08d-005056bb9d00"
      }
    }
  }
}
```

### Learn more
* [`DOC /storage/directory-restore`](#docs-storage-storage_directory-restore)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)




    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restores the source directory from the volume Snapshot copy on the destination directory.
### Required Properties
* `vserver`
* `volume.name`
* `snapshot.name`
* `source_path`
* `restore_path`
### Related ONTAP commands
* `volume snapshot directory-restore start`
```
# The API:
/api/storage/directory-restore
# The call:
curl -X POST "https://<mgmt_ip>/api/storage/directory-restore" -H "accept: application/hal+json" -d '{"svm":"vs1", "volume": "vol1", "snapshot": "sp1", "path": "/aaaa", "restore_path": "/bbbb"}'
# The response:
{
  "job": {
    "uuid": "23b5ff3a-4743-11ee-a08d-005056bb9d00",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/23b5ff3a-4743-11ee-a08d-005056bb9d00"
      }
    }
  }
}
```

### Learn more
* [`DOC /storage/directory-restore`](#docs-storage-storage_directory-restore)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="directory restore create")
        async def directory_restore_create(
        ) -> ResourceTable:
            """Create an instance of a DirectoryRestore resource

            Args:
                path: Source from where the directory is restored.
                restore_path: Destination directory where the new directory tree is created.
                snapshot: Name of the volume Snapshot copy from which the directory is restored.
                volume: Name of the volume from which the Snapshot copy is used for directory restore.
                vserver: Name of the SVM.
            """

            kwargs = {}
            if path is not None:
                kwargs["path"] = path
            if restore_path is not None:
                kwargs["restore_path"] = restore_path
            if snapshot is not None:
                kwargs["snapshot"] = snapshot
            if volume is not None:
                kwargs["volume"] = volume
            if vserver is not None:
                kwargs["vserver"] = vserver

            resource = DirectoryRestore(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create DirectoryRestore: %s" % err)
            return [resource]




