import pytest

from organisations.models import Organisation
from projects.models import Project
from environments.models import Environment
from segments.models import Segment, SegmentRule, Condition, EQUAL
from features.models import Feature


@pytest.fixture()
def organisation(db):
    return Organisation.objects.create(name="Test Organisation")


@pytest.fixture()
def project(organisation):
    return Project.objects.create(name="Test Project", organisation=organisation)


@pytest.fixture()
def environment(project):
    return Environment.objects.create(name="Test Environment", project=project)


@pytest.fixture()
def feature(project):
    return Feature.objects.create(name="test_feature", project=project)


@pytest.fixture()
def segment(project):
    segment = Segment.objects.create(name="Test Segment", project=project)
    rule = SegmentRule.objects.create(type=SegmentRule.ALL_RULE, segment=segment)
    condition = Condition.objects.create(operator=EQUAL, property="foo", value="bar")
    return segment
