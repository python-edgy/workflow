from django.conf.urls import url
from django.contrib import admin

from example.workflow_app.views import IssueListView, IssueCreateView, IssueDetailView, IssueTransitionView

urlpatterns = [
    url(r'^$', IssueListView.as_view(), name='issue-list'),
    url(r'^create$', IssueCreateView.as_view(), name='issue-create'),
    url(r'^(?P<pk>\d+)$', IssueDetailView.as_view(), name='issue-detail'),
    url(r'^(?P<pk>\d+)/transition/(?P<transition>[\w-]+)$', IssueTransitionView.as_view(), name='issue-transition'),
    url(r'^admin/', admin.site.urls),
]
