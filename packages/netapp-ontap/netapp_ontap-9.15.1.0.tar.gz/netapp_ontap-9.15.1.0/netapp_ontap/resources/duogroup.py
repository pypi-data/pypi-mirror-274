r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures the Duo group for an SVM.
Specify the owner UUID. The owner UUID corresponds to the UUID of the SVM containing the Duo groups and can be obtained from the response body of the GET request performed on the API “/api/svm/svms".
## Examples
### Retrieving the specific configured Duo group(s) of the cluster or SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Duogroup(
    {
        "owner": {"name": "cluster-1", "uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"},
        "comment": "test group create",
        "name": "test",
        "excluded_users": ["tsmith", "msmith"],
    }
)

```
</div>
</div>

### Modifying a Duo group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
    )
    resource.comment = "Testing"
    resource.patch()

```

### Deleting a  Duo group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
    )
    resource.delete()

```
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


__all__ = ["Duogroup", "DuogroupSchema"]
__pdoc__ = {
    "DuogroupSchema.resource": False,
    "DuogroupSchema.opts": False,
    "Duogroup.duogroup_show": False,
    "Duogroup.duogroup_create": False,
    "Duogroup.duogroup_modify": False,
    "Duogroup.duogroup_delete": False,
}


class DuogroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Duogroup object"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment for the Duo group."""

    excluded_users = marshmallow_fields.List(marshmallow_fields.Str, data_key="excluded_users", allow_none=True)
    r""" List of excluded users.

Example: ["user1","user2"]"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the group to be included in Duo authentication.

Example: AD_Group"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the duogroup."""

    @property
    def resource(self):
        return Duogroup

    gettable_fields = [
        "comment",
        "excluded_users",
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
    ]
    """comment,excluded_users,name,owner.links,owner.name,owner.uuid,"""

    patchable_fields = [
        "comment",
        "excluded_users",
    ]
    """comment,excluded_users,"""

    postable_fields = [
        "comment",
        "excluded_users",
        "name",
        "owner.name",
        "owner.uuid",
    ]
    """comment,excluded_users,name,owner.name,owner.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Duogroup.get_collection(fields=field)]
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
            raise NetAppRestError("Duogroup modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Duogroup(Resource):
    r""" Group profile to include in Duo authentication. """

    _schema = DuogroupSchema
    _path = "/api/security/authentication/duo/groups"
    _keys = ["owner.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the configured groups.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duogroup show")
        def duogroup_show(
            fields: List[Choices.define(["comment", "excluded_users", "name", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Duogroup resources

            Args:
                comment: Comment for the Duo group.
                excluded_users: List of excluded users.
                name: Name of the group to be included in Duo authentication.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if excluded_users is not None:
                kwargs["excluded_users"] = excluded_users
            if name is not None:
                kwargs["name"] = name
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Duogroup.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Duogroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent Duogroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Duogroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo group for a cluster or SVM.
### Related ONTAP commands
* `security login duo group modify`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Duogroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Duogroup"], NetAppResponse]:
        r"""Creates a Duo Group.
### Required properties
* `owner.uuid` - Account owner UUID.
* `name` - Group name
### Related ONTAP commands
* `security login duo group create`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Duogroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Duo group of the SVM or cluster.
### Related ONTAP commands
* `security login duo group delete`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the configured groups.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Duo group configured for an SVM or cluster.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a Duo Group.
### Required properties
* `owner.uuid` - Account owner UUID.
* `name` - Group name
### Related ONTAP commands
* `security login duo group create`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duogroup create")
        async def duogroup_create(
        ) -> ResourceTable:
            """Create an instance of a Duogroup resource

            Args:
                comment: Comment for the Duo group.
                excluded_users: List of excluded users.
                name: Name of the group to be included in Duo authentication.
                owner: 
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if excluded_users is not None:
                kwargs["excluded_users"] = excluded_users
            if name is not None:
                kwargs["name"] = name
            if owner is not None:
                kwargs["owner"] = owner

            resource = Duogroup(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create Duogroup: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo group for a cluster or SVM.
### Related ONTAP commands
* `security login duo group modify`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duogroup modify")
        async def duogroup_modify(
        ) -> ResourceTable:
            """Modify an instance of a Duogroup resource

            Args:
                comment: Comment for the Duo group.
                query_comment: Comment for the Duo group.
                excluded_users: List of excluded users.
                query_excluded_users: List of excluded users.
                name: Name of the group to be included in Duo authentication.
                query_name: Name of the group to be included in Duo authentication.
            """

            kwargs = {}
            changes = {}
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_excluded_users is not None:
                kwargs["excluded_users"] = query_excluded_users
            if query_name is not None:
                kwargs["name"] = query_name

            if comment is not None:
                changes["comment"] = comment
            if excluded_users is not None:
                changes["excluded_users"] = excluded_users
            if name is not None:
                changes["name"] = name

            if hasattr(Duogroup, "find"):
                resource = Duogroup.find(
                    **kwargs
                )
            else:
                resource = Duogroup()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify Duogroup: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Duo group of the SVM or cluster.
### Related ONTAP commands
* `security login duo group delete`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="duogroup delete")
        async def duogroup_delete(
        ) -> None:
            """Delete an instance of a Duogroup resource

            Args:
                comment: Comment for the Duo group.
                excluded_users: List of excluded users.
                name: Name of the group to be included in Duo authentication.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if excluded_users is not None:
                kwargs["excluded_users"] = excluded_users
            if name is not None:
                kwargs["name"] = name

            if hasattr(Duogroup, "find"):
                resource = Duogroup.find(
                    **kwargs
                )
            else:
                resource = Duogroup()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete Duogroup: %s" % err)


