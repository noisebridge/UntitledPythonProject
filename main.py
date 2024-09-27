# Main entry point to run the recommendation pipeline
from data_processing.load_data import list_rating_files
from data_processing.process_data import create_interaction_matrix
from data_processing.save_data import save_matrix
# from db.mongo_connection import get_db_connection
# from db.movie_storage import insert_movie_data

# Configurations
data_directory = './data/'
movie_titles_file = f'{data_directory}movie_titles.txt'
output_file = f'{data_directory}interaction_matrix.pkl'
mongo_uri = 'mongodb://localhost:27017/'
db_name = 'movie_recommendation'

# Number of users and movies
num_users = 480189  # Example: Replace with actual value
num_movies = 17770  # Example: Replace with actual value

# Step 1: Load Data
movie_data = list_rating_files(movie_titles_file)

# Step 2: Process Data
interaction_matrix = create_interaction_matrix(data_directory, num_users, num_movies, movie_data)

# Step 3: Save Data
save_matrix(interaction_matrix, output_file)

# Step 4: Store Movies in MongoDB
# db = get_db_connection(uri=mongo_uri, db_name=db_name)
# insert_movie_data(db, 'movies', movie_data)
