r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Non-Volatile Memory Express (NVMe) subsystem controllers represent dynamic connections between hosts and a storage solution.<br/>
The NVMe subsystem controllers REST API provides information about connected hosts.
## Examples
### Retrieving the NVMe subsystem controllers for the entire system
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NvmeSubsystemController.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
            },
            "id": "0040h",
        }
    ),
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0041h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
            },
            "id": "0041h",
        }
    ),
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/1489d0d5-2594-11e9-94c4-00a0989a1c8e/0040h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/1489d0d5-2594-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "1489d0d5-2594-11e9-94c4-00a0989a1c8e",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_1",
            },
            "id": "0040h",
        }
    ),
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/1489d0d5-2594-11e9-94c4-00a0989a1c8e/0041h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/1489d0d5-2594-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "1489d0d5-2594-11e9-94c4-00a0989a1c8e",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_1",
            },
            "id": "0041h",
        }
    ),
]

```
</div>
</div>

---
### Retrieving the NVMe subsystem controllers for a specific subsystem
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            NvmeSubsystemController.get_collection(
                **{"subsystem.uuid": "14875240-2594-11e9-abde-00a098984313"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
            },
            "id": "0040h",
        }
    ),
    NvmeSubsystemController(
        {
            "svm": {
                "name": "symmcon_fcnvme_vserver_0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"
                    }
                },
                "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0041h"
                }
            },
            "subsystem": {
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                    }
                },
                "uuid": "14875240-2594-11e9-abde-00a098984313",
                "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
            },
            "id": "0041h",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific NVMe subsystem controller
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemController

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeSubsystemController(
        id="0040h", **{"subsystem.uuid": "14875240-2594-11e9-abde-00a098984313"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
NvmeSubsystemController(
    {
        "admin_queue": {"depth": 32},
        "svm": {
            "name": "symmcon_fcnvme_vserver_0",
            "_links": {
                "self": {"href": "/api/svm/svms/f0f5b928-2593-11e9-94c4-00a0989a1c8e"}
            },
            "uuid": "f0f5b928-2593-11e9-94c4-00a0989a1c8e",
        },
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/subsystem-controllers/14875240-2594-11e9-abde-00a098984313/0040h"
            }
        },
        "interface": {
            "uuid": "fa1c5941-2593-11e9-94c4-00a0989a1c8e",
            "transport_address": "nn-0x200400a0989a1c8d:pn-0x200500a0989a1c8d",
            "name": "symmcon_lif_fcnvme_symmcon_fcnvme_vserver_0_3a_0",
        },
        "dh_hmac_chap": {"mode": "none"},
        "subsystem": {
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystems/14875240-2594-11e9-abde-00a098984313"
                }
            },
            "uuid": "14875240-2594-11e9-abde-00a098984313",
            "name": "symmcon_symmcon_fcnvme_vserver_0_subsystem_0",
        },
        "keep_alive_timeout": 4000,
        "digest": {"data": False, "header": True},
        "host": {
            "transport_address": "nn-0x20000090fae00806:pn-0x10000090fae00806",
            "nqn": "nqn.2014-08.org.nvmexpress:uuid:c2846cb1-89d2-4020-a3b0-71ce907b4eef",
            "id": "b8546ca6097349e5b1558dc154fc073b",
        },
        "id": "0040h",
        "io_queue": {"depth": [32, 32, 32, 32], "count": 4},
        "node": {
            "name": "ssan-8040-94a",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/ebf66f05-2590-11e9-abde-00a098984313"
                }
            },
            "uuid": "ebf66f05-2590-11e9-abde-00a098984313",
        },
    }
)

```
</div>
</div>
"""

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


__all__ = ["NvmeSubsystemController", "NvmeSubsystemControllerSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerSchema.resource": False,
    "NvmeSubsystemControllerSchema.opts": False,
    "NvmeSubsystemController.nvme_subsystem_controller_show": False,
    "NvmeSubsystemController.nvme_subsystem_controller_create": False,
    "NvmeSubsystemController.nvme_subsystem_controller_modify": False,
    "NvmeSubsystemController.nvme_subsystem_controller_delete": False,
}


class NvmeSubsystemControllerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemController object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_subsystem_controller."""

    admin_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_admin_queue.NvmeSubsystemControllerAdminQueueSchema", data_key="admin_queue", unknown=EXCLUDE, allow_none=True)
    r""" The admin_queue field of the nvme_subsystem_controller."""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_dh_hmac_chap.NvmeSubsystemControllerDhHmacChapSchema", data_key="dh_hmac_chap", unknown=EXCLUDE, allow_none=True)
    r""" The dh_hmac_chap field of the nvme_subsystem_controller."""

    digest = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_digest.NvmeSubsystemControllerDigestSchema", data_key="digest", unknown=EXCLUDE, allow_none=True)
    r""" The digest field of the nvme_subsystem_controller."""

    host = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_host.NvmeSubsystemControllerHostSchema", data_key="host", unknown=EXCLUDE, allow_none=True)
    r""" The host field of the nvme_subsystem_controller."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" The identifier of the subsystem controller. This field consists of 4 zero-filled hexadecimal digits followed by an 'h'.


Example: 0040h"""

    interface = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_interface.NvmeSubsystemControllerInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The interface field of the nvme_subsystem_controller."""

    io_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_controller_io_queue.NvmeSubsystemControllerIoQueueSchema", data_key="io_queue", unknown=EXCLUDE, allow_none=True)
    r""" The io_queue field of the nvme_subsystem_controller."""

    keep_alive_timeout = Size(
        data_key="keep_alive_timeout",
        allow_none=True,
    )
    r""" The keep-alive timeout value for the controller and all of its host connections, in milliseconds. <br/>
