import traceback
import logging
from colorama import init, Fore, Back, Style

# Initialize Colorama
init()

class CustomLogger(logging.Logger):
    def error(self, msg, *args, exc_info=None, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'. Automatically add traceback if exception info is available.
        
        Args:
            msg (str): The message to log.
            exc_info (bool/exception type, optional): If not None, exception information will be added to the logging message.
        """
        if exc_info:
            # Manually get traceback details and format them
            if exc_info is True:
                tb = traceback.format_exc()
            else:
                tb = ''.join(traceback.format_exception(*exc_info))
            msg = f"{msg}\nTraceback details:\n{tb}"

        # Call the base class error method with exc_info set to False to prevent it from appending traceback again
        super().error(msg, *args, exc_info=False, stacklevel=2, **kwargs)



logging.setLoggerClass(CustomLogger)  # Ensure our CustomLogger is used


# Create a custom logging level
MESSAGES_LEVEL_NUM = 15
logging.addLevelName(MESSAGES_LEVEL_NUM, "MESSAGES")

def messages(self, message, *args, **kwargs):
    if self.isEnabledFor(MESSAGES_LEVEL_NUM):
        self._log(MESSAGES_LEVEL_NUM, message, args, **kwargs)

logging.Logger.messages = messages

# Create a custom logging level
TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kwargs)

logging.Logger.trace = trace

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to the lowest level

# Define log colors
LOG_COLORS = {
    logging.DEBUG: (Fore.CYAN, None),
    logging.INFO: (Fore.GREEN, None),
    logging.WARNING: (Fore.YELLOW, None),
    logging.ERROR: (Fore.RED, None),
    logging.CRITICAL: (Fore.MAGENTA, None),
    MESSAGES_LEVEL_NUM: (Fore.BLACK, Back.WHITE),
    TRACE_LEVEL_NUM: (Fore.GREEN, Back.WHITE)
}

class ColorLogFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        # Define a default format that includes module and function name
        default_fmt = "%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
        # Initialize the base formatter with the appropriate format
        super().__init__(fmt or default_fmt, datefmt, style)

    def format(self, record):
        fore_color, back_color = LOG_COLORS.get(record.levelno, (Fore.WHITE, None))
        # Apply the foreground and optional background color before returning the formatted string
        record.msg = f"{fore_color}{back_color if back_color else ''}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(name, log_file='kbi.log', console_level=logging.INFO):
    """
    Set up and return a logger with the given name and log file.

    Args:
        name (str): The name of the logger.
        log_file (str): Filename for the log file where logs are also saved.

    Returns:
        logging.Logger: Configured logger with both console and file logging.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Ensure it captures all levels of logs

    # Formatter that includes module and function names
    formatter = ColorLogFormatter()

    # Console handler with a configurable log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # File handler which logs even debug messages
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(5)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

