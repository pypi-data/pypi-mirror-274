import requests
from datetime import datetime, timezone
from typing import Optional, Any

DEFAULT_SERVER = 'https://terobot.lobelia.earth'

# ====================================
# Declarations
# ====================================
class BotOptions:
    def __init__(self, server: Optional[str] = None, appInstance: Optional[str] = None,
                 appDescription: Optional[str] = None, isTest: Optional[bool] = None,
                 disabled: Optional[bool] = None):
        self.server = server or DEFAULT_SERVER
        self.appInstance = appInstance or 'App'
        self.appDescription = appDescription
        self.isTest = isTest
        self.disabled = disabled

class KpiOptions:
    def __init__(self, message: Optional[str] = None, details: Optional[Any] = None,
                 timestamp: Optional[datetime] = None, logger: Optional[Any] = None):
        self.message = message
        self.details = details
        self.timestamp = timestamp
        self.logger = logger

class ErrorOptions:
    def __init__(self, details: Optional[Any] = None, timestamp: Optional[datetime] = None,
                 logger: Optional[Any] = None, err: Optional[Exception] = None):
        self.details = details
        self.timestamp = timestamp
        self.logger = logger
        self.err = err

class BotError(Exception):
    def __init__(self, key: str, message: str, options: Optional[ErrorOptions] = None):
        super().__init__(message)
        self.key = key
        self.details = options.details if options else None
        self.timestamp = options.timestamp if options else None
        self.logger = options.logger if options else None

        if options and options.err:
            self.__traceback__ = options.err.__traceback__
            self.__cause__ = options.err

class TeroBot:
    def __init__(self, userOptions: Optional[BotOptions] = None):
        options = userOptions or BotOptions()
        self.server = options.server
        self.appInstance = options.appInstance
        self.appDescription = options.appDescription
        self.isTest = options.isTest
        self.disabled = options.disabled
        self.api = requests.Session()
        self.api.base_url = self.server
        self.breadcrumbs = []
        self._loggedDisabled = False

    def logDisabled(self):
        if self._loggedDisabled:
            return
        self._loggedDisabled = True
        print('WARNING: bot is currently disabled')

    def clearBreadcrumbs(self):
        self.breadcrumbs = []

    def sendKpi(self, key: str, value: Any, options: Optional[KpiOptions] = None):
        if self.disabled:
            self.logDisabled()
            return
        try:
            options = options or KpiOptions()
            timestamp = (options.timestamp or datetime.utcnow()).isoformat()
            datum = {
                'key': key,
                'appInstance': self.appInstance,
                'appDescription': self.appDescription,
                'timestamp': timestamp,
                'type': 'kpi',
                'value': value,
                'message': options.message,
                'details': options.details,
                'isTest': self.isTest,
            }
            self.api.post(f'{self.server}/api/datum', json=datum)
        except Exception as err:
            if options and options.logger:
                options.logger.error('tero-bot', 'Error sending KPI to TeroBot', {'attach': err})
            else:
                print(f'{datetime.now(timezone.utc).isoformat()} Error sending KPI to TeroBot: {str(err)}')

    def sendException(self, error: BotError):
        if self.disabled:
            self.logDisabled()
            return
        try:
            timestamp = (error.timestamp or datetime.now(timezone.utc)).isoformat()
            datum = {
                'key': error.key,
                'appInstance': self.appInstance,
                'appDescription': self.appDescription,
                'timestamp': timestamp,
                'type': 'exception',
                'value': str(error),
                'details': error.details,
                'exceptionStack': str(error.__traceback__),
                'exceptionBreadcrumbs': self.breadcrumbs,
                'isTest': self.isTest,
            }
            self.api.post(f'{self.server}/api/datum', json=datum)
        except Exception as err:
            if error.logger:
                error.logger.error('tero-bot', 'Error sending exception to TeroBot', {'attach': err})
            else:
                print(f'{datetime.utcnow().isoformat()} Error sending exception to TeroBot: {str(err)}')