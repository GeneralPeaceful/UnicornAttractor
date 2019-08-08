from django.conf.urls import url
from .views import view_cart, add_to_cart, remove_from_cart, checkout, charge, update_cart

urlpatterns = [
    url(r'^$', view_cart, name='view_cart'),
    url(r'^add/(?P<featureid>\d+)/$', add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<featureid>\d+)/$', remove_from_cart, name='remove_from_cart'),
    url(r'^update_cart/(?P<featureid>\d+)/$', update_cart, name='update_cart'),
    url(r'^charge/$', charge, name='charge'),
]