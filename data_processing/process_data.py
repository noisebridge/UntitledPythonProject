# This script handles the processing and creation of the interaction matrix

import numpy as np
import os

def create_interaction_matrix(directory_path, num_users, num_movies, files):
    interaction_matrix = np.zeros((num_users, num_movies), dtype=np.int8)
    user_mapper = {}
    current_user_index = 0
    
    for filename in files:
        with open(os.path.join(directory_path, filename), 'r') as file:
            movie_id = int(file.readline().strip().replace(':', ''))
            movie_idx = movie_id - 1
            
            for line in file:
                user_id, rating, _ = line.strip().split(',')
                user_id = int(user_id)
                rating = int(rating)
                
                if rating < 4:
                    continue
                else:
                    if user_id not in user_mapper:
                        user_mapper[user_id] = current_user_index
                        current_user_index += 1
                    user_idx = user_mapper[user_id]
                    interaction_matrix[user_idx, movie_idx] = rating

    return interaction_matrix
