# minisentry

A Django reusable app to extend sentry-sdk with ability to collect errors in
local database rather than send to sentry. An admin panel is provided to browse
grouped issues.

This app is useful when for some reason you cannot use sentry.io interface,
maybe you can't send data to third party vendors, maybe you can't have a
self-hosted version.

This is a very simple app, it hooks into sentry_sdk.init.before_send function,
serializes the events into json and stores them in the database.

Thjs app is written in rush to get first working version out, I test the app in
my application and only maybe will add automatic tests if it gets used.

I analysed the datastructures emitted by sentry-sdk and hae some confidence that
I didn't miss anything. The app will store the raw event as a whole, so if I
missed anything, corrections to the main template should be enough. It is a
recoverbale mistake.

This app will obviously only work for errors that don't relate to database
connection itself. You have to have working django and connection to store them.

Versioning: calver, I only care for the most recent version of sentry-sdk,
python and django, but likely it will work with some lower versions.

I start with implementing only what I need, with time I will add more stuff.

# install

    pip install django-minisentry

    # settings.py
    INSTALLED_APPS = [
        ...,
        'minisentry'
    ]

    # urls.py
    urlpatterns = [
        ...
        path('minisentry/', include('minisentry.urls')),
        ...
    ]

    # wherever you setup sentry_sdk
    from minisentry import store
    sentry_sdk.init(
        ...,
        before_send = store(
            send=False,            # default
            event_callback=print,  # maybe for debug
            hint_callback=print,   # maybe for debug
            ignore_errors=(ZeroDivisionError, KeyboardInterrupt)
        )
    )

# develop

    git clone https://github.com/bartekbrak/django-minisentry
    pip install -e django-minisentry

# legal

Dear Sentry, please don't sue me. This project is for people who cannot use your
wonderful, best-in-class product. I'm your biggest fan and evangelise your paid
version where I can. This all is in good faith, but it does abuse your SDK, you
didn't build it so that we can store your events elsewhere. Thanks.

# todo

- tests
- backlinks, in admin, in browse
- search
- graph on issue list
- x minutes ago
- permissions?
- colours
- stringify2 needs to escape html
- management commands to delete old
- storage information, sizes
- clean css
- prettify sql

# based on

- https://docs.djangoproject.com/en/4.2/intro/reusable-apps/
- https://docs.sentry.io/platforms/python/configuration/filtering/

# build and release (to myself)

    pip install -e .
    pip install -U setuptools wheel build twine
    # change "version = ????????" in setup.cfg
    rm dist/* && python -m build --wheel &&  twine check dist/* && twine upload dist/*

# changelog

- 2023-08-24 handle logger.error
- 2023-08-17 display tags set via `sentry_sdk.set_tag("sth", "sth")`
- 2023-08-11 ignore_errors, expand README
- 2023-08-10 rename to minisentry
- 2023-08-04 first rushed alpha version
