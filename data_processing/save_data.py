# This script handles saving the interaction matrix
import pickle

def save_matrix(matrix, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump(matrix, f)
    print(f"Interaction matrix saved to {output_file}")
