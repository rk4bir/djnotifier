# djnotifier/config.py
from django.conf import settings
from django.utils.module_loading import import_string


class Config:
    """Application configs"""

    def __init__(self):
        self.debug = self._debug
        self.consumer = self._consumer
        self.extra_routes = self._extra_routes

    @property
    def _debug(self):
        """
        Fetch debug variable from project settings or set default as False
        and return it
        """
        _debug = hasattr(settings, 'DJ_NOTIFIER_CONFIG_INFO_SHOW')
        if _debug:
            _debug = settings.DJ_NOTIFIER_CONFIG_INFO_SHOW
        return _debug

    @property
    def _consumer(self):
        """
        Fetch consumer class from project settings or set default class
        and return it
        """
        try:
            return import_string(settings.DJ_NOTIFIER_CONSUMER)
        except Exception as err:
            if self._debug:
                print(f"djnotifier->config->loading consumer setting: {err}")
            from .consumers import DJNotifierConsumer
            return DJNotifierConsumer

    @property
    def _extra_routes(self):
        """
        Fetch extra_routes from project settings or set default as [] i.e.
        empty list and return it
        """
        try:
            return import_string(settings.DJ_NOTIFIER_EXTRA_ROUTES)
        except Exception as err:
            if self._debug:
                print(f"djnotifier->config->loading extra_routes setting: {err}")
            return []


config = Config()
