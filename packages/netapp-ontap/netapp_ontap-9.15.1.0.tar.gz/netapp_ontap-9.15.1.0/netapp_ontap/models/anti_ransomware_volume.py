r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolume", "AntiRansomwareVolumeSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeSchema.resource": False,
    "AntiRansomwareVolumeSchema.opts": False,
    "AntiRansomwareVolume": False,
}


class AntiRansomwareVolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolume object"""

    attack_probability = marshmallow_fields.Str(data_key="attack_probability", allow_none=True)
    r""" Probability of a ransomware attack.<br>`none` No files are suspected of ransomware activity.<br>`low` A number of files are suspected of ransomware activity.<br>`moderate` A moderate number of files are suspected of ransomware activity.<br>`high` A large number of files are suspected of ransomware activity.

Valid choices:

* none
* low
* moderate
* high """

    attack_reports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_attack_report.AntiRansomwareAttackReportSchema", unknown=EXCLUDE, allow_none=True), data_key="attack_reports", allow_none=True)
    r""" The attack_reports field of the anti_ransomware_volume. """

    dry_run_start_time = ImpreciseDateTime(data_key="dry_run_start_time", allow_none=True)
    r""" Time when Anti-ransomware monitoring `state` is set to dry-run value for starting evaluation mode. """

    event_log = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_event_log.AntiRansomwareVolumeEventLogSchema", unknown=EXCLUDE, data_key="event_log", allow_none=True)
    r""" The event_log field of the anti_ransomware_volume. """

    space = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_space.AntiRansomwareVolumeSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the anti_ransomware_volume. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Anti-ransomware state.<br>`disabled` Anti-ransomware monitoring is disabled on the volume.  This is the default state in a POST operation.<br>`disable_in_progress` Anti-ransomware monitoring is being disabled and a cleanup operation is in effect. Valid in GET operation.<br>`dry_run` Anti-ransomware monitoring is enabled in the evaluation mode.<br>`enabled` Anti-ransomware monitoring is active on the volume.<br>`paused` Anti-ransomware monitoring is paused on the volume.<br>`enable_paused` Anti-ransomware monitoring is paused on the volume from its earlier enabled state. Valid in GET operation. <br>`dry_run_paused` Anti-ransomware monitoring is paused on the volume from its earlier dry_run state. Valid in GET operation. <br>For POST, the valid Anti-ransomware states are only `disabled`, `enabled` and `dry_run`, whereas for PATCH, `paused` is also valid along with the three valid states for POST.

Valid choices:

* disabled
* disable_in_progress
* dry_run
* enabled
* paused
* enable_paused
* dry_run_paused """

    surge_as_normal = marshmallow_fields.Boolean(data_key="surge_as_normal", allow_none=True)
    r""" Indicates whether or not to set the surge values as historical values. This field is no longer supported. Use update-baseline-from-surge instead. """

    suspect_files = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_suspect_files.AntiRansomwareVolumeSuspectFilesSchema", unknown=EXCLUDE, allow_none=True), data_key="suspect_files", allow_none=True)
    r""" The suspect_files field of the anti_ransomware_volume. """

    update_baseline_from_surge = marshmallow_fields.Boolean(data_key="update_baseline_from_surge", allow_none=True)
    r""" Sets the observed surge value as the new baseline on a volume. """

    @property
    def resource(self):
        return AntiRansomwareVolume

    gettable_fields = [
        "attack_probability",
        "attack_reports",
        "dry_run_start_time",
        "event_log",
        "space",
        "state",
        "surge_as_normal",
        "suspect_files",
        "update_baseline_from_surge",
    ]
    """attack_probability,attack_reports,dry_run_start_time,event_log,space,state,surge_as_normal,suspect_files,update_baseline_from_surge,"""

    patchable_fields = [
        "event_log",
        "state",
        "surge_as_normal",
        "update_baseline_from_surge",
    ]
    """event_log,state,surge_as_normal,update_baseline_from_surge,"""

    postable_fields = [
        "event_log",
        "state",
        "surge_as_normal",
        "update_baseline_from_surge",
    ]
    """event_log,state,surge_as_normal,update_baseline_from_surge,"""


class AntiRansomwareVolume(Resource):

    _schema = AntiRansomwareVolumeSchema
