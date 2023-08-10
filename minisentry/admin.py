import json

from django.contrib import admin
from django.db.models import Count, Max, Min
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from minisentry.models import SentryEvent, SentryIssue


class ReadOnlyAdmin(admin.ModelAdmin):
    def _no(self, *_args, **_kwargs):
        return False
    has_add_permission = has_change_permission =  _no

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(SentryIssue)
class SentryIssueAdmin(ReadOnlyAdmin):
    list_display = (
        'created', 'hash', 'title', 'where', 'exception_value', 'issues_first',
        'first_seen', 'last_seen', 'count'
    )
    # TODO: list events link
    ordering = '-created',

    def count(self, obj):
        return obj.count

    def first_seen(self, obj):
        return obj.first_seen

    def last_seen(self, obj):
        return obj.last_seen

    def get_queryset(self, request):
        # inefficient?
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(count=Count("sentryevent"))
        queryset = queryset.annotate(first_seen=Min("sentryevent__created"))
        queryset = queryset.annotate(last_seen=Max("sentryevent__created"))
        return queryset

    def issues_first(self, obj):
        return format_html("<a href='{url}'>browse most recent</a>", url=reverse('issues_first', args=(obj.hash,)))


@admin.register(SentryEvent)
class SentryEventAdmin(ReadOnlyAdmin):
    list_display = 'id', 'created', 'browse_event', 'issue',  # 'issue_link'
    list_display_links = 'id',
    list_select_related = 'issue',
    ordering = '-created',

    fields = (
        'created',
        'issue',
        'pretty',
    )
    readonly_fields = fields

    def browse_event(self, obj):
        return format_html("<a href='{url}'>browse</a>", url=reverse('browse_event', args=(obj.id,)))

    def issue_link(self, obj):
        return '?'

    def pretty(self, obj):
        dumps = json.dumps(json.loads(obj.json), indent=4)
        return mark_safe(f'<pre>{dumps}</pre>')
