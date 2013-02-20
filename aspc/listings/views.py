# django imports
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# generic view imports
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

# package imports
from .models import Listing
from .forms import ContactForm

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('seller', 'posted', 'sold')

class ListingEditForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('seller', 'sold')

class ListingSearchForm(forms.Form):
    search = forms.CharField(initial='Search')

class ListingCreateView(CreateView):
    form_class = ListingForm
    model = Listing

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.title = ad.title.strip()
        ad.seller = self.request.user
        ad.save()

        messages.add_message(
                self.request,
                messages.SUCCESS,
                u"Succesfully listed {0} for sale".format(ad.title))

        return super(ListingCreateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListingCreateView, self).dispatch(*args, **kwargs)


class ListingDetailView(DetailView, FormView):
    model = Listing
    form_class = ContactForm

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        return super(ListingDetailView, self).post(*args, **kwargs)

    def form_valid(self, form):
        print "Succeeded"
        # TODO: add more useful stuff (add to messages, send emails)
        return super(ListingDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        new_context = kwargs
        form_class = self.get_form_class()
        self.object = self.get_object()
        self.initial = {
                    'subject': 'Re: {}'.format(self.object.title),
                    'message': 'Hi,\n\nI saw your listing "{}" and was interested in making a purchase. If it is still for sale, could you contact me at {}?\n\nThanks!'.format(self.object.title, self.request.user.email)
                }
        new_context.update(super(DetailView, self).get_context_data())
        new_context.update({'form': self.get_form(form_class),})
        return new_context

    def get_success_url(self):
        return reverse('detailed_listing', kwargs={'pk' : self.get_object().id})

class ListingEditView(UpdateView):
    form_class = ListingEditForm
    model = Listing

class ListingDeleteView(DeleteView):
    model = Listing
    success_url = "/listings/"

    def get_object(self, queryset=None):
        obj = super(ListingDeleteView, self).get_object()
        if not self.request.user == obj.seller:
            raise HttpResponseForbidden
        return obj

class ListingsView(ListView):
    model = Listing
