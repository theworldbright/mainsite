# django imports
from django import forms

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
