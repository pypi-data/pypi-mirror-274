r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnapshotResponseRecords", "ConsistencyGroupSnapshotResponseRecordsSchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotResponseRecordsSchema.resource": False,
    "ConsistencyGroupSnapshotResponseRecordsSchema.opts": False,
    "ConsistencyGroupSnapshotResponseRecords": False,
}


class ConsistencyGroupSnapshotResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshotResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_snapshot_response_records. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" Comment for the Snapshot copy.


Example: My Snapshot copy comment """

    consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="consistency_group", allow_none=True)
    r""" The consistency_group field of the consistency_group_snapshot_response_records. """

    consistency_type = marshmallow_fields.Str(data_key="consistency_type", allow_none=True)
    r""" Consistency type. This is for categorization purposes only. A Snapshot copy should not be set to 'application consistent' unless the host application is quiesced for the Snapshot copy. Valid in POST.


Valid choices:

* crash
* application """

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" Time the snapshot copy was created


Example: 2020-10-25T11:20:00.000+0000 """

    is_partial = marshmallow_fields.Boolean(data_key="is_partial", allow_none=True)
    r""" Indicates whether the Snapshot copy taken is partial or not.


Example: false """

    missing_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="missing_volumes", allow_none=True)
    r""" List of volumes which are not in the Snapshot copy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the Snapshot copy. """

    snapmirror_label = marshmallow_fields.Str(data_key="snapmirror_label", allow_none=True)
    r""" Snapmirror Label for the Snapshot copy.


Example: sm_label """

    snapshot_volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_volume_snapshot.ConsistencyGroupVolumeSnapshotSchema", unknown=EXCLUDE, allow_none=True), data_key="snapshot_volumes", allow_none=True)
    r""" List of volume and snapshot identifiers for each volume in the Snapshot copy. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The SVM in which the consistency group is located. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the Snapshot copy. The UUID is generated
by ONTAP when the Snapshot copy is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    write_fence = marshmallow_fields.Boolean(data_key="write_fence", allow_none=True)
    r""" Specifies whether a write fence will be taken when creating the Snapshot copy. The default is false if there is only one volume in the consistency group, otherwise the default is true. """

    @property
    def resource(self):
        return ConsistencyGroupSnapshotResponseRecords

    gettable_fields = [
        "links",
        "comment",
        "consistency_group.links",
        "consistency_group.name",
        "consistency_group.uuid",
        "consistency_type",
        "create_time",
        "is_partial",
        "missing_volumes",
        "name",
        "snapmirror_label",
        "snapshot_volumes",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "write_fence",
    ]
    """links,comment,consistency_group.links,consistency_group.name,consistency_group.uuid,consistency_type,create_time,is_partial,missing_volumes,name,snapmirror_label,snapshot_volumes,svm.links,svm.name,svm.uuid,uuid,write_fence,"""

    patchable_fields = [
        "consistency_type",
        "name",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """consistency_type,name,svm.name,svm.uuid,write_fence,"""

    postable_fields = [
        "comment",
        "consistency_type",
        "name",
        "snapmirror_label",
        "svm.name",
        "svm.uuid",
        "write_fence",
    ]
    """comment,consistency_type,name,snapmirror_label,svm.name,svm.uuid,write_fence,"""


class ConsistencyGroupSnapshotResponseRecords(Resource):

    _schema = ConsistencyGroupSnapshotResponseRecordsSchema
