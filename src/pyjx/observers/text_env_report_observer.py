from .base_report_observer import BaseReportObserver

class TextEnvReportObserver(BaseReportObserver):
    def __init__(self, path: str) -> None:
        self.__path = path

    def update(self, issue, message, timestamp):
        with open(self.__path, mode="a", encoding="utf-8") as reporter:
            content = timestamp + " " + message + " " + repr(issue)
            reporter.write(content)
