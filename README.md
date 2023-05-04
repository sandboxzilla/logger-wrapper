# LoggerWrapper Package

This package provides wrappers for the built-in logging.Logger class:

## **PseudoSingletonLogger::**

The PseudoSingletonLogger class inherits the logging.Logger and instantiates a singleton for each logger name give.</br>
PsudoSigletonLogger pre-configures some of the common tasks like formating to help a standardize logging format.</br>
If given the optional 'app_name' the name of the application is placed in the header.</br>
If given the 'use_instance' flag a space is allocated for the instance name for the client class to inject during logging.</br>
If given the optional 'name' string the name is used to find the logger by that name, otherwise the 'root' logger is used.</br>
Each unique 'name' creates a new instance.  Setting the name equal to None will use the previously used instance.  Using a previously used name will return that instance.</br>

The PsudoSigletonLogger class has the following methods::

>   *set_default_format(logger_name: str = None, app_name: str = None, use_instance: bool = False):* </br>
>   Sets the default logging format for the given logger_name.  If no logger_name than the default is the last_logger instance used.

>   *get_output_path(logger_name: str = None, handler_type: logging.Handler=None):*</br>
>   Tries to retrieve a list of output targets of the handler that matches the type passed in. If handler_type is None, all the output targets for all the registered handlers are returned.</br>
>   If no logger_name provided than the default is the last_logger instance used.</br>
>
>   *NOTE:* Not fully tested for all handler types.  Tested on StreamHandler, FileHandler, and SyslogHandler</br>

>   *remove_handler(logger_name: str = None, handler_type: logging.Handler=None):*</br>
>   Removes the handlers that matches the type passed in. If the handler_type is None or the handler_type is not registered, none of the handlers will be removed.  If an abstract handler is given, all handler that have inherited will be removed.</br>
>   If no logger_name provided than the default is the last_logger instance used.</br>

>   *version:*</br>
>   The package version.


## **LoggerWrapper::**

The LoggerWrapper class wraps the logging.Logger to pre-configure some of the common tasks like formating.  Provides a quick access to logging by formating the messages to help stardardize the log entries.  This class injects the instance name into the log messages.</br>
If given the optional 'instance_name' string the given name is used, otherwise the instance name is extracted from the stack.  The instance name is inject into the header during logging.</br>
If given the optional 'name' string the name is used to find the logger by that name, otherwise the 'root' logger is used.</br>

The LoggerWrapper class has the following methods::

>   *change_instance_name(self, instance_name: str):*</br>
>   Changes the instance name to use in the log message header.

>   *_log(level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel: int=1):*</br>
>   Overwrites the logging.Logger._log method to inject the instance name in the log message header.</br>

LoggerWrapper also exposes the PseudoSingletonLogger methods as its own.</br>

## Example Usage ::

```python
import logging
from logging import handlers as hdls
from pathlib import Path

if __name__ == "__main__":
    log_path = Path(".logs", "test.log")
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(),
                logging.FileHandler(log_path)]
    log1 = LoggerWrapper(app_name="LoggerWrapper Demo",
                         handlers=handlers,
                         meta=True,
                         date_filename=False)

    log2 = LoggerWrapper()
    print(log2.version)

    print(str(log1.get_output_path()))

    for count in range(10):
        if count == 5:
            log1.remove_handler(logging.StreamHandler)
        log1.info("test of " + str(count))
        log2.info("test of " + str(count))

    print(str(log2.get_output_path()))
    print(log1.version)
```

### Console ::

>0.1.0</br>
>['<stderr>', '/home/erol/workspace/logger-wrapper/.logs/test.log']</br>
>2023-05-03 23:15:41,123,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 0</br>
>2023-05-03 23:15:44,484,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 0</br>
>2023-05-03 23:15:48,254,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 1</br>
>2023-05-03 23:15:49,052,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 1</br>
>2023-05-03 23:15:51,307,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 2</br>
>2023-05-03 23:15:51,904,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 2</br>
>2023-05-03 23:15:53,822,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 3</br>
>2023-05-03 23:15:54,505,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 3</br>
>2023-05-03 23:15:56,481,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 4</br>
>2023-05-03 23:15:57,099,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 4</br>
>['/home/erol/workspace/logger-wrapper/.logs/test.log']</br>
>0.1.0</br>

### cat ~/workspace/logger-wrapper/.logs/test.log ::

>2023-05-03 23:15:41,123,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 0</br>
>2023-05-03 23:15:44,484,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 0</br>
>2023-05-03 23:15:48,254,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 1</br>
>2023-05-03 23:15:49,052,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 1</br>
>2023-05-03 23:15:51,307,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 2</br>
>2023-05-03 23:15:51,904,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 2</br>
>2023-05-03 23:15:53,822,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 3</br>
>2023-05-03 23:15:54,505,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 3</br>
>2023-05-03 23:15:56,481,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 4</br>
>2023-05-03 23:15:57,099,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 4</br>
>2023-05-03 23:16:01,619,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 5</br>
>2023-05-03 23:16:02,369,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 5</br>
>2023-05-03 23:16:04,266,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 6</br>
>2023-05-03 23:16:04,763,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 6</br>
>2023-05-03 23:16:06,621,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 7</br>
>2023-05-03 23:16:07,148,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 7</br>
>2023-05-03 23:16:09,007,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 8</br>
>2023-05-03 23:16:09,595,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 8</br>
>2023-05-03 23:16:12,300,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log1:logger_wrapper:<module>:408],test of 9</br>
>2023-05-03 23:16:12,301,LoggerWrapper Demo,[INFO:pid=3356970:MainThread:log2:logger_wrapper:<module>:409],test of 9