If the NVMe controller does not receive a keep-alive request or an I/O request within the timeout window, the NVMe controller terminates its admin queue and I/O queue connections leading to NVMe controller teardown. If the NVMe host does not receive a response to a keep-alive request or an I/O request within the timeout window, the NVMe host initiates a connection disconnect.


Example: 1500"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the nvme_subsystem_controller."""

    subsystem = marshmallow_fields.Nested("netapp_ontap.resources.nvme_subsystem.NvmeSubsystemSchema", data_key="subsystem", unknown=EXCLUDE, allow_none=True)
    r""" The subsystem field of the nvme_subsystem_controller."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_subsystem_controller."""

    @property
    def resource(self):
        return NvmeSubsystemController

    gettable_fields = [
        "links",
        "admin_queue",
        "dh_hmac_chap",
        "digest",
        "host",
        "id",
        "interface",
        "io_queue",
        "keep_alive_timeout",
        "node.links",
        "node.name",
        "node.uuid",
        "subsystem.links",
        "subsystem.name",
        "subsystem.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,admin_queue,dh_hmac_chap,digest,host,id,interface,io_queue,keep_alive_timeout,node.links,node.name,node.uuid,subsystem.links,subsystem.name,subsystem.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in NvmeSubsystemController.get_collection(fields=field)]
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
            raise NetAppRestError("NvmeSubsystemController modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class NvmeSubsystemController(Resource):
    r""" A Non-Volatile Memory Express (NVMe) subsystem controller represents a connection between a host and a storage solution.<br/>
An NVMe subsystem controller is identified by the NVMe subsystem UUID and the controller ID. """

    _schema = NvmeSubsystemControllerSchema
    _path = "/api/protocols/nvme/subsystem-controllers"
    _keys = ["subsystem.uuid", "id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe subsystem controllers.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="nvme subsystem controller show")
        def nvme_subsystem_controller_show(
            fields: List[Choices.define(["id", "keep_alive_timeout", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of NvmeSubsystemController resources

            Args:
                id: The identifier of the subsystem controller. This field consists of 4 zero-filled hexadecimal digits followed by an 'h'. 
                keep_alive_timeout: The keep-alive timeout value for the controller and all of its host connections, in milliseconds. <br/> If the NVMe controller does not receive a keep-alive request or an I/O request within the timeout window, the NVMe controller terminates its admin queue and I/O queue connections leading to NVMe controller teardown. If the NVMe host does not receive a response to a keep-alive request or an I/O request within the timeout window, the NVMe host initiates a connection disconnect. 
            """

            kwargs = {}
            if id is not None:
                kwargs["id"] = id
            if keep_alive_timeout is not None:
                kwargs["keep_alive_timeout"] = keep_alive_timeout
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return NvmeSubsystemController.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all NvmeSubsystemController resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeSubsystemController resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe subsystem controllers.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe subsystem controller.
### Related ONTAP commands
* `vserver nvme subsystem controller show`
### Learn more
* [`DOC /protocols/nvme/subsystem-controllers`](#docs-NVMe-protocols_nvme_subsystem-controllers)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





