r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationBackingStorage", "ApplicationBackingStorageSchema"]
__pdoc__ = {
    "ApplicationBackingStorageSchema.resource": False,
    "ApplicationBackingStorageSchema.opts": False,
    "ApplicationBackingStorage": False,
}


class ApplicationBackingStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationBackingStorage object"""

    luns = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_lun_object.ApplicationLunObjectSchema", unknown=EXCLUDE, allow_none=True), data_key="luns", allow_none=True)
    r""" The luns field of the application_backing_storage. """

    namespaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_namespace_object.ApplicationNamespaceObjectSchema", unknown=EXCLUDE, allow_none=True), data_key="namespaces", allow_none=True)
    r""" The namespaces field of the application_backing_storage. """

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_volume_object.ApplicationVolumeObjectSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" The volumes field of the application_backing_storage. """

    @property
    def resource(self):
        return ApplicationBackingStorage

    gettable_fields = [
        "luns",
        "namespaces",
        "volumes",
    ]
    """luns,namespaces,volumes,"""

    patchable_fields = [
        "luns",
        "namespaces",
        "volumes",
    ]
    """luns,namespaces,volumes,"""

    postable_fields = [
        "luns",
        "namespaces",
        "volumes",
    ]
    """luns,namespaces,volumes,"""


class ApplicationBackingStorage(Resource):

    _schema = ApplicationBackingStorageSchema
