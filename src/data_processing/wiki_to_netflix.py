import requests
import csv
import os
import math

base_dir = os.path.join(os.path.dirname(__file__), '../data/')
user_agent = 'Noisebridge MovieBot 0.0.1/Audiodude <audiodude@gmail.com>'

# Reading netflix text file
def read_netflix_txt(txt_file, test):
    netflix_list = []

    num_rows = None
    if test == True:
        num_rows = 100

    with open(txt_file, "r", encoding = "ISO-8859-1") as netflix_data:
        for i, line in enumerate(netflix_data):
            if num_rows is not None and i >= num_rows:
                break
            netflix_list.append(line.rstrip().split(',', 2))

    return netflix_list

# Writing netflix csv file
def create_netflix_csv(csv_name, data_list):   
    with open(csv_name, 'w') as netflix_csv:
        csv.writer(netflix_csv).writerows(data_list)

# Extracting movie info from Wiki data
def wiki_feature_info(data, key):
    if len(data['results']['bindings']) < 1 or key not in data['results']['bindings'][0]:
        return 'NULL'
    if key == 'genreLabel':
        return list({d['genreLabel']['value'] for d in data['results']['bindings'] if 'genreLabel' in d})
    return data['results']['bindings'][0][key]['value'].split('/')[-1] 

# Formatting SPARQL query for Wiki data
def format_sparql_query(title, year):
    QUERY = '''
        SELECT * WHERE {
            SERVICE wikibase:mwapi {
                bd:serviceParam wikibase:api "EntitySearch" ;
                                wikibase:endpoint "www.wikidata.org" ;
                                mwapi:search "%(Title)s" ;
                                mwapi:language "en" .
                ?item wikibase:apiOutputItem mwapi:item .
            }

            ?item wdt:P31/wdt:P279* wd:Q11424 .
            
            {
                # Get US release date
                ?item p:P577 ?releaseDateStatement .
                ?releaseDateStatement ps:P577 ?releaseDate .
                ?releaseDateStatement pq:P291 wd:Q30 .  
            }
            UNION
            {
                # Get unspecified release date
                ?item p:P577 ?releaseDateStatement .
                ?releaseDateStatement ps:P577 ?releaseDate .
                FILTER NOT EXISTS { ?releaseDateStatement pq:P291 ?country }
            }
        
            FILTER (YEAR(?releaseDate) = %(Year)d) .

            ?item rdfs:label ?itemLabel .
            FILTER (lang(?itemLabel) = "en") .

            OPTIONAL {
                ?item wdt:P136 ?genre .
                ?genre rdfs:label ?genreLabel .
                FILTER (lang(?genreLabel) = "en") .
            }

            OPTIONAL {?item wdt:P57 ?director.
                            ?director rdfs:label ?directorLabel.
                            FILTER (lang(?directorLabel) = "en")}

            SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
            }
    
        '''
    return QUERY % {'Title': title, 'Year': year}

# Getting list of movie IDs, genre IDs, and director IDs from request
def wiki_query(data_csv, user_agent):
    wiki_movie_ids = []
    wiki_genres = []
    wiki_directors = []
        
    for row in data_csv:
        if row[1] == "NULL":
            continue

        SPARQL = format_sparql_query(row[2], int(row[1]))

        response = requests.post('https://query.wikidata.org/sparql',
                    headers={'User-Agent': user_agent},
                    data={
                    'query': SPARQL,
                    'format': 'json',
                    }
        )
        response.raise_for_status() 
        
        data = response.json()
        
        wiki_movie_ids.append(wiki_feature_info(data, 'item'))
        wiki_genres.append(wiki_feature_info(data, 'genreLabel'))
        wiki_directors.append(wiki_feature_info(data, 'directorLabel'))
    
    return wiki_movie_ids, wiki_genres, wiki_directors

# Calling all functions
def process_data(test=False):
    missing_count = 0
    processed_data = []

    netflix_file = read_netflix_txt(os.path.join(base_dir, 'movie_titles.txt'), test)
    num_rows = len(netflix_file)

    netflix_csv = os.path.join(base_dir, 'movie_data.csv')

    wiki_movie_ids_list, wiki_genres_list, wiki_directors_list = wiki_query(netflix_file, user_agent)

    for index, row in enumerate(netflix_file):
        netflix_id, year, title = row
        if wiki_movie_ids_list[index] == 'NULL':
            missing_count += 1
        processed_data.append([netflix_id, wiki_movie_ids_list[index], title, year, wiki_genres_list[index], wiki_directors_list[index]])

    create_netflix_csv(netflix_csv, processed_data)

    print(f'missing:  {missing_count} ({missing_count / num_rows * 100}%)')
    print(f'found: {num_rows - missing_count} ({num_rows - missing_count) / num_rows * 100}%)')
    print(f'total: {num_rows}')

if __name__ == '__main__':
    process_data(True)
