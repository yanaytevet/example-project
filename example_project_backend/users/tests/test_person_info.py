from typing import Dict

from django.db.models import QuerySet
from django.test import TestCase

from common.type_hints import JSONType
from users.consts.email_source import EmailSource
from users.models import PersonInfo
from users.models.email_address import EmailAddress


class TestPersonInfo(TestCase):
    def test_emails_1(self) -> None:
        person_info = PersonInfo()
        person_info.save()

        person_info.add_email('e1@g.c')
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': True, 'sources': [EmailSource.DEFAULT]}
        })

        person_info.add_email('e1@g.c')
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': True, 'sources': [EmailSource.DEFAULT]}
        })

        person_info.add_email('e1@g.c', source=EmailSource.PDL)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': True, 'sources': [EmailSource.DEFAULT, EmailSource.PDL]},
        })

        person_info.add_email('e2@g.c', source=EmailSource.PDL)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': True, 'sources': [EmailSource.DEFAULT, EmailSource.PDL]},
            'e2@g.c': {'is_primary': False, 'sources': [EmailSource.PDL]}
        })

        person_info.set_primary_email('e2@g.c', source=EmailSource.PDL)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': False, 'sources': [EmailSource.DEFAULT, EmailSource.PDL]},
            'e2@g.c': {'is_primary': True, 'sources': [EmailSource.PDL]}
        })

        person_info.set_primary_email('e1@g.c', source=EmailSource.BY_USER)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': True, 'sources': [EmailSource.DEFAULT, EmailSource.PDL, EmailSource.BY_USER]},
            'e2@g.c': {'is_primary': False, 'sources': [EmailSource.PDL]}
        })

        person_info.set_primary_email('e2@g.c', source=EmailSource.BY_USER)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': False, 'sources': [EmailSource.DEFAULT, EmailSource.PDL, EmailSource.BY_USER]},
            'e2@g.c': {'is_primary': True, 'sources': [EmailSource.PDL, EmailSource.BY_USER]}
        })

        person_info.add_email('e1@g.c', source=EmailSource.PDL)
        self.assert_emails(person_info.email_addresses, {
            'e1@g.c': {'is_primary': False, 'sources': [EmailSource.DEFAULT, EmailSource.PDL, EmailSource.BY_USER]},
            'e2@g.c': {'is_primary': True, 'sources': [EmailSource.PDL, EmailSource.BY_USER]}
        })

        self.assertEqual(person_info.has_primary_email(), True)

        self.assertEqual(person_info.get_primary_email(), 'e2@g.c')

        self.assertEqual(person_info.has_email_from_source(EmailSource.PDL), True)

        person_info.remove_email('e1@g.c')
        self.assert_emails(person_info.email_addresses, {
            'e2@g.c': {'is_primary': True, 'sources': [EmailSource.PDL, EmailSource.BY_USER]}
        })

    def assert_emails(self, emails_list: QuerySet[EmailAddress], wanted_emails_list: Dict[str, JSONType]) -> None:
        self.assertEqual(set(emails_list.values_list('address', flat=True)), set(wanted_emails_list.keys()))
        for email_obj in emails_list.all():
            wanted_email_obj = wanted_emails_list[email_obj.address]
            self.assertEqual(email_obj.is_primary_email, wanted_email_obj['is_primary'])
            sources = email_obj.sources
            sources.sort()
            wanted_sources = wanted_email_obj['sources']
            wanted_sources.sort()
            self.assertEqual(sources, wanted_sources)

