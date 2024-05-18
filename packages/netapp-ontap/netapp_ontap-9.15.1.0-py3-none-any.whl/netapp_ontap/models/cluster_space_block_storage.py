r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceBlockStorage", "ClusterSpaceBlockStorageSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageSchema.resource": False,
    "ClusterSpaceBlockStorageSchema.opts": False,
    "ClusterSpaceBlockStorage": False,
}


class ClusterSpaceBlockStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpaceBlockStorage object"""

    available = Size(data_key="available", allow_none=True)
    r""" Available space across the cluster. """

    inactive_data = Size(data_key="inactive_data", allow_none=True)
    r""" Inactive data across the cluster. """

    medias = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_space_block_storage_medias.ClusterSpaceBlockStorageMediasSchema", unknown=EXCLUDE, allow_none=True), data_key="medias", allow_none=True)
    r""" Configuration information based on type of media. For example, SSD media type information includes the sum of all the SSD storage across the cluster. """

    physical_used = Size(data_key="physical_used", allow_none=True)
    r""" Total physical used space across the cluster. """

    size = Size(data_key="size", allow_none=True)
    r""" Total space across the cluster. """

    used = Size(data_key="used", allow_none=True)
    r""" Used space (includes volume reserves) across the cluster. """

    @property
    def resource(self):
        return ClusterSpaceBlockStorage

    gettable_fields = [
        "available",
        "inactive_data",
        "medias",
        "physical_used",
        "size",
        "used",
    ]
    """available,inactive_data,medias,physical_used,size,used,"""

    patchable_fields = [
        "available",
        "inactive_data",
        "medias",
        "physical_used",
        "size",
        "used",
    ]
    """available,inactive_data,medias,physical_used,size,used,"""

    postable_fields = [
        "available",
        "inactive_data",
        "medias",
        "physical_used",
        "size",
        "used",
    ]
    """available,inactive_data,medias,physical_used,size,used,"""


class ClusterSpaceBlockStorage(Resource):

    _schema = ClusterSpaceBlockStorageSchema
