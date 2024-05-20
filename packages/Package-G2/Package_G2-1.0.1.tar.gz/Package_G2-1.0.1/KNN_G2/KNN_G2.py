import pandas as pd
import numpy as np

### Algorithme de KNN sans bibliotèque externe

class KNN_G2 :
    ## Initialisation des parametres
    def __init__(self, k=3):
        self.k = k

    ## Entrainement du modele
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    ## Application à nos données de tests

    def predict(self, X_test): 
        predictions = []
        for x in X_test:
            # Calcul des distances euclidiennes entre x et tous les points de X_train
            distances = np.sqrt(np.sum((self.X_train - x)**2, axis=1))

            # Tri des indices des distances croissantes
            sorted_indices = np.argsort(distances)

            # Sélection des k plus proches voisins
            k_nearest_indices = sorted_indices[:self.k]

            # Obtention des étiquettes des k plus proches voisins
            k_nearest_labels = self.y_train[k_nearest_indices]

            # Prédiction de l'étiquette majoritaire parmi les k plus proches voisins
            prediction = np.bincount(k_nearest_labels).argmax()

            predictions.append(prediction)

        return np.array(predictions)