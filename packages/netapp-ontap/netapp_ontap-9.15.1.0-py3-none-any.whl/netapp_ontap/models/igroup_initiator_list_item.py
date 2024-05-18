r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorListItem", "IgroupInitiatorListItemSchema"]
__pdoc__ = {
    "IgroupInitiatorListItemSchema.resource": False,
    "IgroupInitiatorListItemSchema.opts": False,
    "IgroupInitiatorListItem": False,
}


class IgroupInitiatorListItemSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorListItem object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiators_links.IgroupInitiatorsLinksSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_initiator_list_item. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. Valid in POST and PATCH. """

    connectivity_tracking = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiators_connectivity_tracking.IgroupInitiatorsConnectivityTrackingSchema", unknown=EXCLUDE, data_key="connectivity_tracking", allow_none=True)
    r""" The connectivity_tracking field of the igroup_initiator_list_item. """

    igroup = marshmallow_fields.Nested("netapp_ontap.resources.igroup.IgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The igroup field of the igroup_initiator_list_item. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/>
An FC WWPN consists of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.


Example: iqn.1998-01.com.corp.iscsi:name1 """

    proximity = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_list_item_proximity.IgroupInitiatorListItemProximitySchema", unknown=EXCLUDE, data_key="proximity", allow_none=True)
    r""" The proximity field of the igroup_initiator_list_item. """

    @property
    def resource(self):
        return IgroupInitiatorListItem

    gettable_fields = [
        "links",
        "comment",
        "connectivity_tracking",
        "igroup.links",
        "igroup.name",
        "igroup.uuid",
        "name",
        "proximity",
    ]
    """links,comment,connectivity_tracking,igroup.links,igroup.name,igroup.uuid,name,proximity,"""

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


class IgroupInitiatorListItem(Resource):

    _schema = IgroupInitiatorListItemSchema
