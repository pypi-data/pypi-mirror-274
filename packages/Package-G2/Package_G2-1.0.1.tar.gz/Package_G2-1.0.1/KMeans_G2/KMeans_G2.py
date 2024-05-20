import pandas as pd
import numpy as np
def kmeans_G2(X, k, num_iterations=10000000):
    
    # Convertir la liste en un tableau numpy
    X = np.array(X)
    iteration = 0
    # Initialisation : choisissez k points aléatoires comme centroïdes
    np.random.seed(45)  # Fixer l'aléa
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]

    for _ in range(num_iterations):
    
        # Assignation des points aux clusters
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        
        labels = np.argmin(distances, axis=1)

        # Mise à jour des centroïdes
        #for i in range(k):
            #centroids[i] = np.mean(X[labels == i], axis=0)
        new_centers = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        
        iteration += 1
        if np.allclose(new_centers, centroids):
            break 
        
        centroids = new_centers
    
    return labels, centroids, iteration
