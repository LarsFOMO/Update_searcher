import os
import time
import git
import datetime
import shutil
import distutils.dir_util
from github import Github
from git.repo.base import Repo
from gitlab import Gitlab
import gitlab_clone
import subprocess
from subprocess import Popen, PIPE
import gitlab
from subprocess import check_output
import dateutil.parser as parser


#   ACHTUNG[1]: Auf ein privates Repository kann nur mit einem Access-Token zugegriffen werden
#       Der Access-Token muss nachdem das Repository auf private gestellt wurde, erzeugt werden.
#       Nur so ist es möglich auf ein privates Repository zuzugreifen. Alles andere funktioniert nicht.
#   Access-Token erzeugen: Settings --> Developer settings --> Personal access tokens
#   ACHTUNG[2]: Dieser Code darf bei einem Update nicht überschrieben/verändert werden, da sonst der 
#   Access Token ungültig wird.
 
fehler = 0
#   Check ob Update verfügbar 
try:
    #my_git = Github("LarsFOMO", "2003Lars")                                                            #   Login mit User+PW
    #my_git = Github("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")                                        #   Login mit Token
    gl = gitlab.Gitlab(url='http://alpmine.synology.me:8080',private_token='')
    #my_repo = my_git.get_repo("LarsFOMO/Test-Update")       #('Code-Tester')                           #   Repo auswählen
    gl.auth()
    project = gl.projects.get('paulsner_lars/Test')

except Exception:
    print("Fehler (0)")
    fehler = 1

#   Abänderungsdatum der lokalen Datei
try:
    mod_date = os.path.getmtime('/home/lars/Dokumente/Test')                                            #   Unixzeit (Start 1970)
    readable_date = datetime.datetime.fromtimestamp(mod_date)                                           #   Richtige Zeitrechnung
    t_time = readable_date
    localTime = t_time.strftime("  %d.%m.%Y, %H:%M:%S")
    print('\nLokal changed on:', localTime)
    local_change_date = readable_date
    localTimestamp = datetime.datetime.timestamp(t_time)
    print(localTimestamp)
    
except Exception:
    print("Fehler (1)")
    fehler = 1

#   Abänderungsdatum des Repositories
#   Für genauere Infos zu 'last_activity_at': https://gitlab.com/gitlab-org/gitlab/-/issues/20952 
try:
    newtime = project.last_activity_at
    date = parser.parse(newtime)                                                                        #   Zeit ist um 2h verschoben
    addhours = 2
    updatedTime = date + datetime.timedelta(hours= addhours)                                            #   Zeit anpassen
    repoTime = updatedTime.strftime("    %d.%m.%Y, %H:%M:%S")
    print('Last Update on:', repoTime)
    repoTimestamp = datetime.datetime.timestamp(updatedTime)
    print(repoTimestamp)    
    
except Exception:
    print("Fehler (2)")
    fehler = 1

#   Prüft ob neuste Version auf Lokal
try:
    repoTimestamp = int(repoTimestamp)
    localTimestamp = int(localTimestamp)+7200

    if(repoTimestamp > localTimestamp):
        print("Es ist ein neues Update verfügbar...")
    elif(repoTimestamp < localTimestamp):
        print("Sie haben bereits die neuste Version der Software auf Ihrem Gerät")
        exit(0)
        
except Exception:
    print("Fehler (3)")
    fehler = 1

#   Update durchführen (Abfrage)?
eingabe_ok = 1                                                                                          #   Check ob gültige Eingabe
while(eingabe_ok == 1):
    antwort = input("Möchten Sie es installieren?\n(J,N)\n")
    if(antwort == "J"):

#   Cloned Repo auf Lokal
        tmp_path = '/home/lars/Dokumente/Foldertmp'   
        local_dest_path = '/home/lars/Dokumente/Test'                                                   #   Zielpfad                      
        os.mkdir(tmp_path)                                                                              #   Neuen Ordner erstellen
        
        git_url = 'http://alpmine.synology.me:8080/paulsner_lars/Test'                                  

        try:
            Repo.clone_from('http://oauth2:f5CzY5syLBy89HPro4ur@alpmine.synology.me:8080/paulsner_lars/Test.git',tmp_path)
        
        except Exception:
            print('Fehler (4)')
            fehler = 1


        distutils.dir_util.copy_tree(tmp_path,local_dest_path)                                          #   Überschreibe alte Verion

        shutil.rmtree(tmp_path,ignore_errors=True)                                                      #   tmp Ordner löschen  

        eingabe_ok = 0
        if(fehler == 0):
            print("Das Update wurde erfolgreich durchgeführt!")

    elif(antwort == "N"):
        eingabe_ok = 0
        break

    elif((antwort != "J") and (antwort != "N")):
        print("Keine gültige Eingabe. Wiederholen Sie die Eingabe")