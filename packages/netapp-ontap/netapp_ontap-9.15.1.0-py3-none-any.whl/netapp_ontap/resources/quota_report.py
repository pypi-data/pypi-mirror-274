r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Quota reports provide the current file and space consumption for a user, group, or qtree in a FlexVol or a FlexGroup volume.
## Quota report APIs
The following APIs can be used to retrieve quota reports associated with a volume in ONTAP.

* GET       /api/storage/quota/reports
* GET       /api/storage/quota/reports/{volume_uuid}/{index}
## Examples
### Retrieving all the quota report records
This API is used to retrieve all the quota report records. <br/>
The following example shows how to retrieve quota report records for all FlexVol volumes and FlexGroup volumes.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/0"
                }
            },
            "index": 0,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/1152921504606846976"
                }
            },
            "index": 1152921504606846976,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/3458764513820540928"
                }
            },
            "index": 3458764513820540928,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/4611686018427387904"
                }
            },
            "index": 4611686018427387904,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/314a328f-502d-11e9-8771-005056a7f717"
                    }
                },
                "uuid": "314a328f-502d-11e9-8771-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/314a328f-502d-11e9-8771-005056a7f717/5764607523034234880"
                }
            },
            "index": 5764607523034234880,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/0"
                }
            },
            "index": 0,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/281474976710656"
                }
            },
            "index": 281474976710656,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/1152921504606846976"
                }
            },
            "index": 1152921504606846976,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/1153202979583557632"
                }
            },
            "index": 1153202979583557632,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/3458764513820540928"
                }
            },
            "index": 3458764513820540928,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/3459045988797251584"
                }
            },
            "index": 3459045988797251584,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/4611686018427387904"
                }
            },
            "index": 4611686018427387904,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/4611967493404098560"
                }
            },
            "index": 4611967493404098560,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
                    }
                },
                "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
                    }
                },
                "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cb20da45-4f6b-11e9-9a71-005056a7f717/5764607523034234880"
                }
            },
            "index": 5764607523034234880,
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific quota report record
This API is used to retrieve a specific quota report record. <br/>
The following example shows how to retrieve a single quota report user record.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=281474976710656, **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
QuotaReport(
    {
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
            "soft_limit": 31457280,
        },
        "users": [{"name": "fred", "id": "300008"}],
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/281474976710656"
            }
        },
        "qtree": {
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "name": "qt1",
            "id": 1,
        },
        "files": {
            "hard_limit": 40,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
            "soft_limit": 30,
        },
        "index": 281474976710656,
        "type": "user",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report multi-user record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=281474976710656, **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
QuotaReport(
    {
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
            "soft_limit": 31457280,
        },
        "users": [
            {"name": "fred", "id": "300008"},
            {"name": "john", "id": "300009"},
            {"name": "smith", "id": "300010"},
        ],
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/1153484454560268288"
            }
        },
        "qtree": {
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "name": "qt1",
            "id": 1,
        },
        "files": {
            "hard_limit": 40,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
            "soft_limit": 30,
        },
        "index": 1153484454560268288,
        "type": "user",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report group record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=3459045988797251584,
        **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
QuotaReport(
    {
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
            "soft_limit": 31457280,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/3459045988797251584"
            }
        },
        "qtree": {
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "name": "qt1",
            "id": 1,
        },
        "group": {"name": "test_group", "id": "500009"},
        "files": {
            "hard_limit": 40,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
            "soft_limit": 30,
        },
        "index": 3459045988797251584,
        "type": "group",
    }
)

```
</div>
</div>

---
### Retrieving a single quota report tree record
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QuotaReport(
        index=4612248968380809216,
        **{"volume.uuid": "cf480c37-2a6b-11e9-8513-005056a7657c"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
QuotaReport(
    {
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"}
            },
            "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
        },
        "volume": {
            "name": "fv",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                }
            },
            "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
        },
        "space": {
            "hard_limit": 41943040,
            "used": {
                "hard_limit_percent": 25,
                "soft_limit_percent": 34,
                "total": 10567680,
            },
            "soft_limit": 31457280,
        },
        "_links": {
            "self": {
                "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/4612248968380809216"
            }
        },
        "qtree": {
            "_links": {
                "self": {
                    "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                }
            },
            "name": "qt1",
            "id": 1,
        },
        "files": {
            "hard_limit": 40,
            "used": {"hard_limit_percent": 28, "soft_limit_percent": 37, "total": 11},
            "soft_limit": 30,
        },
        "index": 4612248968380809216,
        "type": "tree",
    }
)

```
</div>
</div>

