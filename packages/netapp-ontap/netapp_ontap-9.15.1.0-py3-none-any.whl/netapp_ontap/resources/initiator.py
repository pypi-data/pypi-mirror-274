r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An initiator is a Fibre Channel (FC) world wide port name (WWPN), an iSCSI Qualified Name (IQN), or an iSCSI EUI (Extended Unique Identifier) that identifies a host endpoint. Initiators are collected into initiator groups (igroups) used to control which hosts can access specific LUNs. Initiators are also discovered as they log in to SAN network LIFs.<br/>
ONTAP supports configuration for an initiator. Configured properties apply to all uses of the initiator within an SVM. Although the same initiator may interact with multiple SVMs of a cluster, ONTAP treats initiator configuration as an SVM-scoped activity. For example, a comment may be set for an initiator in a specific SVM. The comment value applies to all uses of the initiator in the SVM including use in multiple initiator groups. But a different comment value may be specified for the same initiator in a different SVM.<br/>
The initiator REST API provides read-only access to properties of initators.<br/>
An FC WWPN consists of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters."""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    RECLINE_INSTALLED = False
    import recline
    from recline.arg_types.choices import Choices
    from recline.commands import ReclineCommandError
    from netapp_ontap.resource_table import ResourceTable
    RECLINE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Initiator", "InitiatorSchema"]
__pdoc__ = {
    "InitiatorSchema.resource": False,
    "InitiatorSchema.opts": False,
    "Initiator.initiator_show": False,
    "Initiator.initiator_create": False,
    "Initiator.initiator_modify": False,
    "Initiator.initiator_delete": False,
}


class InitiatorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Initiator object"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A user-specified comment.


Example: My initiator comment."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the initiator.


Example: iqn.2018-02.com.netapp.iscsi:name1"""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['fcp', 'iscsi']),
        allow_none=True,
    )
    r""" The protocol of the initiator.


Valid choices:

* fcp
* iscsi"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the initiator."""

    @property
    def resource(self):
        return Initiator

    gettable_fields = [
        "comment",
        "name",
        "protocol",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """comment,name,protocol,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Initiator.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("Initiator modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Initiator(Resource):
    r""" An initiator is a Fibre Channel (FC) world wide port name (WWPN), an iSCSI Qualified Name (IQN), or an iSCSI EUI (Extended Unique Identifier) that identifies a host endpoint. Initiators are collected into initiator groups (igroups) used to control which hosts can access specific LUNs. Initiators are also discovered as they log in to SAN network LIFs.<br/>
ONTAP supports configuration for an initiator. Configured properties apply to all uses of the initiator within an SVM. Although the same initiator may interact with multiple SVMs of a cluster, ONTAP treats initiator configuration as an SVM-scoped activity. For example, a comment may be set for an initiator in a specific SVM. The comment value applies to all uses of the initiator in the SVM including use in multiple initiator groups. But a different comment value may be specified for the same initiator in a different SVM. """

    _schema = InitiatorSchema
    _path = "/api/protocols/san/initiators"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves initiators.
### Related ONTAP commands
* `lun igroup initiator show`
### Learn more
* [`DOC /protocols/san/initiators`](#docs-SAN-protocols_san_initiators)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="initiator show")
        def initiator_show(
            fields: List[Choices.define(["comment", "name", "protocol", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Initiator resources

            Args:
                comment: A user-specified comment. 
                name: The name of the initiator. 
                protocol: The protocol of the initiator. 
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if name is not None:
                kwargs["name"] = name
            if protocol is not None:
                kwargs["protocol"] = protocol
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Initiator.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Initiator resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent Initiator resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves initiators.
### Related ONTAP commands
* `lun igroup initiator show`
### Learn more
* [`DOC /protocols/san/initiators`](#docs-SAN-protocols_san_initiators)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an initiator.
### Related ONTAP commands
* `lun igroup initiator show`
### Learn more
* [`DOC /protocols/san/initiators`](#docs-SAN-protocols_san_initiators)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





