import os
import time
import git
import datetime
import shutil
import distutils.dir_util
from github import Github
from git.repo.base import Repo


# Check ob Update verfügbar
#   ACHTUNG: Auf ein privates Repository kann nur mit einem Access-Token zugegriffen werden
try:
    #my_git = Github("LarsFOMO", "2003Lars")                                #   Login mit User+PW
    my_git = Github(" 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")            #   Login mit Token
    my_repo = my_git.get_repo("LarsFOMO/Test-Update")                       #   Repo auswählen
    

except Exception:
    print("Fehler (0)")

#   Abänderungsdatum der lokalen Datei
try:
    mod_date = os.path.getmtime('/home/lars/Dokumente/Test')                #   Unixzeit (Start 1970)
    #print(mod_date)
    readable_date = datetime.datetime.fromtimestamp(mod_date)               #   Richtige Zeitrechnung
    t_time = readable_date
    print('\nLokal Changed on:', t_time.strftime("%d.%m.%Y, %H:%M:%S"))
    local_change_date = readable_date

except Exception:
    print("Fehler (1)")

#   Letztes Commit Datum
try:
    master = my_repo.get_branch("master")
    sha_com = master.commit
    commit = my_repo.get_commit(sha=sha_com.sha)
    hours = 2
    hours_dazu = datetime.timedelta(hours = hours)
    last_commit_date = commit.commit.author.date + hours_dazu
    t2_time = last_commit_date
    print("Last Commit:", t2_time.strftime("     %d.%m.%Y, %H:%M:%S"))#last_commit_date) 
    

except Exception:
    print("Fehler (2)")

#   Prüft ob neuste Version auf Lokal
try:
    if(last_commit_date > local_change_date):
        print("Ein neues Update ist verfügbar")
    elif(last_commit_date < local_change_date):
        print("Sie haben bereits die neuste Version der Software auf Ihrem Gerät")
        exit(0)
        
except Exception:
    print("Fehler (3)")

#   Update durchführen (Abfrage)?
eingabe_ok = 1                                                              #   Check ob gültige Eingabe
while(eingabe_ok == 1):
    antwort = input("Möchten Sie es installieren?\n(J,N)\n")
    if(antwort == "J"):

#   Cloned Repo auf Lokal
        tmp_path = "/home/lars/Dokumente/Folder_tmp"  
        local_dest_path = '/home/lars/Dokumente/Test'                       #   Zielpfad                      
        os.mkdir(tmp_path)                                                  #   Neuen Ordner erstellen
        
        try:
            repo_URL = 'https://github.com/LarsFOMO/Test-Update.git'
            try:
                Repo.clone_from(repo_URL,tmp_path)                          #   In tmp_path kopieren
            except Exception:
                print('Fehler (4)')

        except Exception:
            print("Fehler (5)")

        distutils.dir_util.copy_tree(tmp_path,local_dest_path)              #   Überschreibe alte Verion

        shutil.rmtree(tmp_path)                                             #   tmp Ordner löschen  

        eingabe_ok = 0

    elif(antwort == "N"):
        eingabe_ok = 0
        break

    elif((antwort != "J") and (antwort != "N")):
        print("Keine gültige Eingabe. Wiederholen Sie die Eingabe")

