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

Install `django-minisentry` from PyPI:

```bash
pip install django-minisentry
```

# configure

```python
# settings.py
INSTALLED_APPS = [
    ...,
    'minisentry'
]

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

# urls.py
from django.urls import path, include

...

urlpatterns = [
    ...
    path("admin/_minisentry/", include('minisentry.urls')),
    path("admin/", admin.site.urls),
]
```

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
- rename debug
- search
- first_seen, last_seen
- graph on issue list
- x minutes ago
- event_id as primary
- permissions?
- colours
- stringify2 needs to escape html
- managment commands to delete old
- storage information, sizes
- rename to minisentry, never mini- mini_
- clean css
- prettify sql

# based on

- https://docs.djangoproject.com/en/4.2/intro/reusable-apps/
- https://docs.sentry.io/platforms/python/configuration/filtering/

# changelog

- 2023-08-10 rename to minisentry
- 2023-08-04 first rushed alpha version
