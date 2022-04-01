# djnotifier
>**djnotifier** is a Django app to conduct web-based real time notification. Almost fully customizable app + plugin.


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
Default config `djnotifier`
```python
# You may replace this consumer as needed and 
# point the consumer class
DJ_NOTIFIER_CONSUMER = 'djnotifier.consumers.DJNotifierConsumer'

# If you want to register more websocket routes
# you may point to the routes list variable as - 
DJ_NOTIFIER_EXTRA_ROUTES = "<app_label>.routing.extra_routes"

# When you're developing you may want to 
# turn it on by putting `True` to see
# `djnotifier` logs
DJ_NOTIFIER_CONFIG_INFO_SHOW = False
```
Consumer class `djnotifier.consumers.DJNotifierConsumer`
```python
# djnotifier/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DJNotifierConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:
        user = self.scope["user"]
        group = "dj_notifier_anonymous"
        if not user.is_anonymous:
            group = f"dj_notifier_{user.pk}"

        self.group_name = group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.groups.append(self.group_name)
        await self.accept()

    async def disconnect(self, close_code) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.groups.remove(self.group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None) -> None:
        pass

    async def dj_notifier(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
```

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


# Customization
