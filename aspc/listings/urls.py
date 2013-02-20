from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.listings.views import (ListingsView,
                                 ListingCreateView,
                                 ListingDetailView,
                                 ListingEditView,
                                 ListingDeleteView)

urlpatterns = patterns('',
    url(r'^$', ListingsView.as_view(), name="listings"),
    url(r'^create/$', ListingCreateView.as_view(), name="create_listing"),
    url(r'^(?P<pk>\d+)/$', ListingDetailView.as_view(), name="detailed_listing"),
    url(r'^(?P<pk>\d+)/edit/$', ListingEditView.as_view(), name="edit_listing"),
    url(r'^(?P<pk>\d+)/delete/$', ListingDeleteView.as_view(), name="delete_listing"),
)
# urlpatterns = patterns('',
#     url(r'^$', ListBookSalesView.as_view(), name="sagelist"),
#     url(r'^create/$', login_required(CreateBookSaleView.as_view()), name="sagelist_create"),
#     url(r'^(?P<pk>\d+)/$', BookSaleDetailView.as_view(), name="sagelist_detail"),
#     url(r'^(?P<pk>\d+)/delete/$', BookSaleDeleteView.as_view(), name="sagelist_delete"),
#     url(r'^(?P<username>[^/]+)/$', ListUserBookSalesView.as_view(), name="sagelist_user_listings"),
# )
