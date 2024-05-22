from datetime import datetime
import importlib


def apply_monkey_patch():
    from crewai.utilities import Logger

    # Subclass Logger to add timestamp functionality
    class LoggerWithTimestamp(Logger):
        def __init__(self, verbose_level=0):
            super().__init__(verbose_level)

        def log(self, level, message, color="bold_green"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_with_timestamp = f"[{timestamp}] {message}"
            super().log(level, message_with_timestamp, color)

    # Monkey patch the Logger class in the original module
    import crewai.utilities
    crewai.utilities.Logger = LoggerWithTimestamp


# Apply the monkey patch before any other imports or code execution
def initialize_patch():
    import crewai
    apply_monkey_patch()
    importlib.reload(crewai)
