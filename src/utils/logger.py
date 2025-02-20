import logging
import sys

def setup_logger():
    logger = logging.getLogger('dart_scorer')
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(handler)
    
    return logger