from ..textUtils import textUtils

class Logger:
    def __init__(self, prefix = None, debug=False, log = None, format = "{event} {white}| {message}"):
        self.prefix = prefix
        self.log = log
        self.format = format
        self.debug = debug
        self.text_utils = textUtils()

    def  __toLogFile(self, message):
        if self.log is not None:
            with open(self.log, "a") as file:
                file.write(message + "\n")

    def __log(self, event, message):
        if self.prefix is not None:
            event = self.prefix + " " + event
        message = self.text_utils.format(message)
        formatted_message = f"{event} {message}"
        print(formatted_message)
        self.__toLogFile(formatted_message)
    
    def info(self, message):
        self.__log("INFO", message)

    def warning(self, message):
        self.__log("WARNING", message)

    def error(self, message):
        self.__log("ERROR", message)

    def success(self, message):
        self.__log("SUCCESS", message)

    def debug(self, message):
        if self.debug:
            self.__log("DEBUG", message)

    def announce(self, message):
        self.__log("ANNOUNCE", message)