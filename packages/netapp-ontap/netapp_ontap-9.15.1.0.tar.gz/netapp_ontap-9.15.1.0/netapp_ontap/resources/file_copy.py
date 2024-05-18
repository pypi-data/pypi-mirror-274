r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

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


__all__ = ["FileCopy", "FileCopySchema"]
__pdoc__ = {
    "FileCopySchema.resource": False,
    "FileCopySchema.opts": False,
    "FileCopy.file_copy_show": False,
    "FileCopy.file_copy_create": False,
    "FileCopy.file_copy_modify": False,
    "FileCopy.file_copy_delete": False,
}


class FileCopySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileCopy object"""

    cutover_time = Size(
        data_key="cutover_time",
        allow_none=True,
    )
    r""" The maximum amount of time (in seconds) that the source can be quiesced before a destination file must be made available for read-write traffic.

Example: 10"""

    files_to_copy = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.file_copy_files_to_copy.FileCopyFilesToCopySchema", unknown=EXCLUDE, allow_none=True), data_key="files_to_copy", allow_none=True)
    r""" A list of source files along with the destinations they are copied to. If the terminal path component of the destination is a directory, then the source file's basename is replicated in that directory."""

    hold_quiescence = marshmallow_fields.Boolean(
        data_key="hold_quiescence",
        allow_none=True,
    )
    r""" Specifies whether the source file should be held quiescent for the duration of the copy operation."""

    max_throughput = Size(
        data_key="max_throughput",
        allow_none=True,
    )
    r""" Maximum amount of data, in bytes that can be transferred per second in support of this operation. A non-zero value less than 1MB/s is set to 1MB/s. A non-zero value greater than 1MB/s is truncated to the nearest integral megabyte value. If unspecified, the default value is "0" which means no range is set for the data transfer."""

    reference_cutover_time = Size(
        data_key="reference_cutover_time",
        allow_none=True,
    )
    r""" The maximum amount of time (in seconds) that the source reference file can be quiesced before the corresponding destination file must be made available for read-write traffic.

Example: 10"""

    reference_path = marshmallow_fields.Str(
        data_key="reference_path",
        allow_none=True,
    )
    r""" The source reference file. If a reference file is specified, data for other files being copied will be transferred as a difference from the reference file. This can save bandwidth and destination storage if the specified source files share blocks. If provided, this input must match one of the source file paths. This input need not be provided if only one source file is specified.

Example: svm1:volume1/file1"""

    @property
    def resource(self):
        return FileCopy

    gettable_fields = [
        "cutover_time",
        "files_to_copy",
        "hold_quiescence",
        "max_throughput",
        "reference_cutover_time",
        "reference_path",
    ]
    """cutover_time,files_to_copy,hold_quiescence,max_throughput,reference_cutover_time,reference_path,"""

    patchable_fields = [
        "cutover_time",
        "files_to_copy",
        "hold_quiescence",
        "max_throughput",
        "reference_cutover_time",
        "reference_path",
    ]
    """cutover_time,files_to_copy,hold_quiescence,max_throughput,reference_cutover_time,reference_path,"""

    postable_fields = [
        "cutover_time",
        "files_to_copy",
        "hold_quiescence",
        "max_throughput",
        "reference_cutover_time",
        "reference_path",
    ]
    """cutover_time,files_to_copy,hold_quiescence,max_throughput,reference_cutover_time,reference_path,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in FileCopy.get_collection(fields=field)]
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
            raise NetAppRestError("FileCopy modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class FileCopy(Resource):
    r""" File copy """

    _schema = FileCopySchema
    _path = "/api/storage/file/copy"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["FileCopy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FileCopy"], NetAppResponse]:
        r"""Starts a file copy operation. Only supported on flexible volumes.
## Required properties
* `files_to_copy` - List of files with the destination they are to be copied to.
## Default property values
* `cutover_time` - _10_
* `hold_quiescence` - _false_
* `max_throughput` - _0_
* `reference_cutover_time` - _10_
## Related ONTAP commands
* `volume file copy start`
## Examples
### Copying two files
The POST request is used to copy file(s).
```
# The API:
/api/storage/file/copy
# The call:
curl -X POST  "https://<mgmt-ip>/api/storage/file/copy" -H "accept: application/hal+json" -d '{"files_to_copy":[{"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f1"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f1"}}, {"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f2"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f2"}}]}'
# The response:
{
  "job": {
    "uuid": "b89bc5dd-94a3-11e8-a7a3-0050568edf84",
    "_links": {
       "self": {
         "href": "/api/cluster/jobs/b89bc5dd-94a3-11e8-a7a3-0050568edf84"
       }
     }
   }
}
```
"""
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
        r"""Starts a file copy operation. Only supported on flexible volumes.
## Required properties
* `files_to_copy` - List of files with the destination they are to be copied to.
## Default property values
* `cutover_time` - _10_
* `hold_quiescence` - _false_
* `max_throughput` - _0_
* `reference_cutover_time` - _10_
## Related ONTAP commands
* `volume file copy start`
## Examples
### Copying two files
The POST request is used to copy file(s).
```
# The API:
/api/storage/file/copy
# The call:
curl -X POST  "https://<mgmt-ip>/api/storage/file/copy" -H "accept: application/hal+json" -d '{"files_to_copy":[{"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f1"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f1"}}, {"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f2"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f2"}}]}'
# The response:
{
  "job": {
    "uuid": "b89bc5dd-94a3-11e8-a7a3-0050568edf84",
    "_links": {
       "self": {
         "href": "/api/cluster/jobs/b89bc5dd-94a3-11e8-a7a3-0050568edf84"
       }
     }
   }
}
```
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="file copy create")
        async def file_copy_create(
        ) -> ResourceTable:
            """Create an instance of a FileCopy resource

            Args:
                cutover_time: The maximum amount of time (in seconds) that the source can be quiesced before a destination file must be made available for read-write traffic.
                files_to_copy: A list of source files along with the destinations they are copied to. If the terminal path component of the destination is a directory, then the source file's basename is replicated in that directory.
                hold_quiescence: Specifies whether the source file should be held quiescent for the duration of the copy operation.
                max_throughput: Maximum amount of data, in bytes that can be transferred per second in support of this operation. A non-zero value less than 1MB/s is set to 1MB/s. A non-zero value greater than 1MB/s is truncated to the nearest integral megabyte value. If unspecified, the default value is \"0\" which means no range is set for the data transfer.
                reference_cutover_time: The maximum amount of time (in seconds) that the source reference file can be quiesced before the corresponding destination file must be made available for read-write traffic.
                reference_path: The source reference file. If a reference file is specified, data for other files being copied will be transferred as a difference from the reference file. This can save bandwidth and destination storage if the specified source files share blocks. If provided, this input must match one of the source file paths. This input need not be provided if only one source file is specified.
            """

            kwargs = {}
            if cutover_time is not None:
                kwargs["cutover_time"] = cutover_time
            if files_to_copy is not None:
                kwargs["files_to_copy"] = files_to_copy
            if hold_quiescence is not None:
                kwargs["hold_quiescence"] = hold_quiescence
            if max_throughput is not None:
                kwargs["max_throughput"] = max_throughput
            if reference_cutover_time is not None:
                kwargs["reference_cutover_time"] = reference_cutover_time
            if reference_path is not None:
                kwargs["reference_path"] = reference_path

            resource = FileCopy(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create FileCopy: %s" % err)
            return [resource]




