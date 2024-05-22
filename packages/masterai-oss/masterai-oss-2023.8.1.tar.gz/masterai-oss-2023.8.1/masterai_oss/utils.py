import tenacity
import logging
import traceback

logger = logging.getLogger(__name__)


def retry_log(retry_state: tenacity.RetryCallState):
    fn: str = retry_state.fn.__name__
    attempt_number: int = retry_state.attempt_number
    args: tuple = retry_state.args
    kwargs: dict = retry_state.kwargs
    msg = f"[*] retry log: call func: {fn} for {attempt_number} time with args: {args} kwargs: {kwargs}"
    if retry_state.outcome:
        retry_exception = retry_state.outcome.exception()
        retry_exception_traceback = ''.join(traceback.format_exception(retry_exception))
        msg += f"\ncause by --> \n{retry_exception_traceback}"
    logger.warning(msg)


if __name__ == '__main__':
    @tenacity.retry(
        # retry=tenacity.retry_if_exception_type(Exception),
        stop=tenacity.stop_after_attempt(3),
        after=retry_log,
        reraise=True
    )
    def httpbin(a, b, c):
        raise Exception('cc')

    httpbin(1, 2, 3)
