import logging
from threading import Lock

class Logger:
    # Class-level attributes to store the singleton instance and a lock to ensure thread-safe instantiation
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Override the creation of a new instance to ensure only one instance of Logger exists (singleton)."""
        with cls._lock:
            if cls._instance is None:
                # If no instance exists, create one and setup the logger configuration
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance.setup_logger()
            return cls._instance

    def setup_logger(self):
        """Sets up a custom logger with a specific format and DEBUG level."""
        self._logger = logging.getLogger('flexidata')  # Create a logger object for 'flexidata'
        self._logger.setLevel(logging.DEBUG)  # Set the default log level to DEBUG

        # Create a stream handler to output logs to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Define the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set the defined formatter to the console handler
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)  # Add the console handler to the logger

    def debug(self, message):
        """Log a DEBUG level message."""
        self._logger.debug(message)

    def info(self, message):
        """Log an INFO level message."""
        self._logger.info(message)

    def warning(self, message):
        """Log a WARNING level message."""
        self._logger.warning(message)

    def error(self, message):
        """Log an ERROR level message."""
        self._logger.error(message)
