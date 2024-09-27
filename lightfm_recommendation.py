from lightfm import LightFM
from scipy.sparse import coo_matrix
import numpy as np

# Example interaction data
user_ids = [0, 0, 1, 1, 2]
movie_ids = [0, 1, 1, 2, 2]
ratings = [5, 4, 5, 4, 5]  # Only 4s and 5s for this example

# Create sparse interaction matrix
interaction_matrix = coo_matrix((ratings, (user_ids, movie_ids)), shape=(3, 3))

# Initialize LightFM model with WARP loss
model = LightFM(loss='warp')

# Train the model
model.fit(interaction_matrix, epochs=30, num_threads=2)

# Predict scores for User 0
scores = model.predict(0, np.arange(3))
top_items = np.argsort(-scores)
print("Top recommended items for User 0:", top_items)

# Evaluate model
from lightfm.evaluation import precision_at_k, auc_score
precision = precision_at_k(model, interaction_matrix, k=5).mean()
auc = auc_score(model, interaction_matrix).mean()

print(f"Precision at k=5: {precision}, AUC Score: {auc}")
