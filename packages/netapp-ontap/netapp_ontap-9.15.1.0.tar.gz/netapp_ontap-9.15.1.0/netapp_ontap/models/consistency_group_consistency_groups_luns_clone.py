r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsLunsClone", "ConsistencyGroupConsistencyGroupsLunsCloneSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsLunsCloneSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsLunsClone": False,
}


class ConsistencyGroupConsistencyGroupsLunsCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsLunsClone object"""

    source = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_luns_clone_source.ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source field of the consistency_group_consistency_groups_luns_clone. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsLunsClone

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "source",
    ]
    """source,"""

    postable_fields = [
        "source",
    ]
    """source,"""


class ConsistencyGroupConsistencyGroupsLunsClone(Resource):

    _schema = ConsistencyGroupConsistencyGroupsLunsCloneSchema
