import logging
import signal
import threading
from time import sleep

from watchdog.observers import Observer

from src.config import parse_arguments, setup_logging
from src.file_watcher import HourlySalesCsvHandler
from src.io.reader import CsvReader
from src.model import SalesStore
from src.parser import HourlySalesCsvParser

stop_event = threading.Event()

def handle_shutdown_signal(signum: int, frame: object) -> None:
    logging.info("Received shutdown signal")
    stop_event.set()


def main() -> None:

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)


    args = parse_arguments()
    watch_dir = args.dir
    watch_dir.mkdir(exist_ok=True)

    log_file = watch_dir / "logs" / args.logfile
    setup_logging(log_file)

    logger = logging.getLogger(__name__)
    logger.info(f"Starting CSV Sales in {watch_dir.resolve()}")
    logger.info(f"Starting login in {log_file.resolve()}")

    store = SalesStore(days = {})
    reader = CsvReader[str]()
    parser = HourlySalesCsvParser(reader, key_name=args.key_name)
    handler = HourlySalesCsvHandler(store=store, parser=parser, watch_path=watch_dir)

    observer = Observer()
    observer.schedule(handler, path=str(watch_dir), recursive=False)
    observer.start()
    logger.info(f"Watching {watch_dir} for Csv files")

    try:
        while not stop_event.is_set():
            sleep(1)
    finally:
        logger.info(f"Stopped observer ...")
        observer.stop()
        observer.join()
        logger.info(f"Shutdown complete")


if __name__ == '__main__':
    main()