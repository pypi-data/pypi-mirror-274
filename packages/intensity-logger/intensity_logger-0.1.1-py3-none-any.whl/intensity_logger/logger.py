from datetime import datetime

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

    def format_message(self, level_color, level, message):
        time_now = f"{self.COLORS['GRAY']}[{self.c_time()}]{self.COLORS['RESET']}"
        level_str = f"{level_color}[{level}]"
        return f"{time_now} {level_str} - {message}"

    def debug(self, message):
        print(self.format_message(self.COLORS['LBLUE'], "DEBUG", message))

    def info(self, message):
        print(self.format_message(self.COLORS['CYAN'], "INFO", message))

    def warning(self, message):
        print(self.format_message(self.COLORS['YELLOW'], "WARNING", message))

    def error(self, message):
        print(self.format_message(self.COLORS['RED'], "ERROR", message))

    def success(self, message):
        print(self.format_message(self.COLORS['GREEN'], "SUCCESS", message))

    def ratelimit(self, message):
        print(self.format_message(self.COLORS['LRED'], "RATELIMIT", message))