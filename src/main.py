# Main entry point to run the recommendation pipeline

from data_processing.wiki_to_netflix import * 

if __name__ == '__main__':
    test = len(sys.argv) < 2 or sys.argv[1] != '--prod'
    data = process_data(test = test)
    insert_into_mongo(data)
