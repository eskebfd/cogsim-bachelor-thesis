import logging
import time
from contextlib import contextmanager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger("cogsim.workflow")


@contextmanager
def log_duration(label: str, **details):
    start = time.perf_counter()
    logger.info("START %s %s", label, details)

    try:
        yield
    except Exception:
        duration = time.perf_counter() - start
        logger.exception("ERROR %s after %.2fs %s", label, duration, details)
        raise
    else:
        duration = time.perf_counter() - start
        logger.info("END %s %.2fs %s", label, duration, details)
