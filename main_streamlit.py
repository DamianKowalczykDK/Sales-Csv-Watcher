import logging
import signal
import threading
from time import sleep
from datetime import time
from watchdog.observers import Observer

from src.config import parse_arguments, setup_logging
from src.file_watcher import HourlySalesCsvHandler
from src.io.reader import CsvReader
from src.model import SalesStore
from src.parser import HourlySalesCsvParser
from src.report_service import ReportService
from src.service import SalesService
from src.ui_service import UiService

stop_event = threading.Event()

def handle_shutdown_signal(signum: int, frame: object) -> None:
    logging.info("Received shutdown signal")
    stop_event.set()

def main() -> None:

    args = parse_arguments()
    watch_dir = args.dir
    watch_dir.mkdir(exist_ok=True)

    log_file = watch_dir / "logs" / args.logfile
    setup_logging(log_file)

    logger = logging.getLogger(__name__)
    logger.info(f"Starting CSV Sales in {watch_dir.resolve()}")
    logger.info(f"Starting login in {log_file.resolve()}")

    store = SalesStore(days = {})
    reader = CsvReader[time]()
    parser = HourlySalesCsvParser(reader=reader, key_name=args.key_name)
    handler = HourlySalesCsvHandler(store=store, parser=parser, watch_path=watch_dir)
    service = SalesService(handler)
    report_service = ReportService(service)
    ui_service = UiService(report_service)


    observer = Observer()
    observer.schedule(handler, path=str(watch_dir), recursive=False)
    observer.start()
    logger.info(f"Watching {watch_dir} for Csv files")

    try:
        ui_service.show_ui()

    finally:
        logger.info(f"Stopped observer ...")
        observer.stop()
        observer.join()
        logger.info(f"Shutdown complete")

if __name__ == '__main__':
    main()