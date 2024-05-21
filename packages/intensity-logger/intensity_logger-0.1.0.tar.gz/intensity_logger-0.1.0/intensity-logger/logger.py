from datetime import datetime
from typing import Optional

class Logger:
    COLORS = {
        "WHITE": "\u001b[37m",
        "MAGENTA": "\033[38;5;97m",
        "MAGENTAA": "\033[38;2;157;38;255m",
        "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;40m",
        "YELLOW": "\033[38;5;220m",
        "BLUE": "\033[38;5;21m",
        "PINK": "\033[38;5;176m",
        "CYAN": "\033[96m",
        "RESET": "\033[0m"
    }

    def __init__(self, application_name: Optional[str] = None):
        self.application_name = application_name

    @staticmethod
    def get_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def format_message(self, level_color: str, level: str, message: str, start: Optional[int] = None, end: Optional[int] = None) -> str:
        time_stamp = f"{self.COLORS['MAGENTA']}{self.get_time()}{self.COLORS['RESET']}"
        app_context = f"{self.COLORS['PINK']}{self.application_name if self.application_name else ''}{self.COLORS['RESET']}"
        level_label = f"{level_color}{level}{self.COLORS['RESET']}"
        base_message = f"{f'[{app_context}] ' if self.application_name else ''}[{time_stamp}] | [{level_label}] ->"

        if start is not None and end is not None:
            duration = f" Duration: {self.COLORS['MAGENTAA']}{str(end - start)[:5]} sec{self.COLORS['RESET']}"
            message += duration

        return f"{base_message} {self.COLORS['WHITE']}{message}{self.COLORS['RESET']}"
    
    def log(self, level_color: str, level: str, message: str, start: Optional[int] = None, end: Optional[int] = None) -> None:
        print(self.format_message(level_color, level, message, start, end))
    
    def success(self, message: str, start: Optional[int] = None, end: Optional[int] = None) -> None:
        self.log(self.COLORS['GREEN'], "Success", message, start, end)

    def info(self, message: str, start: Optional[int] = None, end: Optional[int] = None) -> None:
        self.log(self.COLORS['BLUE'], "Info", message, start, end)

    def failure(self, message: str, start: Optional[int] = None, end: Optional[int] = None) -> None:
        self.log(self.COLORS['RED'], "Failure", message, start, end)

    def ratelimit(self, message: str, start: Optional[int] = None, end: Optional[int] = None) -> None:
        self.log(self.COLORS['CYAN'], "Ratelimit", message, start, end)