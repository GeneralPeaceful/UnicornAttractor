from django.conf.urls import url, include
from django.views.generic import RedirectView
from .views import register, logout, login

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login/')),
    url(r'^register/$', register, name='register'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
]
