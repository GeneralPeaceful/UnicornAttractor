from django.conf.urls import url
from .views import bugs, bug, features, feature, add_bug, add_feature, add_vote, edit_bug, edit_feature

urlpatterns = [
    url(r'^bugs$', bugs, name='bugs'),
    url(r'^bug/(?P<bugid>\d+)/$', bug, name='bug'),
    url(r'^features$', features, name='features'),
    url(r'^feature/(?P<featureid>\d+)/$', feature, name='feature'),
    url(r'^addbug', add_bug, name='add_bug'),
    url(r'^addfeature', add_feature, name='add_feature'),
    url(r'^addvote/(?P<bugid>\d+)/$', add_vote, name='add_vote'),
    url(r'^editbug/(?P<bugid>\d+)/$', edit_bug, name='edit_bug'),
    url(r'^editfeature/(?P<featureid>\d+)/$', edit_feature, name='edit_feature'),
]