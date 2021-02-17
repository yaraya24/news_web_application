from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model


from .forms import CustomUserCreationForm

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/signup.html'

class ProfilePage(generic.DetailView):

    model = get_user_model()

    template_name = 'profile.html'

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        context['news_orgs'] = 'lol'
        return context

