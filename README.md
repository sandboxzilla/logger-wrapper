# LoggingHelper Package

This package provides a wrapper for the built-in logger:

> *LoggingHelper:* A class for creating and managing events with callback routines.
>     This class can be used independently of TimerEvent for handling general event-driven scenarios without any time-based requirements.

## **LoggingHelper:**

The LoggingHelper class wraps the logger package to pre-configure some of the common tasks like formating.

The LoggingHelper class has the following methods::

>  *get_output_path(handler_type: logging.Handler=None):* Tries to retrieve a list of output targets of the handler that matches the type passed in.  If handler_type is None, all the output targets for all the registered handlers are returned.
>
>  *remove_handler(handler_type: logging.Handler=None):* Removes the handlers that matches the type passed in. If the handler_type is None or the handler_type is not registered,none of the handlers will be removed.  If an abstract handler is given, all handler that have inherited will be removed.
>
>  *version():* The package version.

## Example Usage::

```python
import logging
from logging import handlers as hdls

if __name__ == "__main__":
    name = None
    handlers = [logging.StreamHandler(), hdls.SysLogHandler(address='/dev/log')]
    logger = LoggingHelper(name=name,
                        level=logging.DEBUG,
                        date_filename=True,
                        meta=True,
                        handlers=handlers)

    print("version: " + logger.version)

    for count in range(10):
        if count == 5:
            logger.remove_handler(logging.StreamHandler)
        logger.info("test of " + str(count))


```
