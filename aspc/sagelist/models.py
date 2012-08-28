from django.db import models
from django.contrib.auth.models import User
from aspc.college.models import Term

class BookSaleManager(models.Manager):
    def expiring(self):
        return self.filter(expired=False, buyer__isnull=True,
            last_renewed__lt=Term.objects.last_active_term().end)
    
    def expired(self):
        return self.filter(expired=True)
    
    def active(self):
        return self.filter(expired=False, buyer__isnull=True)

class BookSale(models.Model):
    CONDITIONS = (
        (0, "like new"),
        (1, "very good"),
        (2, "good"),
        (3, "usable"),
    )
    """Model representing a sale of a textbook"""
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, verbose_name="Author(s)")
    isbn = models.CharField(max_length=20, null=True, blank=True, verbose_name="ISBN")
    edition = models.CharField(max_length=20, null=True, blank=True)
    condition = models.IntegerField(choices=CONDITIONS)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    seller = models.ForeignKey(User, related_name="book_sales_set")
    buyer = models.ForeignKey(User, null=True, blank=True, related_name="book_purchases_set")
    
    posted = models.DateTimeField(auto_now_add=True)
    last_renewed = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=20, null=True, blank=True, verbose_name="Renewal Token")
    expired = models.BooleanField()
    
    objects = BookSaleManager()
    
    class Meta:
        ordering = ['posted']

    def __unicode__(self):
        return u"BookSale: {0} by {1} ({2})".format(self.title, self.authors, self.seller.username)

    @models.permalink
    def get_absolute_url(self):
        return ('sagelist_detail', [self.id])