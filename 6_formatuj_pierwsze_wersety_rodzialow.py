import sys
from pathlib import Path
import logging
from utils.processing_coordinator import ProcessingCoordinator

logger = logging.getLogger(__name__)

def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    global logger
    logger = logging.getLogger(__name__)

    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
        if not filepath.exists():
            logger.error('Plik %s nie istnieje.', filepath)
            return
    else:
        try:
            filepath = next(Path('.').glob('part0000.html'))
        except StopIteration:
            logger.error("Nie znaleziono pliku 'part0000.html'.")
            return

    bible_text = Path(filepath).read_text(encoding='utf-8').splitlines(keepends=True)
    processing_coordinator = ProcessingCoordinator(bible_text)
    processing_coordinator.process_all()
    processing_coordinator.save_back(Path(filepath))

if __name__ == '__main__':
    main()
