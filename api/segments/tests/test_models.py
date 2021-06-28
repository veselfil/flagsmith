from unittest import TestCase, mock

import pytest

import segments
from environments.identities.models import Identity
from environments.models import Environment
from organisations.models import Organisation
from projects.models import Project
from segments.models import PERCENTAGE_SPLIT, Condition, Segment, SegmentRule


@pytest.mark.django_db
class SegmentTestCase(TestCase):
    def setUp(self) -> None:
        self.organisation = Organisation.objects.create(name="Test Org")
        self.project = Project.objects.create(
            name="Test Project", organisation=self.organisation
        )
        self.environment = Environment.objects.create(
            name="Test Environment", project=self.project
        )
        self.identity = Identity.objects.create(
            environment=self.environment, identifier="test_identity"
        )

    def tearDown(self) -> None:
        Segment.objects.all().delete()
        Identity.objects.all().delete()


@pytest.mark.django_db
class SegmentRuleTest(TestCase):
    def setUp(self) -> None:
        self.organisation = Organisation.objects.create(name="Test Org")
        self.project = Project.objects.create(
            name="Test Project", organisation=self.organisation
        )
        self.environment = Environment.objects.create(
            name="Test Environment", project=self.project
        )
        self.identity = Identity.objects.create(
            environment=self.environment, identifier="test_identity"
        )
        self.segment = Segment.objects.create(project=self.project, name="test_segment")


@pytest.mark.django_db
class ConditionTest(TestCase):
    def setUp(self) -> None:
        self.organisation = Organisation.objects.create(name="Test Org")
        self.project = Project.objects.create(
            name="Test Project", organisation=self.organisation
        )
        self.environment = Environment.objects.create(
            name="Test Environment", project=self.project
        )
        self.identity = Identity.objects.create(
            environment=self.environment, identifier="test_identity"
        )
        self.segment = Segment.objects.create(project=self.project, name="test_segment")
        self.rule = SegmentRule.objects.create(
            segment=self.segment, type=SegmentRule.ALL_RULE
        )

    @mock.patch("segments.models.get_hashed_percentage_for_object_ids")
    def test_percentage_split_calculation_divides_value_by_100_before_comparison(
        self, mock_get_hashed_percentage_for_object_ids
    ):
        # Given
        condition = Condition(rule=self.rule, operator=PERCENTAGE_SPLIT, value=10)
        mock_get_hashed_percentage_for_object_ids.return_value = 0.2
        mock_segment = mock.MagicMock(id=1)

        # When
        res = condition.does_identity_match(self.identity, mock_segment)

        # Then
        assert not res
