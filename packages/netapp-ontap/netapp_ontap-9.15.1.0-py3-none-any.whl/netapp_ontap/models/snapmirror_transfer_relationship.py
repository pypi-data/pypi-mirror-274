r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorTransferRelationship", "SnapmirrorTransferRelationshipSchema"]
__pdoc__ = {
    "SnapmirrorTransferRelationshipSchema.resource": False,
    "SnapmirrorTransferRelationshipSchema.opts": False,
    "SnapmirrorTransferRelationship": False,
}


class SnapmirrorTransferRelationshipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorTransferRelationship object"""

    destination = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_endpoint.SnapmirrorEndpointSchema", unknown=EXCLUDE, data_key="destination", allow_none=True)
    r""" The destination field of the snapmirror_transfer_relationship. """

    restore = marshmallow_fields.Boolean(data_key="restore", allow_none=True)
    r""" Is the relationship for restore? """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the SnapMirror relationship.

Example: d2d7ceea-ab52-11e8-855e-00505682a4c7 """

    @property
    def resource(self):
        return SnapmirrorTransferRelationship

    gettable_fields = [
        "destination",
        "restore",
        "uuid",
    ]
    """destination,restore,uuid,"""

    patchable_fields = [
        "destination",
        "restore",
        "uuid",
    ]
    """destination,restore,uuid,"""

    postable_fields = [
        "destination",
        "restore",
        "uuid",
    ]
    """destination,restore,uuid,"""


class SnapmirrorTransferRelationship(Resource):

    _schema = SnapmirrorTransferRelationshipSchema
