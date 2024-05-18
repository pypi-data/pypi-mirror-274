r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KeyManagerConfigHealthMonitorPolicy", "KeyManagerConfigHealthMonitorPolicySchema"]
__pdoc__ = {
    "KeyManagerConfigHealthMonitorPolicySchema.resource": False,
    "KeyManagerConfigHealthMonitorPolicySchema.opts": False,
    "KeyManagerConfigHealthMonitorPolicy": False,
}


class KeyManagerConfigHealthMonitorPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyManagerConfigHealthMonitorPolicy object"""

    akv = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="akv", allow_none=True)
    r""" The akv field of the key_manager_config_health_monitor_policy. """

    aws = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="aws", allow_none=True)
    r""" The aws field of the key_manager_config_health_monitor_policy. """

    gcp = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="gcp", allow_none=True)
    r""" The gcp field of the key_manager_config_health_monitor_policy. """

    ikp = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="ikp", allow_none=True)
    r""" The ikp field of the key_manager_config_health_monitor_policy. """

    kmip = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="kmip", allow_none=True)
    r""" The kmip field of the key_manager_config_health_monitor_policy. """

    okm = marshmallow_fields.Nested("netapp_ontap.models.health_monitor_policy_fields.HealthMonitorPolicyFieldsSchema", unknown=EXCLUDE, data_key="okm", allow_none=True)
    r""" The okm field of the key_manager_config_health_monitor_policy. """

    @property
    def resource(self):
        return KeyManagerConfigHealthMonitorPolicy

    gettable_fields = [
        "akv",
        "aws",
        "gcp",
        "ikp",
        "kmip",
        "okm",
    ]
    """akv,aws,gcp,ikp,kmip,okm,"""

    patchable_fields = [
        "akv",
        "aws",
        "gcp",
        "ikp",
        "kmip",
        "okm",
    ]
    """akv,aws,gcp,ikp,kmip,okm,"""

    postable_fields = [
        "akv",
        "aws",
        "gcp",
        "ikp",
        "kmip",
        "okm",
    ]
    """akv,aws,gcp,ikp,kmip,okm,"""


class KeyManagerConfigHealthMonitorPolicy(Resource):

    _schema = KeyManagerConfigHealthMonitorPolicySchema