---
### Retrieving only records enforced by non-default rules
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(show_default_records=False)))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"
                    }
                },
                "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                    }
                },
                "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
            },
            "space": {
                "hard_limit": 41943040,
                "used": {
                    "hard_limit_percent": 25,
                    "soft_limit_percent": 34,
                    "total": 10567680,
                },
                "soft_limit": 31457280,
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/4612248968380809216"
                }
            },
            "qtree": {
                "_links": {
                    "self": {
                        "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                    }
                },
                "name": "qt1",
                "id": 1,
            },
            "files": {
                "hard_limit": 40,
                "used": {
                    "hard_limit_percent": 28,
                    "soft_limit_percent": 37,
                    "total": 11,
                },
                "soft_limit": 30,
            },
            "index": 4612248968380809216,
            "type": "tree",
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/5093e722-248e-11e9-96ee-005056a7657c"
                    }
                },
                "uuid": "5093e722-248e-11e9-96ee-005056a7657c",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/cf480c37-2a6b-11e9-8513-005056a7657c"
                    }
                },
                "uuid": "cf480c37-2a6b-11e9-8513-005056a7657c",
            },
            "space": {
                "hard_limit": 41943040,
                "used": {
                    "hard_limit_percent": 25,
                    "soft_limit_percent": 34,
                    "total": 10567680,
                },
                "soft_limit": 31457280,
            },
            "users": [
                {"name": "fred", "id": "300008"},
                {"name": "john", "id": "300009"},
                {"name": "smith", "id": "300010"},
            ],
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/cf480c37-2a6b-11e9-8513-005056a7657c/1153484454560268288"
                }
            },
            "qtree": {
                "_links": {
                    "self": {
                        "href": "/api/storage/qtrees/cf480c37-2a6b-11e9-8513-005056a7657c/1"
                    }
                },
                "name": "qt1",
                "id": 1,
            },
            "files": {
                "hard_limit": 40,
                "used": {
                    "hard_limit_percent": 28,
                    "soft_limit_percent": 37,
                    "total": 11,
                },
                "soft_limit": 30,
            },
            "index": 1153484454560268288,
            "type": "user",
        }
    ),
]

```
</div>
</div>

---
### Retrieving quota report records with query parameters
The following example shows how to retrieve tree type quota report records.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(type="tree")))

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "type": "tree",
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "volume": {
                "name": "fg",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/a5ceebd2-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "a5ceebd2-6ccf-11ea-bc35-005056823577",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/a5ceebd2-6ccf-11ea-bc35-005056823577/2305843013508661248"
                }
            },
            "index": 2305843013508661248,
            "type": "tree",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all the quota reports of a specific volume and the files fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QuotaReport.get_collection(fields="files", **{"volume.name": "fv"})))

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/410328290557952"
                }
            },
            "files": {
                "hard_limit": 30,
                "used": {"hard_limit_percent": 0, "soft_limit_percent": 0, "total": 0},
                "soft_limit": 20,
            },
            "index": 410328290557952,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/903e54ee-6ccf-11ea-bc35-005056823577"
                    }
                },
                "uuid": "903e54ee-6ccf-11ea-bc35-005056823577",
            },
            "volume": {
                "name": "fv",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/8812b000-6e1e-11ea-9bad-00505682cd5c"
                    }
                },
                "uuid": "8812b000-6e1e-11ea-9bad-00505682cd5c",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/8812b000-6e1e-11ea-9bad-00505682cd5c/2305843013508661248"
                }
            },
            "files": {
                "hard_limit": 400,
                "used": {"hard_limit_percent": 1, "soft_limit_percent": 2, "total": 4},
                "soft_limit": 200,
            },
            "index": 2305843013508661248,
        }
    ),
]

```
</div>
</div>

---
### Retrieving quota reports for all volumes with the property files.hard_limit greater than 5 or null (unlimited) for qtree qt1
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QuotaReport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            QuotaReport.get_collection(
                **{"qtree.name": "qt1", "files.hard_limit": ">5|null"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/281474976710656"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 281474976710656,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/1153202979583557632"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 1153202979583557632,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/2305843013508661248"
                }
            },
            "qtree": {"name": "qt1"},
            "files": {"hard_limit": 15},
            "index": 2305843013508661248,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/3459045988797251584"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 3459045988797251584,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/0c9cff59-da3c-11ed-930f-005056ac3135"
                    }
                },
                "uuid": "0c9cff59-da3c-11ed-930f-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/0c9cff59-da3c-11ed-930f-005056ac3135/4611967493404098560"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 4611967493404098560,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/281474976710656"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 281474976710656,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/1153202979583557632"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 1153202979583557632,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/3459045988797251584"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 3459045988797251584,
        }
    ),
    QuotaReport(
        {
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/842981cb-c985-11ed-a399-005056ac442b"
                    }
                },
                "uuid": "842981cb-c985-11ed-a399-005056ac442b",
            },
            "volume": {
                "name": "srcVolume2",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/3a2a8d78-ded3-11ed-9806-005056ac3135"
                    }
                },
                "uuid": "3a2a8d78-ded3-11ed-9806-005056ac3135",
            },
            "_links": {
                "self": {
                    "href": "/api/storage/quota/reports/3a2a8d78-ded3-11ed-9806-005056ac3135/4611967493404098560"
                }
            },
            "qtree": {"name": "qt1"},
            "index": 4611967493404098560,
        }
    ),
]

