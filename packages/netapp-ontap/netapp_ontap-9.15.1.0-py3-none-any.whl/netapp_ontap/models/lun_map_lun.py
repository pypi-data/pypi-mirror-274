r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMapLun", "LunMapLunSchema"]
__pdoc__ = {
    "LunMapLunSchema.resource": False,
    "LunMapLunSchema.opts": False,
    "LunMapLun": False,
}


class LunMapLunSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMapLun object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_map_lun. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The fully qualified path name of the LUN composed of a \"/vol\" prefix, the volume name, the (optional) qtree name, and file name of the LUN. Valid in POST.


Example: /vol/volume1/qtree1/lun1 """

    node = marshmallow_fields.Nested("netapp_ontap.models.lun_map_lun_node.LunMapLunNodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the lun_map_lun. """

    smbc = marshmallow_fields.Nested("netapp_ontap.models.lun_map_lun_smbc.LunMapLunSmbcSchema", unknown=EXCLUDE, data_key="smbc", allow_none=True)
    r""" The smbc field of the lun_map_lun. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the LUN. Valid in POST.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunMapLun

    gettable_fields = [
        "links",
        "name",
        "node",
        "smbc",
        "uuid",
    ]
    """links,name,node,smbc,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class LunMapLun(Resource):

    _schema = LunMapLunSchema
