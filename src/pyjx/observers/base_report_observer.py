from abc import ABC, abstractmethod

class BaseReportObserver(ABC):
    @abstractmethod
    def update(self, issue, message, timestamp):
        pass
