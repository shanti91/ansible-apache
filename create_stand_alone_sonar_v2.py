import os
import git
import sys
import pickle
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from git import Repo
from sonarqube import SonarQubeClient


###############################################################################################
### FUNC ######################################################################################
def git_clone(repo_name):
    try:
        repo = git.Repo.clone_from("https://isx46995096:glpat-Qn9SQJiaHgxyYk5GSDYC@gitlab.com/isx46995096/" + repo_name + ".git",
                               "/home/kadmin/"+repo_name,
                               branch='master')
    except: print("GIT Repository already exists,proceed to create project in sonarqube for first scan")


#API - library reuest
#import requests

#r = requests.get('https://api')
#print(r.content)
#open('temp.txt', 'wb').write(r.content)
###############################################################################################

def create_proj_sonar(proj_key,proj_name):
    try:
        sonar.projects.create_project(project=proj_key, name=proj_name, visibility="private")
        print("SONARQUBE: Your new project has been created")
    except:
        print("SONARQUBE: Project already exist in Sonarqube")

###############################################################################################

def create_token_sonar(proj_name):
    try:
        user_token = sonar.user_tokens.generate_user_token("token" + proj_name)
        print("SONARQUBE: Your token for the project is:",user_token["token"])

        # Save token in a file
        file = open('token'+proj_name+'.txt', 'w',encoding='utf-8')
        file.write(user_token["token"])
        file.close()

        return user_token

    except: 
        print("SONARQUBE: The token for this Sonar project already exist. Contact administrator")

###############################################################################################


#### INIT VARS for SONARQUBE 
url = 'http://localhost:9000'
username = "admin"
password = "qwerty"
sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)


#### CODE

# Clone repo from git to local for scan
git_clone(sys.argv[1])

# Create project in sonar for first scan 
create_proj_sonar(sys.argv[1],sys.argv[1])

# Create token for scan
user_token_sonar= create_token_sonar(sys.argv[1])


#Make first scan
os.system("sonar-scanner -Dsonar.projectKey="+sys.argv[1]+" -Dsonar.sources=/home/kadmin/"+sys.argv[1]+" -Dsonar.host.url=http://192.168.111.128:9000 -Dsonar.login="+ user_token_sonar["token"])

