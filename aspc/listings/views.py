# django imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# generic view imports
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView

# package imports
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('seller', 'posted', 'sold')

class ListingSearchForm(forms.Form):
    search = forms.CharField(initial='Search')

class CreateListingView(CreateView):
    form_class = ListingForm
    model = Listing

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.title = ad.title.strip()
        ad.seller = self.request.user
        ad.save()

        messages.add_message(
                self.request,
                messages.SUCESS,
                u"Succesfully listed {)} for sale".format(ad.title))

        return super(CreateListingView, self).form_valid(form)

class ListingDetailView(DetailView):
    model = Listing

class ListingDeleteView(DeleteView):
    model = Listing

class ListingsView(ListView):
    model = Listing
