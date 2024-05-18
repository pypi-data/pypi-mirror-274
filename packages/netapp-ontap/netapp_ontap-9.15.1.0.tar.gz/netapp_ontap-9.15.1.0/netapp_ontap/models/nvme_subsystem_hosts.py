r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemHosts", "NvmeSubsystemHostsSchema"]
__pdoc__ = {
    "NvmeSubsystemHostsSchema.resource": False,
    "NvmeSubsystemHostsSchema.opts": False,
    "NvmeSubsystemHosts": False,
}


class NvmeSubsystemHostsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemHosts object"""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_dh_hmac_chap_authentication.NvmeDhHmacChapAuthenticationSchema", unknown=EXCLUDE, data_key="dh_hmac_chap", allow_none=True)
    r""" The dh_hmac_chap field of the nvme_subsystem_hosts. """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target.


Example: nqn.1992-01.example.com:string """

    priority = marshmallow_fields.Str(data_key="priority", allow_none=True)
    r""" The host priority setting allocates appropriate NVMe I/O queues (count and depth) for the host to submit I/O commands. Absence of this property in GET implies user configured values of I/O queue count and I/O queue depth are being used.


Valid choices:

* regular
* high """

    @property
    def resource(self):
        return NvmeSubsystemHosts

    gettable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
    ]
    """dh_hmac_chap,nqn,priority,"""

    patchable_fields = [
        "dh_hmac_chap",
    ]
    """dh_hmac_chap,"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
    ]
    """dh_hmac_chap,nqn,priority,"""


class NvmeSubsystemHosts(Resource):

    _schema = NvmeSubsystemHostsSchema
