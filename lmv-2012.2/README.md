Antragsbuch für Mitgliederversammlungen
=======================================

Was ist das hier?
-----------------

Für die Landesmitgliederversammlung 2012.2 des Landesverbandes Mecklenburg-Vorpommern der Piratenpartei (http://wiki.piratenpartei.de/MV:Landesmitgliederversammlung_2012.2) haben wir ein Antragsbuch (Datei `antragsbuch.pdf`) automatisch aus den erzeugten Anträgen erzeugt.

Erzeugen eines Dokumentes
-------------------------

In der aktuellen Konfiguration werden offene Anträge aus dem Projekt https://redmine.piratenpartei-mv.de/projects/lpt geladen. Falls in einem Antrag das Feld "Liquid Feedback Initiative" ausgefüllt ist, wird weiterhin das Liquid Feedback des Landesverbandes Mecklenburg-Vorpommern (https://lqpp.de/mv) abgefragt.

Mit `make` wird ein PDF mit allen Anträgen erzeugt.

Aktualisieren
-------------

Das Abfragen der Anträge kann mit

    cd antraege
    ./getantraege.py

gestartet werden. Wenn ein neues Antragsbuch erstellt werden soll, müssen alle Dateien bis auf `getantraege.py` aus dem Verzeichnis `antraege` gelöscht werden.

Anpassen der Antragsreihenfolge
-------------------------------

Die eigentliche Magie passiert im Latex-Dokument `antragsbuch.tex`. Dort kann die Antragsreihenfolge mit den Makroaufrufen `\LPTantrag{}` gesteuert werden. Das `Makefile` ruft automatisch XeLatex oft genug auf, sodass Indizes, Inhaltsverzeichnis und Querverweise korrekt sind.

Voraussetzungen
---------------

- Anträge müssen in einem Redmine-System gepflegt werden. Am besten habt ihr dazu ein Projekt wie https://redmine.piratenpartei-mv.de/projects/lpt in dem Anträge wie https://redmine.piratenpartei-mv.de/issues/423 aussehen. Die Quelle müsst ihr im Script `antraege/getantraege.py` anpassen.
- Optional braucht ihr einen Zugang zu einer Liquid-Feedback-JSON-API, um Initiativen auszulesen und einzutragen.
- Weitere Dokumente wie Satzung oder Wahlordnung haben wir im Verzeichnis `anhaenge` abgelegt.
- Für die Erzeugung des PDFs wird XeLatex benötigt.
- Wir nutzen viele viele Latex-Pakete - siehe Datei `antragsbuch.tex`.

Fragen
------

Bei Fragen bitte eine Mail an support@piraten-mv.de schreiben. Wir helfen gerne!