import datetime as dt

import pytest
import pytz

import stix2

from .constants import FAKE_TIME, INDICATOR_ID, INDICATOR_KWARGS
from .fixtures import clock, uuid4, indicator  # noqa: F401

EXPECTED_INDICATOR = """{
    "created": "2017-01-01T00:00:01Z",
    "id": "indicator--01234567-89ab-cdef-0123-456789abcdef",
    "labels": [
        "malicious-activity"
    ],
    "modified": "2017-01-01T00:00:01Z",
    "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    "type": "indicator",
    "valid_from": "1970-01-01T00:00:01Z"
}"""

EXPECTED_INDICATOR_REPR = "Indicator(" + " ".join("""
    created=datetime.datetime(2017, 1, 1, 0, 0, 1, tzinfo=<UTC>),
    id='indicator--01234567-89ab-cdef-0123-456789abcdef',
    labels=['malicious-activity'],
    modified=datetime.datetime(2017, 1, 1, 0, 0, 1, tzinfo=<UTC>),
    pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    type='indicator',
    valid_from=datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=<UTC>)
""".split()) + ")"


def test_indicator_with_all_required_fields():
    now = dt.datetime(2017, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    epoch = dt.datetime(1970, 1, 1, 0, 0, 1, tzinfo=pytz.utc)

    ind = stix2.Indicator(
        type="indicator",
        id=INDICATOR_ID,
        labels=['malicious-activity'],
        pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
        created=now,
        modified=now,
        valid_from=epoch,
    )

    assert str(ind) == EXPECTED_INDICATOR
    assert repr(ind) == EXPECTED_INDICATOR_REPR


def test_indicator_autogenerated_fields(indicator):  # noqa: F811
    assert indicator.type == 'indicator'
    assert indicator.id == 'indicator--00000000-0000-0000-0000-000000000001'
    assert indicator.created == FAKE_TIME
    assert indicator.modified == FAKE_TIME
    assert indicator.labels == ['malicious-activity']
    assert indicator.pattern == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator.valid_from == FAKE_TIME

    assert indicator['type'] == 'indicator'
    assert indicator['id'] == 'indicator--00000000-0000-0000-0000-000000000001'
    assert indicator['created'] == FAKE_TIME
    assert indicator['modified'] == FAKE_TIME
    assert indicator['labels'] == ['malicious-activity']
    assert indicator['pattern'] == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator['valid_from'] == FAKE_TIME


def test_indicator_type_must_be_indicator():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator(type='xxx', **INDICATOR_KWARGS)

    assert str(excinfo.value) == "Invalid value for Indicator 'type': must equal 'indicator'."


def test_indicator_id_must_start_with_indicator():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator(id='my-prefix--', **INDICATOR_KWARGS)

    assert str(excinfo.value) == "Invalid value for Indicator 'id': must start with 'indicator--'."


def test_indicator_required_fields():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator()
    assert str(excinfo.value) == "Missing required field(s) for Indicator: (labels, pattern)."


def test_indicator_required_field_pattern():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator(labels=['malicious-activity'])
    assert str(excinfo.value) == "Missing required field(s) for Indicator: (pattern)."


def test_indicator_created_ref_invalid_format():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator(created_by_ref='myprefix--12345678', **INDICATOR_KWARGS)
    assert str(excinfo.value) == "Invalid value for Indicator 'created_by_ref': must match <object-type>--<guid>."


def test_indicator_revoked_invalid():
    with pytest.raises(ValueError) as excinfo:
        stix2.Indicator(revoked='no', **INDICATOR_KWARGS)
    assert str(excinfo.value) == "Invalid value for Indicator 'revoked': must be a boolean value."


def test_cannot_assign_to_indicator_attributes(indicator):  # noqa: F811
    with pytest.raises(ValueError) as excinfo:
        indicator.valid_from = dt.datetime.now()

    assert str(excinfo.value) == "Cannot modify properties after creation."


def test_invalid_kwarg_to_indicator():
    with pytest.raises(TypeError) as excinfo:
        stix2.Indicator(my_custom_property="foo", **INDICATOR_KWARGS)
    assert str(excinfo.value) == "unexpected keyword arguments: ['my_custom_property']"


def test_created_modified_time_are_identical_by_default():
    """By default, the created and modified times should be the same."""
    ind = stix2.Indicator(**INDICATOR_KWARGS)

    assert ind.created == ind.modified
