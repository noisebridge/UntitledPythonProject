# Main entry point to run the recommendation pipeline

from data_processing.wiki_to_netflix import * 

import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    test = len(sys.argv) < 2 or sys.argv[1] != '--prod'
    logging.basicConfig(filename='program_log.log', level=logging.INFO)
    logger.info('Program running starts')
    data = process_data(test = test)
    logger.info('Program successfully processes Netflix data')
    insert_into_mongo(data)
    logger.info('Program successfully stores data')
