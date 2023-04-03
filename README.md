# LoggerWrapper Package

This package provides a wrapper for the built-in logging.Logger class:

## **LoggerWrapper:**

The LoggerWrapper class wraps the logging.Logger to pre-configure some of the common tasks like formating.

The LoggerWrapper class has the following methods::

>  *get_output_path(handler_type: logging.Handler=None):* Tries to retrieve a list of output targets of the handler that matches the type passed in.  If handler_type is None, all the output targets for all the registered handlers are returned.\
>       *NOTE:* Not fully tested
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
    handlers = [logging.StreamHandler(),
                logging.FileHandler("test.logs"),
                hdls.SysLogHandler(address='/dev/log'),
                ]
    log = LoggerWrapper(name=name,
                        level=logging.DEBUG,
                        date_filename=True,
                        meta=True,
                        handlers=handlers)

    print("version: " + log.version)
    print(str(log.get_output_path()))

    for count in range(10):
        if count == 5:
            log.remove_handler(logging.StreamHandler)
        log.info("test of " + str(count))
```

### Console::

> version: 0.0.1\
> ['<stderr>', '/home/erol/workspace/logger-wrapper/test_20230403044423.logs', '/dev/log']\
> 2023-04-03 04:44:24,003,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 0\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 1\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 2\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 3\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 4

### cat test_20230403044423.logs::

> 2023-04-03 04:44:24,003,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 0\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 1\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 2\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 3\
> 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 4\
> 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 5\
> 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 6\
> 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 7\
> 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 8\
> 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 9

### cat /var/log/syslog |grep logger_wrapper

> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,003,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 0\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 1\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 2\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 3\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,004,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 4\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 5\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 6\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 7\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 8\
> Apr  3 04:44:24 erol-ub01 2023-04-03 04:44:24,005,[INFO:pid=950586:MainThread:logger_wrapper:<module>:232],test of 9
