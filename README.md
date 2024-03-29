BEKI
====


Neuauflage von `bekiga`: Erzeugen von Prüfprotokollen (für Kindergärten).


## Allgemein

Du siehst eine Web-Applikation, welche im Front-End durch [VueJs](https://v3.vuejs.org/) und im Backend durch [Flask](https://flask.palletsprojects.com/en/1.1.x/) getrieben wird.
Als Datenbank wird momentan eine einfache SQlite-Datenbank verwendet, wobei eine Vielzahl durch Plug-N-Play einsetzbar sein sollte.

Es gibt leider keine Doku, da zu viel Arbeit - ich werde jegliche Pull-Requests akzeptieren.

## Deployment

Eine Production-ähnliche Umgebung wird in Form eines Docker-Images exemplarisch bereitgestellt.
Dieses benutzt [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) sowie [nginx](https://www.nginx.com/).

Zum bundlen kann das folgende Script verwendet werden:
```bash
$ python3 scripts/bundle.py
```

Hierfür wird eine Node >13 Installation benötigt.

Anschließend kann ein Docker-Image mit den in `dist/` verfügbaren Dateien erstellt werden.
Eventuelle Konfiguration kann angepasst werden.

```bash
$ cd dist/
$ docker build -t beki .
```

Standardmäßg kann der Server dann im Container ausgeführt werden.
Alternativ steht ein Pre-Built im Hub zur Verfügung: https://hub.docker.com/r/milck/beki.
Es wird erwartet, dass ein Ordner in `/mnt/beki` eingebunden ist, in welchem persistente Informationen gespeichert werden:
```
$ ls data
uploads/
beki.db
err.log
$ docker run -d -p 80:5000 -v $(PWD)/data:/mnt/beki milck/beki:latest
```

WARNUNG: Das Deployment ist sicherheitstechnisch nicht zu empfehlen, inbesondere da der uWSGI Server als `root` ausgeführt wird.

## Migration von `bekiga`

Zur Migration von der alten `bekiga` Version werden einige Scripte zur Verfügung gestellt.
Siehe hierzu [scripts/migrate/](scripts/migrate).
