r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupQos", "ConsistencyGroupQosSchema"]
__pdoc__ = {
    "ConsistencyGroupQosSchema.resource": False,
    "ConsistencyGroupQosSchema.opts": False,
    "ConsistencyGroupQos": False,
}


class ConsistencyGroupQosSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupQos object"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos_policy.ConsistencyGroupQosPolicySchema", unknown=EXCLUDE, data_key="policy", allow_none=True)
    r""" The policy field of the consistency_group_qos. """

    @property
    def resource(self):
        return ConsistencyGroupQos

    gettable_fields = [
        "policy",
    ]
    """policy,"""

    patchable_fields = [
        "policy",
    ]
    """policy,"""

    postable_fields = [
        "policy",
    ]
    """policy,"""


class ConsistencyGroupQos(Resource):

    _schema = ConsistencyGroupQosSchema
