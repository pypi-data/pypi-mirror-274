from datetime import datetime
from typing import Optional

class Logger:
    COLORS = {
        "RESET": "\033[0m",
        "BLACK": "\033[30m", 
        "WHITE": "\033[37m",   
        "GRAY": "\033[90m",       
        "MAGENTA": "\033[35m",   
        "RED": "\033[31m",        
        "GREEN": "\033[32m",      
        "YELLOW": "\033[33m",     
        "LBLUE": "\033[94m",
        "CYAN": "\033[36m", 
        "PINK": "\033[95m",
        "LRED": "\033[91m"
    }

    def __init__(self):
        pass

    def c_time(self) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def format_message(self, level_color, level, message, start: Optional[float] = None, end: Optional[float] = None):
        time_now = f"{self.COLORS['GRAY']}[{self.c_time()}]{self.COLORS['RESET']}"
        level_str = f"{level_color}[{level}]"
        duration = f" {self.COLORS['MAGENTA']}({end - start:.2f} seconds){self.COLORS['RESET']}" if start and end else ""
        return f"{time_now} {level_str} - {message}{duration}"

    def debug(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['LBLUE'], "DEBUG", message, start, end))

    def info(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['CYAN'], "INFO", message, start, end))

    def warning(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['YELLOW'], "WARNING", message, start, end))

    def error(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['RED'], "ERROR", message, start, end))

    def success(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['GREEN'], "SUCCESS", message, start, end))

    def ratelimit(self, message, start: Optional[float] = None, end: Optional[float] = None):
        print(self.format_message(self.COLORS['LRED'], "RATELIMIT", message, start, end))