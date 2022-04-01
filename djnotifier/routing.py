# djnotifier/routing.py
from django.urls import path

from .config import config

websocket_urlpatterns = [
    # ws://<host_name or ip_address>/djnotifier/
    path('djnotifier/', config.consumer.as_asgi()),
]

if len(config.extra_routes) > 0:
    websocket_urlpatterns += config.extra_routes


# print djnotifier configs
if config.debug:
    print("\n", '=' * 22, "")
    print("|  djnotifier configs  |")
    print(" " + '=' * 22)
    print("Debug:", config.debug)
    print("Consumer:", config.consumer)
    print("Extra routes:", config.extra_routes)
    print("Routes:", websocket_urlpatterns, end='\n\n')
