r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemMapNamespace", "NvmeSubsystemMapNamespaceSchema"]
__pdoc__ = {
    "NvmeSubsystemMapNamespaceSchema.resource": False,
    "NvmeSubsystemMapNamespaceSchema.opts": False,
    "NvmeSubsystemMapNamespace": False,
}


class NvmeSubsystemMapNamespaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemMapNamespace object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_subsystem_map_namespace. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The fully qualified path name of the NVMe namespace composed from the volume name, qtree name, and file name of the NVMe namespace. Valid in POST.


Example: /vol/vol1/namespace1 """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the nvme_subsystem_map_namespace. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the NVMe namespace. Valid in POST.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemMapNamespace

    gettable_fields = [
        "links",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "uuid",
    ]
    """links,name,node.links,node.name,node.uuid,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class NvmeSubsystemMapNamespace(Resource):

    _schema = NvmeSubsystemMapNamespaceSchema
