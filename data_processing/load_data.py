# This script handles loading the movie titles and ratings data
import os

# def load_movie_titles(filepath):
#     movie_data = []
#     with open(filepath, 'r', encoding='ISO-8859-1') as file:
#         for line in file:
#             movie_id, year, title = line.strip().split(",", 2)
#             movie_data.append([int(movie_id), int(year), title])
#     return movie_data        (This function is not being called in the main.py file. It is not needed for the current implementation.)

def list_rating_files(directory_path):
    return sorted([f for f in os.listdir(directory_path) if f.startswith('mv_')]) # List of files starting with 'mv_'
   