```
</div>
</div>

---"""

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


__all__ = ["QuotaReport", "QuotaReportSchema"]
__pdoc__ = {
    "QuotaReportSchema.resource": False,
    "QuotaReportSchema.opts": False,
    "QuotaReport.quota_report_show": False,
    "QuotaReport.quota_report_create": False,
    "QuotaReport.quota_report_modify": False,
    "QuotaReport.quota_report_delete": False,
}


class QuotaReportSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaReport object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the quota_report."""

    files = marshmallow_fields.Nested("netapp_ontap.models.quota_report_files.QuotaReportFilesSchema", data_key="files", unknown=EXCLUDE, allow_none=True)
    r""" The files field of the quota_report."""

    group = marshmallow_fields.Nested("netapp_ontap.models.quota_report_group.QuotaReportGroupSchema", data_key="group", unknown=EXCLUDE, allow_none=True)
    r""" The group field of the quota_report."""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Index that identifies a unique quota record. Valid in URL."""

    qtree = marshmallow_fields.Nested("netapp_ontap.models.quota_report_qtree.QuotaReportQtreeSchema", data_key="qtree", unknown=EXCLUDE, allow_none=True)
    r""" The qtree field of the quota_report."""

    space = marshmallow_fields.Nested("netapp_ontap.models.quota_report_space.QuotaReportSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the quota_report."""

    specifier = marshmallow_fields.Str(
        data_key="specifier",
        allow_none=True,
    )
    r""" Quota specifier"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the quota_report."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['tree', 'user', 'group']),
        allow_none=True,
    )
    r""" Quota type associated with the quota record.

Valid choices:

* tree
* user
* group"""

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.quota_report_users.QuotaReportUsersSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" This parameter specifies the target user or users associated with the given quota report record. This parameter is available for user quota records and is not available for group or tree quota records. The target user or users are identified by a user name and user identifier. The user name can be a UNIX user name or a Windows user name, and the identifer can be a UNIX user identifier or a Windows security identifier."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the quota_report."""

    @property
    def resource(self):
        return QuotaReport

    gettable_fields = [
        "links",
        "files",
        "group",
        "index",
        "qtree.links",
        "qtree.id",
        "qtree.name",
        "space",
        "specifier",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "users",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,files,group,index,qtree.links,qtree.id,qtree.name,space,specifier,svm.links,svm.name,svm.uuid,type,users,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "files",
        "group",
        "space",
        "svm.name",
        "svm.uuid",
        "users",
        "volume.name",
        "volume.uuid",
    ]
    """files,group,space,svm.name,svm.uuid,users,volume.name,volume.uuid,"""

    postable_fields = [
        "files",
        "group",
        "space",
        "svm.name",
        "svm.uuid",
        "users",
        "volume.name",
        "volume.uuid",
    ]
    """files,group,space,svm.name,svm.uuid,users,volume.name,volume.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in QuotaReport.get_collection(fields=field)]
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
            raise NetAppRestError("QuotaReport modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class QuotaReport(Resource):
    """Allows interaction with QuotaReport objects on the host"""

    _schema = QuotaReportSchema
    _path = "/api/storage/quota/reports"
    _keys = ["volume.uuid", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the quota report records for all FlexVol volumes and FlexGroup volumes.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="quota report show")
        def quota_report_show(
            fields: List[Choices.define(["index", "specifier", "type", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of QuotaReport resources

            Args:
                index: Index that identifies a unique quota record. Valid in URL.
                specifier: Quota specifier
                type: Quota type associated with the quota record.
            """

            kwargs = {}
            if index is not None:
                kwargs["index"] = index
            if specifier is not None:
                kwargs["specifier"] = specifier
            if type is not None:
                kwargs["type"] = type
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return QuotaReport.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all QuotaReport resources that match the provided query"""
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
        """Returns a list of RawResources that represent QuotaReport resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the quota report records for all FlexVol volumes and FlexGroup volumes.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific quota report record.
### Related ONTAP commands
* `quota report`

### Learn more
* [`DOC /storage/quota/reports`](#docs-storage-storage_quota_reports)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





