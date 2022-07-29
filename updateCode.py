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
from subprocess import Popen
import gitlab
from subprocess import check_output


#   ACHTUNG[1]: Auf ein privates Repository kann nur mit einem Access-Token zugegriffen werden
#       Der Access-Token muss nachdem das Repository auf private gestellt wurde, erzeugt werden.
#       Nur so ist es möglich auf ein privates Repository zuzugreifen. Alles andere funktioniert nicht.
#   Access-Token erzeugen: Settings --> Developer settings --> Personal access tokens
#   ACHTUNG[2]: Dieser Code darf bei einem Update nicht überschrieben/verändert werden, da sonst der 
#   Access Token ungültig wird.
 
fehler = 0
#   Check ob Update verfügbar 
try:
    #my_git = Github("LarsFOMO", "2003Lars")                                #   Login mit User+PW
    #my_git = Github("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")     #Gitlab("NE2Ffawd5s3HgE3XcXfn")#    #   Login mit Token
    gl = gitlab.Gitlab(url='http://alpmine.synology.me:8080',private_token='NE2Ffawd5s3HgE3XcXfn')
    #my_repo = my_git.get_repo("LarsFOMO/Test-Update")       #('Code-Tester')                #   Repo auswählen
    gl.auth()
    project = gl.projects.get('paulsner_lars/Test')

except Exception:
    print("Fehler (0)")
    fehler = 1

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
    fehler = 1

#   Letztes Commit Datum
#repo_url = 'http://alpmine.synology.me:8080/paulsner_lars/Test.git'
#process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
date_string = check_output('git log -1 --pretty=format:"%ci"'.split()).decode()
print(date_string)
try:
    print(project.events.list(10))
    master = my_repo.get_branch("master")
    sha_com = master.commit
    commit = my_repo.get_commit(sha=sha_com.sha)
    hours = 2
    hours_dazu = datetime.timedelta(hours = hours)
    last_commit_date = commit.commit.author.date + hours_dazu
    t2_time = last_commit_date
    print("Last Commit:", t2_time.strftime("     %d.%m.%Y, %H:%M:%S"))
    
except Exception:
    print("Fehler (2)")
    fehler = 1

#   Prüft ob neuste Version auf Lokal
try:
    if(last_commit_date > local_change_date):
        print("Ein neues Update ist verfügbar")
    elif(last_commit_date < local_change_date):
        print("Sie haben bereits die neuste Version der Software auf Ihrem Gerät")
        exit(0)
        
except Exception:
    print("Fehler (3)")
    fehler = 1

#   Update durchführen (Abfrage)?
eingabe_ok = 1                                                              #   Check ob gültige Eingabe
while(eingabe_ok == 1):
    antwort = input("Möchten Sie es installieren?\n(J,N)\n")
    if(antwort == "J"):

#   Cloned Repo auf Lokal
        tmp_path = '/home/lars/Dokumente/Foldertmp' #"/home/lars/Dokumente/Folder_tmp"  
        local_dest_path = '/home/lars/Dokumente/Test'  #'/home/lars/Dokumente/Test'                       #   Zielpfad                      
        os.mkdir(tmp_path)                                                  #   Neuen Ordner erstellen
        
       ## repo_URL = 'https://github.com/LarsFOMO/Test-Update.git'
        git_url = 'http://alpmine.synology.me:8080/paulsner_lars/Test'#'http://gitlab-goe/paulsner_lars/test.git'

        try:
            #Repo.clone_from(git_url,tmp_path)
            #subprocess.call(['git','clone',git_url,tmp_path])
            git.Repo.clone_from(git_url,tmp_path)
            
            #Popen(['git','clone',git_url,tmp_path])
           ## Repo.clone_from(repo_URL,tmp_path)                          #   In tmp_path kopieren
        except Exception:
            print('Fehler (4)')
            fehler = 1


        distutils.dir_util.copy_tree(tmp_path,local_dest_path)              #   Überschreibe alte Verion

        shutil.rmtree(tmp_path,ignore_errors=True)                                           #   tmp Ordner löschen  

        eingabe_ok = 0
        if(fehler == 0):
            print("Das Update wurde erfolgreich durchgeführt!")

    elif(antwort == "N"):
        eingabe_ok = 0
        break

    elif((antwort != "J") and (antwort != "N")):
        print("Keine gültige Eingabe. Wiederholen Sie die Eingabe")