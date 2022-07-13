import os
#import sys
import time
import git
import datetime
from github import Github
from os import path


# Check ob Update verfügbar
try:
    my_git = Github("LarsFOMO", "2003Lars")                                 #   Login mit User+PW
#   my_git = Github("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")             #   Login mit Token
    my_repo = my_git.get_repo("LarsFOMO/Test-Update")                       #   Repo auswählen

except Exception:
    print("Fehler (0)")

try:
    mod_date = os.path.getmtime('/home/lars/Dokumente/Test/TestPro')    #   Unixzeit (Start 1970)
    #print(mod_date)
    readable_date = datetime.datetime.fromtimestamp(mod_date)           #   Richtige Zeitrechnung
    print('\nLokal Changed on:', readable_date)  
    local_change_date = readable_date

except Exception:
    print("Fehler (1)")


try:
    master = my_repo.get_branch("master")
    sha_com = master.commit
    commit = my_repo.get_commit(sha=sha_com.sha)
    hours = 2
    hours_dazu = datetime.timedelta(hours = hours)
    last_commit_date = commit.commit.author.date + hours_dazu
    print("Last Commit:", last_commit_date) 

except Exception:
    print("Fehler (2)")

try:
    if(last_commit_date > local_change_date):
        print("True")
    elif(last_commit_date < local_change_date):
        print("False")
        
except Exception:
    print("Fehler (3)")

#all_commits = my_code.get_commits()
#print(all_commits)

# Update durchführen Abfrage
eingabe_ok = 1                                                          #   Check ob gültige Eingabe
while(eingabe_ok == 1):
    antwort = input("Ein neues Update ist verfügbar.Möchten Sie es installieren?\n(J,N)\n")
    if(antwort == "J"):

        #for reposi in my_git.get_user().get_repos():
        #    print(reposi.name)
            eingabe_ok = 0

        #contents = my_repo.get_contents("")                         #   Enthaltene Dateien ausgeben
        #for content_file in contents:
        #   print(content_file)

    elif(antwort == "N"):
        eingabe_ok = 0
        break

    elif((antwort != "J") and (antwort != "N")):
        print("Keine gültige Eingabe. Wiederholen Sie die Eingabe")

#return 0
