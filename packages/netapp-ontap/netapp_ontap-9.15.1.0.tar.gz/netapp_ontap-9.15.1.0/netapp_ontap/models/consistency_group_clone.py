r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupClone", "ConsistencyGroupCloneSchema"]
__pdoc__ = {
    "ConsistencyGroupCloneSchema.resource": False,
    "ConsistencyGroupCloneSchema.opts": False,
    "ConsistencyGroupClone": False,
}


class ConsistencyGroupCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupClone object"""

    guarantee = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_clone1_guarantee.ConsistencyGroupClone1GuaranteeSchema", unknown=EXCLUDE, data_key="guarantee", allow_none=True)
    r""" The guarantee field of the consistency_group_clone. """

    is_flexclone = marshmallow_fields.Boolean(data_key="is_flexclone", allow_none=True)
    r""" Specifies if this consistency group is a FlexClone of a consistency group. """

    parent_consistency_group = marshmallow_fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="parent_consistency_group", allow_none=True)
    r""" The parent_consistency_group field of the consistency_group_clone. """

    parent_snapshot = marshmallow_fields.Nested("netapp_ontap.resources.snapshot.SnapshotSchema", unknown=EXCLUDE, data_key="parent_snapshot", allow_none=True)
    r""" The parent_snapshot field of the consistency_group_clone. """

    parent_svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="parent_svm", allow_none=True)
    r""" The parent_svm field of the consistency_group_clone. """

    split_complete_percent = Size(data_key="split_complete_percent", allow_none=True)
    r""" Percentage of FlexClone blocks split from its parent consistency group. """

    split_estimate = Size(data_key="split_estimate", allow_none=True)
    r""" Space required to split the FlexClone consistency group. """

    split_initiated = marshmallow_fields.Boolean(data_key="split_initiated", allow_none=True)
    r""" Splits volumes after cloning. Default is false. """

    volume = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_clone1_volume.ConsistencyGroupClone1VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the consistency_group_clone. """

    @property
    def resource(self):
        return ConsistencyGroupClone

    gettable_fields = [
        "guarantee",
        "is_flexclone",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "parent_snapshot.links",
        "parent_snapshot.name",
        "parent_snapshot.uuid",
        "parent_svm.links",
        "parent_svm.name",
        "parent_svm.uuid",
        "split_complete_percent",
        "split_estimate",
        "split_initiated",
        "volume",
    ]
    """guarantee,is_flexclone,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,parent_snapshot.links,parent_snapshot.name,parent_snapshot.uuid,parent_svm.links,parent_svm.name,parent_svm.uuid,split_complete_percent,split_estimate,split_initiated,volume,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "guarantee",
        "is_flexclone",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "parent_snapshot.name",
        "parent_snapshot.uuid",
        "parent_svm.name",
        "parent_svm.uuid",
        "split_initiated",
        "volume",
    ]
    """guarantee,is_flexclone,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,parent_snapshot.name,parent_snapshot.uuid,parent_svm.name,parent_svm.uuid,split_initiated,volume,"""


class ConsistencyGroupClone(Resource):

    _schema = ConsistencyGroupCloneSchema
