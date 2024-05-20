# kbitools
Rarely-changing tools for use throughout the python KerBI application suite.

## KERBI CLIENT (klient.py)

The KerBI client can connect and send messages to a running KBI instance.
It accepts various arguments like connecting to the server and setting the channel and workflow. 
You can also use slash commands to direct a message to a certain workflow or change channels.

## USING THE LOGGER IN YOUR OWN CODE

Import the logger with:

`from kbitools import setup_logger`

And set it up with defaults in your code with:
```bash
logger = setup_logger(__name__, log_file='/path/to/writeable/file')
```

If you're reading in the log level and configuration using a string configuration (like with a configuration file or JSON object), do this:
```bash
log_file = configuration['log_file']
log_level_name = configuration['console_log_level'].upper()
log_level = getattr(logging, log_level_name, None)
if log_level is None:
    raise ValueError(f'Invalid log level for console log output: {log_level_name}'
logger = setup_logger(__name__, log_file=log_file, console_level=log_level)
```

And then you simply call it instead of a print statement. By default, will write out everything at and above DEBUG level (so only the TRACE level is below, which I use to record every function call). Will print INFO and above to console by default.

`logger.info("Lorum ipsum decor")`

`2024-04-30 14:57:57,987 - module_name - say_lorum - INFO - Lorum ipsum decor`
