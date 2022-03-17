# monit-ods

Monitoring des géodonnées ouvertes publiées sur OpenDataSoft.


## Principe

Un script python interroge le catalogue de métadonnées et produit un fichier de configuration pour [monit](https://mmonit.com/monit/).


1. on interroge le catalogue des métadonnées https://public.sig.rennesmetropole.fr/geonetwork/
2. on récupère une liste de métadonnées
3. pour chaque métadonnée, on récupère l'identifiant OpenDataSoft déclaré dans l'url du `linkage`
4. pour chaque métadonnée / jeu de données ODS, une configuration `checkhost` est créée dans un fichier de configuration

Le script python ne peut être lancé qu'une fois par jour.
La modification du fichier de config de monit nécessite son rechargement juste après.


## Installation

### Le script python

```bash
git clone https://github.com/sigrennesmetropole/monit-ods.git

cd monit-ods

# création session virtuelle python
python -m venv venv
source venv/bin/activate

# les librairies nécessaires
python -m pip install --upgrade pip
python -m pip install owslib
```

### Le cron

TODO

## Utilisation

```bash
python main.py
```


## Notes

### exemple de configuration checkhost

```
    check host horodateur-rennes
      with address data.rennesmetropole.fr
      every "0 7-18 * * *"
      if failed
        port 443
        protocol https
        request /explore/dataset/horodateur-rennes/information/
        status = 200
      then alert
```

### Exemple de requête CSW getRecordById

[https://public.sig.rennesmetropole.fr/geonetwork/srv/fre/csw?service=CSW&version=2.0.2&elementSetName=full&request=GetRecordById&id=b705395e-a1c4-4e6c-b069-d35b2efe1a45](https://public.sig.rennesmetropole.fr/geonetwork/srv/fre/csw?service=CSW&version=2.0.2&elementSetName=full&request=GetRecordById&id=b705395e-a1c4-4e6c-b069-d35b2efe1a45)

