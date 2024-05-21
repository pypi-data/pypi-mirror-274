import time
from http import HTTPStatus
from typing import Iterator, List, Optional

from requests.exceptions import ConnectionError

from fiddler.exceptions import AsyncJobFailed
from fiddler.libs.http_client import RequestClient
from fiddler.schema.job import JobStatus
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import JobResponseHandler

logger = get_logger(__name__)


class JobMixin:
    DEFAULT_POLL_INTERVAL = 3  # In seconds
    DEFAULT_TIMEOUT = 1800  # 30 minutes in seconds

    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_job(self, uuid: str) -> JobResponseHandler:
        """
        Get details about a job

        :params uuid: Unique identifier of the job to get the details of
        :returns: JobResponseHandler object containing details
        """
        # Setting timeout as makeshift approach to handle pod restart
        # leading the ConnectionResetError on client
        timeout = 120
        response = self.client.get(url=f'jobs/{uuid}', timeout=timeout)
        if response.status_code == HTTPStatus.OK:
            return JobResponseHandler(response)
        else:
            # @TODO we should throw error here instead of logging
            logger.info(f'Response status code: {response.status_code}')
            logger.info(response.json())
            raise

    @staticmethod
    def get_task_results(job: JobResponseHandler) -> List[str]:
        results: List[str] = []
        if not job.extras:
            return results
        for task_id, extra_info in job.extras.items():
            if not extra_info['result']:
                continue
            results.append(
                f'JOB UUID: {job.uuid} task id: {task_id} '
                f'result: {extra_info["result"]}'
            )
        return results

    def wait_for_job(
        self,
        uuid: str,
        interval: int = DEFAULT_POLL_INTERVAL,
        timeout: int = DEFAULT_TIMEOUT,
        job_name: Optional[str] = None,
    ) -> Optional[JobResponseHandler]:
        """
        Wait for job to complete either with success or failure status
        :param uuid: Job uuid received on submitting the job
        :param job_name: Name of the job which is used for logging the progress
        :param interval: Interval in seconds between polling for job status
        :param timeout: Timeout in seconds for iterator to stop.
        :return: Job object of final status if available, otherwise None
        """
        job = None

        log_prefix = job_name or f'JOB UUID: {uuid}'
        for job in self.watch_job(uuid=uuid, interval=interval, timeout=timeout):
            logger.info(
                '%s: status - %s, progress - %.2f%%',
                log_prefix,
                job.status,
                job.progress,
            )

            if job.status == JobStatus.SUCCESS:
                logger.info('%s: successfully completed', log_prefix)
            elif job.status == JobStatus.FAILURE:
                raise AsyncJobFailed(
                    f'{log_prefix} failed with {job.error_reason or "Exception"}: '
                    f'{job.error_message}'
                )

        return job

    def watch_job(
        self,
        uuid: str,
        interval: int = DEFAULT_POLL_INTERVAL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Iterator[JobResponseHandler]:
        """
        Watch job status at given interval and yield job object
        :param uuid: Job uuid received on submitting the job
        :param interval: Interval in seconds between polling for job status
        :param timeout: Timeout in seconds for iterator to stop.
        :return: Iterator of job object
        """
        start_time = time.time()
        while True:
            try:
                job = self.get_job(uuid)
            except ConnectionError:
                logger.exception(
                    'Failed to connect to the server. Retrying...\n'
                    'If this error persists, please reach out to Fiddler.'
                )
                continue

            yield job

            current_time = time.time()
            if (current_time - start_time) > timeout:
                raise TimeoutError(f'Timed out while watching job {uuid}')

            if job.status in [JobStatus.SUCCESS, JobStatus.FAILURE, JobStatus.REVOKED]:
                return

            time.sleep(interval)
