import logging

from django.template.response import TemplateResponse
from django.contrib import admin
from minisentry.models import SentryEvent

logger = logging.getLogger(__name__)


def _template(request, sentry_event:SentryEvent):
    return TemplateResponse(
        request,
        'minisentry/show.html',
        context={
            'event': sentry_event.event,
            'hash': sentry_event.issue.hash,
            'raw': sentry_event.json,
            'tags': sentry_event.tags,
            'events_count': 1,
            **admin.site.each_context(request)
        }
    )


def issues_first(request, hash_):
    return _template(request, SentryEvent.objects.filter(issue__hash=hash_).select_related('issue').order_by('created').last())


def browse_event(request, id_):
    return _template(request, SentryEvent.objects.get(id=id_))


def trigger_example_error(request):
    logger.debug('sent from logger.debug')
    logger.info('sent from logger.info')
    logger.warning('sent from logger.warning')
    logger.error('sent from logger.error')
    'just an error' + 3.14
