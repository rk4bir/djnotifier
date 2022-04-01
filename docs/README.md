# djnotifier
>**djnotifier** is a Django app to conduct web-based real time notification.


# Quick start
> Guide to setup `djnotifier` into your Django project

## Requirements
1. System requirements: **`Redis server`**
2. `pip3` packages -
    ```text
    channels
    channels-redis
    ```
   and off course `django` itself.

## Install and configure
### Step-0
```shell
pip install djnotifier
```

### Step-1
Add **djnotifier** to your `INSTALLED_APPS` setting like this

 ```python
INSTALLED_APPS = [
     ...
     'djnotifier',
 ]
 ```

### Step-2
Setup `asgi` application for the project

1. Update `asgi.py`
   ```python
   # <project>/asgi.py
   import os
   
   from django.core.asgi import get_asgi_application
   from channels.auth import AuthMiddlewareStack
   from channels.routing import ProtocolTypeRouter, URLRouter
   
   # import web-socket routes from djnotifier
   from djnotifier.routing import websocket_urlpatterns
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<project_name>.settings')
   
   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": AuthMiddlewareStack(
           URLRouter(
               websocket_urlpatterns
           )
       ),
   })
   ```
2. Configure `asgi` application in `settings` 
   ```python
   # <project>/config.py
   ...
   ASGI_APPLICATION = '<project>.asgi.application'
   ```

### Step-3
Configure `redis` layer
```python
# <project>/config.py
...

CHANNEL_LAYERS = {
   'default': {
      'BACKEND': 'channels_redis.core.RedisChannelLayer',
      'CONFIG': {
       "hosts": [('127.0.0.1', 6379)],
      },
   },
}

...
```

### Step-4
Add `djnotifier`'s `template` to a common project template e.g. `base.html or core.html`
```html
<!--templates/core.html-->
{% include 'djnotifier/dj_notifier.html' %}
```


## Usage example
Copy example project into your Django project's root, install in your `INSTALLED_APPS`
```python
INSTALLED_APPS = [
     ...
     'djnotifier',
     'example',
 ]
 ```
Add example routes to `project`'s url 
```python
# <project>/urls.py
...
from django.urls import path, include
...

urlpatterns = [
    ...
    path("example/", include('example.urls')),
    ...
]
```

Now run redis-server and django development server -
```shell
# run redis-server
$  redis-server
```
in another terminal/console tab run -
```shell
# run django dev server
$ python manage.py runserver
```

Now open 2 tabs - 
1. Un-authenticated user page: http://localhost:8000/example/
2. Authenticated user page: http://localhost:8000/example/auth/

Now in another tab if you open http://localhost:8000/example/notify/
then you'll see two different notification.
