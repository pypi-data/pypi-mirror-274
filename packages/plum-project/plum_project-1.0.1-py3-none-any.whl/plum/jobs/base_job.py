import logging
from abc import ABCMeta, abstractmethod
from typing import Optional

import plum.jobs.utils.execution.recorder as ER

class BaseJob(metaclass = ABCMeta):
    """Base class for customizable job object"""
    def __init__(
        self,
        name: str,
        logger: logging.Logger
    ):
        self._logger: logging.Logger = logger
        self.name: str = name
        self._exec_rec = ER.ExecutionRecorder(job_id = name)
    
    @abstractmethod
    def _process(self) -> Optional[Exception]:
        """Custom execution code goes here"""
        pass
    
    def execute(self):
        """
        Executes pre and post operations and triggers the `self._process` method.
        """
        
        # Collect the starting timestamp for the execution recorder
        start_timestamp_reset_err: Optional[ER.StartTimestampResetError] = self._exec_rec.set_start_timestamp()
        if start_timestamp_reset_err != None:
            self._logger.error(
                f'failed to record start timestamp for job execution; {start_timestamp_reset_err.__str__}'
            )

        # Run the developer specificed code within the overwritten _process method
        process_err: Exception = self._process()

        # Collect the ending timestamp for the execution recorder
        end_timestamp_err: Optional[ER.ExecutionRecorderTimeError] = self._exec_rec.set_end_timestamp()
        if end_timestamp_err != None:
            self._logger.error(f'failed to record end timestamp for job execution; {end_timestamp_err}')

        # Handle raised errors in the developer spcified code
        if process_err != None:
            self._logger.error(f'failed to complete the execution of the job "{self.name}"; {process_err.args}')

        exec_time, exec_time_err = self._exec_rec.get_execution_time()
        if exec_time_err != None:
            self._logger.error(exec_time_err.__str__())
        self._logger.info(f'EXECUTION_TIME [{exec_time}]')