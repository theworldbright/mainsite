from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.listings.views import (ListingsView, CreateListingView, DetailedListingView, EditListingView)

urlpatterns = patterns('',
    url(r'^S', ListingsView.as_view(), name="listings"),
    url(r'^create', CreateListingView.as_view(), name="create_listing"),
    url(r'^(?P<pk>\d+)/$', DetailedListingView.as_view(), name="detailed_listing"),
    url(r'^(?P<pk>\d+)/edit/$', EditListingView.as_view(), name="edit_listing"),
)
# urlpatterns = patterns('',
#     url(r'^$', ListBookSalesView.as_view(), name="sagelist"),
#     url(r'^create/$', login_required(CreateBookSaleView.as_view()), name="sagelist_create"),
#     url(r'^(?P<pk>\d+)/$', BookSaleDetailView.as_view(), name="sagelist_detail"),
#     url(r'^(?P<pk>\d+)/delete/$', BookSaleDeleteView.as_view(), name="sagelist_delete"),
#     url(r'^(?P<username>[^/]+)/$', ListUserBookSalesView.as_view(), name="sagelist_user_listings"),
# )
