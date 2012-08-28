from django.contrib.sites.models import Site
from celery.task import task
from aspc.sagelist.models import BookSale
from aspc.college.models import Term

REMINDER_SUBJECT_TEMPLATE = u"Renew your SageBooks listing for {0} with a single click"

def _site_info():
    return {
        'domain': Site.objects.get_current().domain,
        'protocol': 'http', # TODO: this will need to be changed when ASPC
                            # goes all https
    }

@task
def send_renew_reminder(booksale_id, template):
    logger = send_renew_reminder.get_logger()
    try:
        booksale = BookSale.objects.get(pk=booksale_id)
    except BookSale.DoesNotExist:
        logger.warn("BookSale with id = {0} does not exist "
                    "in db, can't send reminder".format(booksale_id))
        return
    
    email_context = {'seller': booksale.seller, 'booksale': booksale,}
    email_context.update(_site_info())
    
    booksale.seller.email_user(
        REMINDER_SUBJECT_TEMPLATE.format(booksale.title),
        render_to_string(template, email_context)
    )
    logger.info("Successfully sent reminder email to {0} [{1}]".format(
        booksale.seller))

@task
def dispatch_reminder_emails():
    logger = dispatch_reminder_emails.get_logger()
    expiring = BookSale.objects.expiring()
    logger.info("Sending reminders for {0} sales...".format(expiring.count()))
    
    # Spawn reminder email tasks
    for booksale in expiring:
        send_renew_reminder.delay(booksale.pk, "sagelist/renew_listing_request.txt")
    logger.info("Spawned the reminder email tasks!")

@task
def dispatch_followup_emails():
    logger = dispatch_followup_emails.get_logger()
    expiring = BookSale.objects.expiring()
    logger.info("Sending reminders for {0} booksales...".format(expiring.count()))
    
    # Spawn reminder email tasks
    for booksale in expiring:
        send_renew_reminder.delay(booksale.pk, "sagelist/renew_listing_request.txt")
    logger.info("Spawned the reminder email tasks!")
    
    # Mark old booksales as expired
    expiring.update(expired=True)
    logger.info("Marked old booksales as expired!")
