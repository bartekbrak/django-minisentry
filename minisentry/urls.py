from django.urls import path

from minisentry.views import issues_first, browse_event, trigger_example_error

urlpatterns = [
    path('issues_first/<str:hash_>', issues_first, name='issues_first',),
    path('browse_event/<str:id_>', browse_event, name='browse_event',),
    path('trigger_example_error', trigger_example_error, name='trigger_example_error'),
]
