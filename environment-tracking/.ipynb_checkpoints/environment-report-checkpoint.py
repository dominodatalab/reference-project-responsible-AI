#set up API
import requests
import json
import os
import platform
import subprocess
import time

#set up API key and headers
api_key = os.environ['DOMINO_USER_API_KEY']
headers = {'X-Domino-Api-Key': api_key,  'Content-Type': 'application/json'}  

#api host
host = os.environ['DOMINO_API_HOST']

#get user id
r_user = requests.get('{host}/v4/users/self'.format(host=host), headers=headers)
user_id = r_user.json()['id']
username = os.environ['DOMINO_STARTING_USERNAME']

#get project id
project_name = os.environ['DOMINO_PROJECT_NAME']
url_project = '{host}/v4/projects?name={project_name}&ownerId={user_id}'.format(
                                host=host, project_name=project_name, user_id=user_id)
r_project = requests.get(url_project, headers=headers)
projectId = r_project.json()[0]['id']

#get environment for current run
run_id = os.environ['DOMINO_RUN_ID']
run_url = '{host}/v4/workspace/project/{projectId}/sessions/{run_id}'.format(host=host, 
                                                                            projectId=projectId,
                                                                            run_id=run_id)
r_run = requests.get(run_url, headers=headers)

#extract environment name and revision
envname = r_run.json()['config']['environment']['name']
env_rev = r_run.json()['config']['environment']['revisionNumber']
env_id = r_run.json()['config']['environment']['id']
env_rev_id = r_run.json()['config']['environment']['revisionId']

#get environment revision details
env_url = '{host}/v4/environments/environmentRevision/{environmentRevisionId}'.format(host=host,
                                                                                     environmentRevisionId=env_rev_id)
r_env = requests.get(env_url, headers=headers)

#extract environment revision details
env_docker = r_env.json()['environmentRevision']['dockerfileInstructions']
env_prescript = r_env.json()['environmentRevision']['preRunScript']
env_postscript = r_env.json()['environmentRevision']['postRunScript']
env_image = r_env.json()['environmentRevision']['imageType']

#write environment report to file

#check if file exists and create if not
host_file = "environment-report.txt"
    
with open(host_file, "w+") as f:
    f.write('ENVIRONMENT REPORT\n')

with open(host_file, "a+") as file:
    file.write('------------------------------------------------------------------------------------\n')
    file.write('Run starting time: \n')
    file.write(time.strftime("%H:%M:%S%Z", time.localtime()))
    file.write('\n')
    file.write('Run started by Domino user: {username}\n'.format(username=username))
    file.write('Domino Environment Name: {envname}, Revision: {env_rev}, Environment_ID     {env_id}\n'.format(envname=envname, env_rev=env_rev, env_id=env_id))
    file.write('Domino Environment image type: {env_image}\n'.format(env_image=env_image))
    file.write('Domino Environment Dockerfile Instructions:\n')
    file.write('\n')
    file.write('------------------------------------------------------------------------------------\n')
    file.write('{env_docker}\n'.format(env_docker=env_docker))

    file.write('Pre-run Script:\n') 
    file.write('{env_prescript}\n'.format(env_prescript=env_prescript))
    file.write('\n')
    file.write('Post-run Script:\n') 
    file.write('{env_postscript}\n'.format(env_postscript=env_postscript)) 
    file.write('\n')
    file.write('------------------------------------------------------------------------------------\n')
    file.write('Platform Info:\n')
    file.write('platform :{}\n'.format(platform.platform()))
    file.write('system   :{}\n'.format(platform.system()))
    file.write('release  :{}\n'.format(platform.release()))
    file.write('version  :{}\n'.format(platform.version()))
    file.write('machine  :{}\n'.format(platform.machine()))
    file.write('processor:{}\n'.format(platform.processor()))
    file.write('\n')
    file.write('Python Interpreter:\n')
    file.write('Python Version :{}\n'.format(platform.python_version()))
    file.write('Compiler       :{}\n'.format(platform.python_compiler()))
    file.write('Build          :{}\n'.format(platform.python_build()))
    file.write('\n')
    file.write('Python packages not in environment but installed during session:\n')
    with open("session_packages_not_in_environment.txt") as file2:
        lines = file2.readlines()
        file.writelines(lines)
    file.write('\n')
    file.write('\n')
    file.write('Installed Python packages:\n')
               

subprocess.run("pip list >> environment.txt", shell=True)