from django.core import mail
from django.utils import unittest
from django.contrib.auth.models import User
from aspc.college.models import Term
from aspc.sagelist.models import BookSale
from aspc.sagelist import tasks
from decimal import Decimal
import datetime

class RenewalTasksTestCase(unittest.TestCase):
    urls = 'sagelist.urls' # Use different root for testing
    
    def setUp(self):
        self.password = '.'
        self.u = User.objects.create_user(
            'test_seller',
            password=self.password,
        )
        
        self.model_kwargs = {
            'title': "Test Tome (Before Edition)",
            'authors': "Some Guy",
            'condition': 0,
            'price': Decimal("47.00"),
            'seller': self.u,
            'expired': False,
        }
        
        self.date = Term.objects.last_active_term().end
        # self.before = BookSale(
        #     posted=self.date - datetime.timedelta(days=1),
        #     last_renewed=self.date = datetime.timedelta(days=1),
        #     **self.model_kwargs,
        # )
        self.sale = BookSale(
            posted=self.date - datetime.timedelta(days=1),
            last_renewed=self.date - datetime.timedelta(days=1),
            **self.model_kwargs
        )
        self.sale.save()
        # self.after = BookSale(
        #     posted=date - datetime.timedelta(days=1),
        #     last_renewed=date = datetime.timedelta(days=1),
        #     **self.model_kwargs,
        # )
    
    def tearDown(self):
        self.sale.delete()
        self.u.delete()
    
    def _check_email(self):
        self.assertEqual(
            mail.outbox[-1].subject,
            tasks.REMINDER_SUBJECT_TEMPLATE.format(self.sale.title),
            msg='Reminder email has wrong subject'
        )
    
    def _check_renew(self):
        # Renew BookSale
        self.client.login(username=self.u.username, password=self.password)
        response = self.client.get('/{0}/renew/{1}/'.format(
            self.sale.id,
            self.sale.token
        ))
        self.assertEqual(response.status_code, 302, msg='Not redirected on renew')
        
        sale = BookSale.objects.get(pk=self.sale.id) # Re-fetch from db
        self.assertTrue(sale.last_renewed > self.date, msg='last_renewed not updated')
        
        # Check false sale.expired
        self.assertFalse(self.sale.expired)
    
    def test_successful_first_renew(self):
        """
        Tests that a reminder email is sent, the book is renewed, and no
        followup is sent and the book is not expired
        """
        # Send reminders
        tasks.dispatch_reminder_emails()
        
        # Check for email
        self.assertEqual(len(mail.outbox), 1, msg='Reminder email not sent')
        self._check_email()
        
        # Renew BookSale
        self._check_renew()
        
        # Send followups
        tasks.dispatch_followup_emails()
        
        # Check that outbox still only has 1 message
        self.assertEqual(len(mail.outbox), 1, msg='Unexpected email sent')
    
    def test_successful_reminder_renew(self):
        """
        Tests that a reminder email is sent, a followup is sent, and the book
        is renewed and not expired
        """
        # Send reminders
        tasks.dispatch_reminder_emails()
        
        # Check for email
        self.assertEqual(len(mail.outbox), 1, msg='Reminder email not sent')
        self._check_email(count=1)
        
        # Send followups
        tasks.dispatch_followup_emails()
        
        # Check that outbox now has 2 messages
        self.assertEqual(len(mail.outbox), 2, msg='Followup email not sent')
        self._check_email()
        
        # Check that BookSale is expired
        self.assertTrue(self.sale.expired, msg='BookSale not marked expired')
        self.assertFalse(self.sale in BookSale.objects.active(),
            msg='BookSale present in active queryset')
        
        # n.b. If the test case ended here, we would have tested everything
        # for the 'sent reminder, sent followup, no renewal, expired listing'
        # case
        
        # Renew BookSale
        self._check_renew()
        
        # Check false sale.expired
        self.assertFalse(self.sale.expired)
