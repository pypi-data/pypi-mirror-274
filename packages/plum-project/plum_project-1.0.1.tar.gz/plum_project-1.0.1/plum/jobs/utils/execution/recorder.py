from typing import Tuple, Optional
from datetime import datetime, timedelta

class ExecutionRecorderTimeError(Exception):
    def __init__(self, msg: str):
        super().__init__(
            f"an issue around execution time tracking took place in ExecutionRecorder; {msg}"
        )

class ExecutionTimeError(ExecutionRecorderTimeError):
    '''
    Raised when the `self.start_timestamp` or `self._end_timestamp` is `None` during a request for execution time.
    '''
    def __init__(self):
        super().__init__("execution record was incomplete when it comes to a start/end timestamp")

class StartTimestampResetError(ExecutionRecorderTimeError):
    '''
    Raised when the `self.start_timestamp` as already been set on the ExecutionRecorder.
    '''
    def __init__(self):
        super().__init__("set_start_timestamp method has already been executed in this instance")

class EndTimestampResetError(ExecutionRecorderTimeError):
    '''
    Raised when the `self.end_timestamp` as already been set on the ExecutionRecorder.
    '''
    def __init__(self):
        super().__init__("set_end_timestamp method has already been executed in this instance")

class PrematureEndTimestampError(ExecutionRecorderTimeError):
    '''
    Raised when the `self.start_timestamp=None` when the self.end_timestamp is attempted to be set.
    '''
    def __init__(self):
        super().__init__("failed to set end timestamp because start timestamp was found to be None")

class ExecutionRecorder:

    def __init__(self, job_id: str):
        self.job_id: str = job_id
        self.start_timestamp: Optional[datetime] = None
        self.end_timestamp: Optional[datetime] = None
    
    def _get_current_timestamp_utc(self) -> datetime:
        return datetime.utcnow()

    def set_start_timestamp(self) -> Optional[StartTimestampResetError]:
        if self.start_timestamp != None:
            return StartTimestampResetError()
        self.start_timestamp: datetime = self._get_current_timestamp_utc()
        return None
    
    def set_end_timestamp(self) -> Optional[ExecutionRecorderTimeError]:
        if self.start_timestamp == None:
            return PrematureEndTimestampError()
        if self.end_timestamp != None:
            return EndTimestampResetError()
        self.end_timestamp: datetime = self._get_current_timestamp_utc()
        return None

    def get_execution_time(self) -> Tuple[timedelta, ExecutionTimeError]:
        if self.start_timestamp == None or self.end_timestamp == None:
            return (None, ExecutionTimeError())
        result = self.end_timestamp - self.start_timestamp
        return (result, None)