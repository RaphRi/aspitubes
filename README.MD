# aspitubes

Un petit script qui télécharge en mp3 depuis youtube les tubes d'une
année données.

Pratique pour se constituer rapidement une grosse playlist pour les
soirées privées.

Les tubes sont tirés du site chartsinfrance.net, le calssement officiel
des meilleures ventes de single depuis 1984.
Les 20 premiers de chaque semaine sont récupérées en éliminant les
doublons.


## Ce qu'il faut
- une distribution Linux avec Python (Debian par ex)

- la librairie python urllib3
     sudo apt-get install python-urllib3

- les convertisseurs multimedia
	sudo apt-get install ffmpeg,lame
	
- la dernière version de youtube-dl (https://yt-dl.org/)
     La méthode simple est d'utiliser pypi
     sudo apt-get install python-pip
     sudo pip install --upgrade youtube-dl
     
##Utilisation
1) Se mettre dans un dossier avec de l'espace disque
2) Lancer le script
python aspitubes.py ANNEE

ANNEE est l'année choisie >= 1984

3) attendre plus ou moins longtemps en fonction du débit Internet
les mp3 sont rangés dans le dossier ANNEE sous la forme "artiste - titre.mp3".

##A faire ensuite

Cet outil est certe bien pratique, mais il faut encore pas mal de boulot de tri
derrière.
1) Trier dans des playlists en .m3u thématique pour rendre l'ensemble plus exploitable
Exemple : tubes 80, Slows 80, Rock 80, Dance 90, ...
J'utilise foobar2000 pour ça. Avec son sytème d'onglet hautement configurable
On peut éventuellement faire ça aussi avec les tags mp3. Mais c'est moins
universel je trouve, par rapport à des m3u.

2) Reprendre les chansons de mauvaise qualité ou tout simplement erronées
Comme le script est basé sur une recherche youtube, le premier lien n'est pas
toujours pertinent.
Je stoke les mauvais titres dans un dossier à part et
J'utjlise l'autre script bettersongs.py ANNEE pour ça.

Travail somme toute assez long, à faire petit à petit.
