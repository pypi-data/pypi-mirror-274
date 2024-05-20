# ***************************************************** DESCRIPTION GENERAL DU PROJET ******************************************

Ce README explique comment installer le package et comment l'utiliser.
Le package a été developpé  pour réaliser des taches de classification (avec KNN) et de clustering (avec KMeans).

# ***************************************************** CONFIGURATION COMPATIBLE ******************************************

Ce package est à sa premiere version sur pypi et ne fonctionne qu'avec les versions de python supérieures ou égales à 3.10
Par ailleurs il fonctionne avec tout type de système d'installation.

# ***************************************************** INSTALLATION ******************************************

Pour installation le package executez la commande : pip install Package-G2==1.0.1

# ***************************************************** UTILISATION ******************************************

Voici comment utiliser les fonctionnalités de ce package :

## Clustering (KMeans)
import KMeans_G2
from  KMeans_G2 import KMeans_G2

## Application
### Définir le K  et la variable X qui contiendra les données et appliquer le KMeans à nos données avec la fonction ".kmeans_G2".
X = np.random.rand(100, 2)

### En sortie, c'est trois resultats à savoir les classes  de chaque individus (1er) le centre des classes (2eme) et le nombre d'itération (3eme)

### Première methode
classes, centres, iteration = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(classes) 

#### Afficher les centres de classes
print(centres)

#### Afficher le nombre d'itération fait
print(iteration)

## Deuxième methodes

result = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(result[0]) 

#### Afficher les centres de classes
print(result[1]) 

#### Afficher le nombre d'itération fait
print(result[2]) 


## Clustering (KNN)

## Classification (KNN)
from  KNN_G2 import KNN_G2
Définir les variables X_train, y_train qui contiendront les données d'entrainement du modèle.
Définir la variable X_test contiendra les données de test

## Exemple
## X_train = [[0, 0], [1, 1], [2, 2], [3, 3]]
## y_train = [0, 1, 2, 3]
## X_test = [[1.1, 1.1], [2.1, 2.1]]

Exécuter KNN(k) , k étant le nombre de voisins
Exécuter KNN.fit(X_train,y_train)
Ensuite exécuter KNN.PREDICT(X_test)
on peut afficher les prédictions avec :
print(KNN.PREDICT(X_test))

## Démarrage
Il faut noter qu'au préalable il faut installer les packages pandas et numpy pour linstastallation de Package-G2==1.0.0.

# ***************************************************** DESCRIPTION GENERAL DU PROJET ******************************************

Ce README explique comment installer le package et comment l'utiliser.
Le package a été developpé  pour réaliser des taches de classification (avec KNN) et de clustering (avec KMeans).

# ***************************************************** CONFIGURATION COMPATIBLE ******************************************

Ce package est à sa premiere version sur pypi et ne fonctionne qu'avec les versions de python supérieures ou égales à 3.10
Par ailleurs il fonctionne avec tout type de système d'installation.

# ***************************************************** INSTALLATION ******************************************

Pour installation le package executez la commande : pip install Package-G2==1.0.1

# ***************************************************** UTILISATION ******************************************

Voici comment utiliser les fonctionnalités de ce package :

## Clustering (KMeans)
import KMeans_G2
from  KMeans_G2 import KMeans_G2

## Application
### Définir le K  et la variable X qui contiendra les données et appliquer le KMeans à nos données avec la fonction ".kmeans_G2".
X = np.random.rand(100, 2)

### En sortie, c'est trois resultats à savoir les classes  de chaque individus (1er) le centre des classes (2eme) et le nombre d'itération (3eme)

### Première methode
classes, centres, iteration = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(classes) 

#### Afficher les centres de classes
print(centres)

#### Afficher le nombre d'itération fait
print(iteration)

## Deuxième methodes

result = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(result[0]) 

#### Afficher les centres de classes
print(result[1]) 

#### Afficher le nombre d'itération fait
print(result[2]) 


## Clustering (KNN)

## Classification (KNN)
from  KNN_G2 import KNN_G2
Définir les variables X_train, y_train qui contiendront les données d'entrainement du modèle.
Définir la variable X_test contiendra les données de test

## Exemple
## X_train = [[0, 0], [1, 1], [2, 2], [3, 3]]
## y_train = [0, 1, 2, 3]
## X_test = [[1.1, 1.1], [2.1, 2.1]]

Exécuter KNN(k) , k étant le nombre de voisins
Exécuter KNN.fit(X_train,y_train)
Ensuite exécuter KNN.PREDICT(X_test)
on peut afficher les prédictions avec :
print(KNN.PREDICT(X_test))

## Démarrage
Il faut noter qu'au préalable il faut installer les packages pandas et numpy pour linstastallation de Package-G2==1.0.0.

######                        ###################        ###################     ##############



# ***************************************************** DESCRIPTION GENERAL DU PROJET ******************************************

Ce README explique comment installer le package et comment l'utiliser.
Le package a été developpé  pour réaliser des taches de classification (avec KNN) et de clustering (avec KMeans).

# ***************************************************** CONFIGURATION COMPATIBLE ******************************************

Ce package est à sa premiere version sur pypi et ne fonctionne qu'avec les versions de python supérieures ou égales à 3.10
Par ailleurs il fonctionne avec tout type de système d'installation.

# ***************************************************** INSTALLATION ******************************************

Pour installation le package executez la commande : pip install Package-G2==1.0.1

# ***************************************************** UTILISATION ******************************************

Voici comment utiliser les fonctionnalités de ce package :

## Clustering (KMeans)
import KMeans_G2
from  KMeans_G2 import KMeans_G2

## Application
### Définir le K  et la variable X qui contiendra les données et appliquer le KMeans à nos données avec la fonction ".kmeans_G2".
X = np.random.rand(100, 2)

### En sortie, c'est trois resultats à savoir les classes  de chaque individus (1er) le centre des classes (2eme) et le nombre d'itération (3eme)

### Première methode
classes, centres, iteration = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(classes) 

#### Afficher les centres de classes
print(centres)

#### Afficher le nombre d'itération fait
print(iteration)

## Deuxième methodes

result = KMeans_G2.kmeans_G2(X,5)

#### Afficher les classes 
print(result[0]) 

#### Afficher les centres de classes
print(result[1]) 

#### Afficher le nombre d'itération fait
print(result[2]) 


## Clustering (KNN)

## Classification (KNN)
import KNN_G2
from  KNN_G2 import KNN_G2

* Définir les variables X_train, y_train qui contiendront les données d'entrainement du modèle.
* Définir la variable X_test contiendra les données de test

## Exemple
X_train = [[0, 0], [1, 1], [2, 2], [3, 3]]
y_train = [0, 1, 2, 3]
X_test = [[1.1, 1.1], [2.1, 2.1]]


KNN=KNN_G2(3)

Entrainement = KNN.fit(X_train, y_train)
prediction = KNN.predict(X_test)
print("Predictions:", prediction)
## Démarrage
Il faut noter qu'au préalable il faut installer les packages pandas et numpy pour linstastallation de Package-G2==1.0.0.

######                        ###################        ###################     ##############

# ***************************************************** Auteur et contact******************************************

* Nom :KABRE  Prénom: Oumarou Mail : kabreoumarou95@gmail.com
* Nom :YODA  Prénom: Abdoul Djamal Mail : yodaa6362@gmail.com
* Nom :KAFANDO  Prénom: G. Judicaël Oscar Mail : kafjudicaeloscar@gmail.com