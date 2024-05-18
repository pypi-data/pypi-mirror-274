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


__all__ = ["SvmMigrationVolume", "SvmMigrationVolumeSchema"]
__pdoc__ = {
    "SvmMigrationVolumeSchema.resource": False,
    "SvmMigrationVolumeSchema.opts": False,
    "SvmMigrationVolume.svm_migration_volume_show": False,
    "SvmMigrationVolume.svm_migration_volume_create": False,
    "SvmMigrationVolume.svm_migration_volume_modify": False,
    "SvmMigrationVolume.svm_migration_volume_delete": False,
}


class SvmMigrationVolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationVolume object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the svm_migration_volume."""

    errors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_messages.SvmMigrationMessagesSchema", unknown=EXCLUDE, allow_none=True), data_key="errors", allow_none=True)
    r""" List of transfer errors"""

    healthy = marshmallow_fields.Boolean(
        data_key="healthy",
        allow_none=True,
    )
    r""" Indicates whether the volume transfer relationship is healthy."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the svm_migration_volume."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the svm_migration_volume."""

    transfer_state = marshmallow_fields.Str(
        data_key="transfer_state",
        validate=enum_validation(['Idle', 'Transferring', 'Aborting', 'OutOfSync', 'InSync', 'Transitioning', 'ReadyForCutoverPreCommit', 'CutoverPreCommitting', 'CuttingOver']),
        allow_none=True,
    )
    r""" Status of the transfer.

Valid choices:

* Idle
* Transferring
* Aborting
* OutOfSync
* InSync
* Transitioning
* ReadyForCutoverPreCommit
* CutoverPreCommitting
* CuttingOver"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the svm_migration_volume."""

    @property
    def resource(self):
        return SvmMigrationVolume

    gettable_fields = [
        "links",
        "errors",
        "healthy",
        "node.links",
        "node.name",
        "node.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "transfer_state",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,errors,healthy,node.links,node.name,node.uuid,svm.links,svm.name,svm.uuid,transfer_state,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "healthy",
    ]
    """healthy,"""

    postable_fields = [
        "healthy",
    ]
    """healthy,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SvmMigrationVolume.get_collection(fields=field)]
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
            raise NetAppRestError("SvmMigrationVolume modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SvmMigrationVolume(Resource):
    r""" Volume transfer information """

    _schema = SvmMigrationVolumeSchema
    _path = "/api/svm/migrations/{svm_migration[uuid]}/volumes"
    _keys = ["svm_migration.uuid", "volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the transfer status of the volumes in the SVM.
### Related ONTAP commands
* `vserver migrate show-volume`
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="svm migration volume show")
        def svm_migration_volume_show(
            svm_migration_uuid,
            healthy: Choices.define(_get_field_list("healthy"), cache_choices=True, inexact=True)=None,
            transfer_state: Choices.define(_get_field_list("transfer_state"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["healthy", "transfer_state", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SvmMigrationVolume resources

            Args:
                healthy: Indicates whether the volume transfer relationship is healthy.
                transfer_state: Status of the transfer.
            """

            kwargs = {}
            if healthy is not None:
                kwargs["healthy"] = healthy
            if transfer_state is not None:
                kwargs["transfer_state"] = transfer_state
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SvmMigrationVolume.get_collection(
                svm_migration_uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SvmMigrationVolume resources that match the provided query"""
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
        """Returns a list of RawResources that represent SvmMigrationVolume resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the transfer status of the volumes in the SVM.
### Related ONTAP commands
* `vserver migrate show-volume`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the volume transfer status of the specified volume.uuid.
### Related ONTAP commands
* `vserver migrate show-volume`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





