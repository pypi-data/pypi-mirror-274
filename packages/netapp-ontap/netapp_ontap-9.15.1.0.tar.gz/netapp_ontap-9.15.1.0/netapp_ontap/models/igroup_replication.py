r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupReplication", "IgroupReplicationSchema"]
__pdoc__ = {
    "IgroupReplicationSchema.resource": False,
    "IgroupReplicationSchema.opts": False,
    "IgroupReplication": False,
}


class IgroupReplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupReplication object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.igroup_replication_error.IgroupReplicationErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the igroup_replication. """

    peer_svm = marshmallow_fields.Nested("netapp_ontap.resources.svm_peer.SvmPeerSchema", unknown=EXCLUDE, data_key="peer_svm", allow_none=True)
    r""" The peer_svm field of the igroup_replication. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the replication queue associated with this igroup. If this igroup is not in the replication queue, the state is reported as _ok_. If this igroup is in the replication queue, but no errors have been encountered, the state is reported as _replicating_. If this igroup is in the replication queue and the queue is blocked by an error, the state is reported as _error_. When in the _error_ state, additional context is provided by the `replication.error` property.


Valid choices:

* ok
* replicating
* error """

    @property
    def resource(self):
        return IgroupReplication

    gettable_fields = [
        "error",
        "peer_svm.links",
        "peer_svm.name",
        "peer_svm.uuid",
        "state",
    ]
    """error,peer_svm.links,peer_svm.name,peer_svm.uuid,state,"""

    patchable_fields = [
        "error",
        "peer_svm.name",
        "peer_svm.uuid",
    ]
    """error,peer_svm.name,peer_svm.uuid,"""

    postable_fields = [
        "error",
        "peer_svm.name",
        "peer_svm.uuid",
    ]
    """error,peer_svm.name,peer_svm.uuid,"""


class IgroupReplication(Resource):

    _schema = IgroupReplicationSchema
