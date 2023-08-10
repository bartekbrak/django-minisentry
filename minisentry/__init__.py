import hashlib
import json
import logging
from typing import Callable


logger = logging.getLogger()


def hashing_function(event: dict) -> str:
    """
    This part I feel least confident about but mistakes can be corrected later on.
    The hash result of this function is used to group events into issues.
    Sentry does this server side but exposes details in the UI very clearly marking what was taken into account
    when creating hash. Yet, edge cases will fail if I don't guess well what their events will be like.

    The goal is to always provide the same hash for all parts, regardless of where it is run.
    # what if there are no frames?

    # https://stackoverflow.com/a/74052716
    """
    # for every frame in every stacktrace in exception section, take module, function, context_line
    parts = [
        # exception in html will have no module and no function
        frame.get('module', '')
        + frame.get('function', '') + frame['context_line']
        for value in event['exception']['values']
        for frame in value['stacktrace']['frames']
    ]
    if parts:
        to_hash = '\n'.join(parts).encode()
    else:
        # guessing, I have not seen exceptions without traceback yet, but I guess they do happen
        to_hash = event['transaction'].encode()
    logger.debug('to_hash:\n%s', to_hash)
    return hashlib.shake_128(to_hash).hexdigest(16)


def store(send=False, event_callback: Callable = None, hint_callback: Callable = None):
    """
    # wherever you setup sentry_sdk
    from minisentry import store
    sentry_sdk.init(
        ...,
        before_send = store(
            send=False,            # default
            event_callback=print,  # maybe for debug
            hint_callback=print,   # maybe for debug
        )
    )
    """
    def inner(event, hint):
        from minisentry.models import SentryEvent
        from minisentry.models import SentryIssue
        logger.info('calling before_send')
        try:
            hash_ = hashing_function(event)
            fields = SentryIssue._model_fields_from_event(event)
            logger.debug('calling before_send: hash: %r, fields: %r', hash_, fields)
            sissue, created =  SentryIssue.objects.get_or_create(
                hash=hash_,
                **fields,
            )
            logger.info('SentryEvent: %s, created: %r', sissue, created)
            sevent = SentryEvent.objects.create(
                id=event['event_id'],
                issue=sissue,
                json=json.dumps(event),
            )
            logger.info('created SentryEvent: %s', sevent)
        except Exception as e:
            logger.debug('unhandles exception in minisentry itself, will not reach sentry: %r', e)
        if event_callback:
            event_callback(event)
        if hint_callback:
            hint_callback(hint)
        if send:
            return event
        return None
    return inner
