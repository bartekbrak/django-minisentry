import json
from functools import cached_property

from django.db import models
from minisentry import hashing_function


class SentryIssue(models.Model):
    hash = models.CharField(max_length=32, primary_key=True)
    title = models.TextField()
    where = models.TextField()
    exception_value = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} {self.where} {self.exception_value}'

    @staticmethod
    def _model_fields_from_event(event: dict):
        return {
            'title': event['exception']['values'][0]['type'],
            'where': event.get('transaction', event['exception']['values'][0]['module']),
            'exception_value': event['exception']['values'][0]['value']
        }

class SentryEvent(models.Model):
    id = models.CharField(max_length=32, primary_key=True, help_text='example: 7bfcbdef7a754da985f8e69d64d1299c')
    issue = models.ForeignKey(SentryIssue, on_delete=models.CASCADE)
    json = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'SentryEvent {self.issue}'

    @cached_property
    def event(self):
        event = json.loads(self.json)
        self._add_context_line_numbers(event)
        return event

    @staticmethod
    def _add_context_line_numbers(event):
        # idempotent
        for exception in event['exception']['values']:
            for frame in exception['stacktrace']['frames']:
                lines_no_pre_context = len(frame['pre_context'])
                for i, line in enumerate(frame['pre_context']):
                    frame['pre_context'][i] = [int(frame['lineno']) - lines_no_pre_context + i, line]
                for i, line in enumerate(frame['post_context']):
                    frame['post_context'][i] = [int(frame['lineno']) + i + 1, line]

    @cached_property
    def tags(self):
        return {
            'environment': self.event['environment'],
            'release': self.event['release'],
            'level': self.event['level'],
            'mechanism': self.event['exception']['values'][0]['mechanism']['type'],
            'server_name': self.event['server_name'],
            # conditional, url is not always present, this will break
            'transaction': self.event.get('transaction', ''),
            'url': self.event['request']['url'] if 'request' in self.event else '',
        }

    @classmethod
    def example(cls):
        # debug mainly
        with open('minisentry/event_samples/event1.json') as f:
            event = f.read()
            hash_ = hashing_function(json.loads(event))
        return cls(hash=hash_, json=event)
