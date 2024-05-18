r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorNoRecords", "IgroupInitiatorNoRecordsSchema"]
__pdoc__ = {
    "IgroupInitiatorNoRecordsSchema.resource": False,
    "IgroupInitiatorNoRecordsSchema.opts": False,
    "IgroupInitiatorNoRecords": False,
}


class IgroupInitiatorNoRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorNoRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_initiator_no_records. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. Valid in POST and PATCH. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/>
An FC WWPN consists of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.


Example: iqn.1998-01.com.corp.iscsi:name1 """

    proximity = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_no_records_proximity.IgroupInitiatorNoRecordsProximitySchema", unknown=EXCLUDE, data_key="proximity", allow_none=True)
    r""" The proximity field of the igroup_initiator_no_records. """

    @property
    def resource(self):
        return IgroupInitiatorNoRecords

    gettable_fields = [
        "links",
        "comment",
        "name",
        "proximity",
    ]
    """links,comment,name,proximity,"""

    patchable_fields = [
        "comment",
        "proximity",
    ]
    """comment,proximity,"""

    postable_fields = [
        "comment",
        "name",
        "proximity",
    ]
    """comment,name,proximity,"""


class IgroupInitiatorNoRecords(Resource):

    _schema = IgroupInitiatorNoRecordsSchema
