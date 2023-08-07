from django.test import TestCase

from common.time_utils import TimeUtils
from users.managers.timelines.timelines_groups_creator import TimelinesGroupsCreator
from users.models import User, UserEvent


class TestTimelinesGroupsCreator(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user('user1', 'user1', 'pass1')
        self.user_2 = User.objects.create_user('user2', 'user2', 'pass2')
        self.user_3 = User.objects.create_user('user3', 'user3', 'pass3')

    def test_get_suggested_times_engagements_empty(self) -> None:
        creator = TimelinesGroupsCreator([self.user_1, self.user_2], TimeUtils.create_aware_datetime(2020, 1, 2),
                                         TimeUtils.create_aware_datetime(2020, 1, 3))
        creator.set_buffer(10 * 60)

        timelines = creator.generate_timelines()
        self.assertEqual(timelines, [
            {'user_id': self.user_1.id, 'user_full_name': self.user_1.get_full_name(), 'segments': []},
            {'user_id': self.user_2.id, 'user_full_name': self.user_2.get_full_name(), 'segments': []},
        ])

    def test_get_suggested_times_engagements_1(self) -> None:
        self.create_user_event(self.user_1, 2020, 1, 1, 0, 0)
        self.create_user_event(self.user_2, 2020, 1, 1, 0, 0)
        self.create_user_event(self.user_3, 2020, 1, 1, 0, 0)
        self.create_user_event(self.user_1, 2020, 1, 1, 23, 0)
        self.create_user_event(self.user_2, 2020, 1, 1, 23, 0)
        self.create_user_event(self.user_3, 2020, 1, 1, 22, 0)
        self.create_user_event(self.user_1, 2020, 1, 1, 23, 59)

        self.create_user_event(self.user_1, 2020, 1, 2, 0, 1)
        self.create_user_event(self.user_2, 2020, 1, 2, 0, 9)
        self.create_user_event(self.user_3, 2020, 1, 2, 0, 9)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 10)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 12)
        self.create_user_event(self.user_2, 2020, 1, 2, 0, 14)
        self.create_user_event(self.user_3, 2020, 1, 2, 0, 14)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 16)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 27)
        self.create_user_event(self.user_2, 2020, 1, 2, 0, 30)
        self.create_user_event(self.user_3, 2020, 1, 2, 0, 30)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 35)
        self.create_user_event(self.user_1, 2020, 1, 2, 0, 40)
        self.create_user_event(self.user_1, 2020, 1, 2, 1, 40)
        self.create_user_event(self.user_3, 2020, 1, 2, 1, 43)

        self.create_user_event(self.user_1, 2020, 1, 3, 0, 9)
        self.create_user_event(self.user_2, 2020, 1, 3, 0, 1)
        self.create_user_event(self.user_3, 2020, 1, 3, 1, 0)

        creator = TimelinesGroupsCreator([self.user_1, self.user_2], TimeUtils.create_aware_datetime(2020, 1, 2),
                                         TimeUtils.create_aware_datetime(2020, 1, 3))
        creator.set_buffer(10 * 60)

        timelines = creator.generate_timelines()
        self.assertEqual(len(timelines), 2)
        self.assertEqual(timelines[0],
            {'user_id': self.user_1.id, 'user_full_name': self.user_1.get_full_name(), 'segments': [
                {'end_datetime': '2020-01-02T00:16:00.000000+0000',
                 'start_datetime': '2020-01-02T00:01:00.000000+0000'},
                {'end_datetime': '2020-01-02T00:40:00.000000+0000',
                 'start_datetime': '2020-01-02T00:27:00.000000+0000'},
                {'end_datetime': '2020-01-02T01:40:00.000000+0000',
                 'start_datetime': '2020-01-02T01:40:00.000000+0000'},
            ]})
        self.assertEqual(timelines[1],
            {'user_id': self.user_2.id, 'user_full_name': self.user_2.get_full_name(), 'segments': [
                {'end_datetime': '2020-01-02T00:14:00.000000+0000',
                 'start_datetime': '2020-01-02T00:09:00.000000+0000'},
                {'end_datetime': '2020-01-02T00:30:00.000000+0000',
                 'start_datetime': '2020-01-02T00:30:00.000000+0000'},
            ]})

    def create_user_event(self, user: User, year: int, month: int, day: int, hour: int, minute: int):
        time = TimeUtils.create_aware_datetime(year, month, day, hour, minute)
        UserEvent(name='test_event', user=user, creation_time=time).save()
