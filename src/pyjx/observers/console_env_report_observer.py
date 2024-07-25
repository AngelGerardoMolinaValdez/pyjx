from .base_report_observer import BaseReportObserver

class ConsoleEnvReportObserver(BaseReportObserver):
    def update(self, issue, message, timestamp):
        print(timestamp, message)
