_version: str
from .locator.locatorWindows import LocatorWindows as LocatorWindows
from .log.log import getLogger as getLogger, loggers as loggers
from .util.hotkey import hotkeyPause as hotkeyPause, hotkeyPauseHere as hotkeyPauseHere

__all__ = ['_version','LocatorWindows', 'hotkeyPause', 'hotkeyPauseHere', 'loggers', 'getLogger']
