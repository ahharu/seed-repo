# coding=utf-8
from fabric.api import task, settings, local
from jenkins_mngmt import JenkinsManagment
import imp
import json
import os.path
import sys
import stashy
from fabric.api import task
import jenkins_mngmt
import stash_mngmt
import re
from jenkinsapi.jenkins import Jenkins

from config import JENKINS_JOB
from config import SSHCHAINGIT
from config import STASH_SERVER

SSHCHAIN = SSHCHAINGIT
generatedrepos = []

def test_pattern(pattern, mylist):
  if pattern in ",".join(mylist):
      return True
  return False

def delete_repo(project, repo, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.delete_repo(project, repo,
                                               )
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")

def update_hook_repo(projects_repos, user, password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    for project_repo in projects_repos:
        if project_repo:
            try:
                stash_server.update_hook_repo(*project_repo)
            except:
                print ("The Stash Repo Doesnt Exist")

def update_branch_permissions(project, repo, branch_permissions, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.update_branch_permissions(project, repo,
                                               branch_permissions)
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")

def update_group_permissions(project, repo, group_permissions, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.update_group_permissions(project, repo,
                                              group_permissions)
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")
        
def update_user_permissions(project, repo, user_permissions, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.update_user_permissions(project, repo,
                                              user_permissions)
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")

def archive_repo(project, repo, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.archive_repo(project, repo,
                                              )
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")

def unarchive_repo(project, repo, user,
                             password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.unarchive_repo(project, repo,
                                              )
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")


def start_and_init_repo(project, repo, user,
                             password,fork=None,sync=None):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.start_and_init_repo(project, repo,
                                         user,password,fork,sync)
    except Exception as e:
        print(e.message)
        print ("The Stash Repo Doesnt Exist")

def create_branches(project, repo, branch_list, user,
                    password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    try:
        stash_server.create_branches(project, repo,
                                     branch_list)
    except Exception, e:
        print ("The Stash Repo Doesnt Exist")

def validate_repos(projects_repos, user, password):
    stash_server = stash_mngmt.StashyManagment(user, password,
                                           STASH_SERVER)
    messages_end = []
    for project_repo in projects_repos:
        if project_repo:
            try:
                stash_server.stash_server.projects[project_repo[1]].repos[
                    project_repo[2]].get()
            except:
                messages_end.append("The Repository is invalid for job %s" %
                       project_repo[0])
                continue
            repo = stash_server.stash_server.projects[project_repo[
                1]].repos[project_repo[2]]
            git_branches = [b['displayId'].lstrip('*/').rstrip('/*').rstrip(
                '/*') for b in list(repo.branches())]
            jenkins_branches = [b.lstrip('*/').rstrip('/*').rstrip('/*') for
                                b in project_repo[4]]
            broken_branches_job = True
            for branch in jenkins_branches:
                if not test_pattern(branch, git_branches ):
                    print("No Branch matching %s for job %s" % (
                        branch, project_repo[0]))
                else:
                    broken_branches_job = False
            if broken_branches_job:
                messages_end.append("The Job %s doesnt match ANY branch" % project_repo[0])

    for msg in messages_end:
        print(msg)



def is_permission_valid(permission):
    valid_permissions = ['REPO_ADMIN','REPO_WRITE','REPO_READ']
    if permission in valid_permissions:
        return True
    else:
        return False

@task
def update_all_jobs(jenkins_url, user, password, stash_password):
    server = JenkinsManagment(jenkins_url, user, password)
    update_hook_repo(server.update_stash_config_all_jobs(), user,
                     stash_password)

@task
def validate_all_jobs(jenkins_url, user, password, stash_password):
    server = JenkinsManagment(jenkins_url, user, password)
    validate_repos(server.get_stash_config_all_jobs(), user,
                     stash_password)

@task
def update_joblist(jenkins_url, user, password, joblist, stash_password):
    server = JenkinsManagment(jenkins_url, user, password)
    update_hook_repo(server.update_stash_config_list_jobs(joblist.split('|')),
                     user, stash_password)

@task
def update_pattern(jenkins_url, user, password, pattern, stash_password):
    server = JenkinsManagment(jenkins_url, user, password)
    update_hook_repo(server.update_stash_config_pattern_jobs(pattern),
                     user, stash_password)

@task
def backup_all_jobs(jenkins_url, user, password, path):
    server = JenkinsManagment(jenkins_url, user, password)

    for job in server.get_jobs_list():
        job_instance = server.get_job(job)
        xml = job_instance.get_config()
        with open("%s%s.xml" % (path, job['name']), 'w+') as f:
            f.write(xml)


@task
def update_all_from_templates():
    templatefolder = os.getcwd()+'/templates'
    jsonfiles = os.listdir(templatefolder)

    global generatedrepos


    for file in jsonfiles:
        create_and_init_repo(templatefolder+'/'+file,os.getenv('stash_username'),os.getenv('stash_password'))
    print("")
    print("---GENERATED REPOS---")
    for repo in generatedrepos:
        print repo.encode('ascii')
    print("---END GENERATED REPOS---")

def get_project_repo_from_stash_url(url):
    return (url.split('/')[5],url.split('/')[7])

def get_last_build_console(jenkins):
    try:
        console = jenkins.get_job(JENKINS_JOB).get_last_good_build().get_console()
    except:
        return ""
    return console

def listify(*args):
     x=[]
     for i in args:
             if '__iter__' in dir(i):
                     x+=list(i)
             else:
                     x.append(i)
     return x

def work_for_one_project(repoentry,project,stash_user,stash_password):
    stash = stashy.connect(STASH_SERVER, stash_user,
                            stash_password)
    global generatedrepos
    repoexists = True

    try:
        stash.projects.get(repoentry['project'])
    except Exception:
        print("Project does not exist. Exiting")
        return

    ## ok so it exists, lets create repository

    for repository in listify(repoentry['repository']):

        shouldarchive = False
        shouldunarchive = False
        repoexists=True
        archived=False
        arrepos = [xpr['name'].encode('ascii') for xpr in stash.projects['AR'].repos.list()]
        prrepos = [xpr['name'].encode('ascii') for xpr in stash.projects[repoentry['project']].repos.list()]

        if repoentry.has_key('archived'):

            if repoentry['archived'] == True:

                if repository.encode('ascii') in prrepos:
                    shouldarchive = True

                if repository.encode('ascii') in arrepos:
                    archived = True


                if not repository.encode('ascii') in prrepos and not repository.encode('ascii') in arrepos:
                    repoexists = False
            else:
                if repository.encode('ascii') in arrepos:
                    shouldunarchive = True
                    repoexists = True
                else:
                    try:
                        stash.projects[repoentry['project']].\
                            repos[repository].get()
                    except:
                        repoexists = False

        else:
            if repository.encode('ascii') in arrepos:
                shouldunarchive = True
                repoexists = True
            else:
                try:
                    stash.projects[repoentry['project']].\
                        repos[repository].get()
                except:
                    repoexists = False
    
        ## Add to the list
    
    

        if not repoexists:

        # If the repo doesnt exist, create it
            if not repoentry.has_key('forked_from'):
                start_and_init_repo(repoentry['project'],repository,
                                    stash_user,stash_password)
            else:
                start_and_init_repo(repoentry['project'],repository,
                                    stash_user,stash_password,repoentry['forked_from'],repoentry['forked_from']['sync'])

        if archived:
            generatedrepos.append(stash.projects['AR'].
                      repos[repository].
                      get()['links']['self'][0]['href'].encode('ascii'))
            continue
        if shouldarchive:
            archive_repo(repoentry['project'],repository,stash_user,stash_password)
            generatedrepos.append(stash.projects['AR'].
                      repos[repository].
                      get()['links']['self'][0]['href'].encode('ascii'))
            continue

        if shouldunarchive:
            unarchive_repo(repoentry['project'],repository,stash_user,stash_password)
            generatedrepos.append(stash.projects[repoentry['project']].
                      repos[repository].
                      get()['links']['self'][0]['href'].encode('ascii'))
            continue

        if repoentry.has_key('additional_branches'):
            create_branches(repoentry['project'],repository,
                            repoentry['additional_branches'],stash_user,
                            stash_password)
    
        ## If there are specified user permissions in JSON, grant them
        if repoentry.has_key('userpermissions'):
            update_user_permissions(repoentry['project'],
                                      repository,
                                      repoentry['userpermissions'],stash_user,
                                      stash_password )
    
        ## Same for group permissions
    
        if repoentry.has_key('grouppermissions'):
            update_group_permissions(repoentry['project'],
                                      repository,
                                      repoentry['grouppermissions'],stash_user,
                                      stash_password )
    
        ## And for branch permissions
    
        if repoentry.has_key('branchpermissions'):
            #Clean all branch permissions and recreate
            update_branch_permissions(repoentry['project'],
                                      repository,
                                      repoentry['branchpermissions'],stash_user,
                                      stash_password)
    
        ## Repo Hook
    
        if repoentry.has_key('jenkins_hook'):
            if repoentry['jenkins_hook']:
                update_hook_repo([[repoentry['project'],repository,
                                   SSHCHAIN.format(repoentry['project'],
                                                   repository).lower(),
                                   True]],
                             stash_user,stash_password)
            else:
                update_hook_repo([[repoentry['project'],repository,
                                   SSHCHAIN.format(repoentry['project'],
                                                   repository).lower(),False]],
                             stash_user,stash_password)
        else:
                update_hook_repo([[repoentry['project'],repository,
                                   SSHCHAIN.format(repoentry['project'],
                                                   repository).lower(),False]],
                             stash_user,stash_password)
        generatedrepos.append(stash.projects[repoentry['project']].
                  repos[repository].
                  get()['links']['self'][0]['href'].encode('ascii'))

@task
def create_and_init_repo(json_path, stash_user, stash_password):


    jenkins = jenkins_mngmt.JenkinsManagment(STASH_SERVER)
    if not os.path.isfile(json_path):
        raise IOError("File not found")
    with open(json_path) as jsonfile:
        data = json.load(jsonfile)

        global generatedrepos
        stash = stashy.connect(STASH_SERVER, stash_user,
                                stash_password)
        for repoentry in data:
            ## Check if the project specified exists
            work_for_one_project(repoentry,repoentry['project'],stash_user,stash_password)




        ##Creation Finished so now delete the useless ones
        newgenrepos = [get_project_repo_from_stash_url(x) for x in generatedrepos]
        try:
            gotconsole = get_last_build_console(jenkins).replace("\n","")
        except:
            return
        try:
            tmprepos = re.search(r'---GENERATED REPOS---(.*)---END GENERATED REPOS---', gotconsole).groups()[0]
            tmprepos = tmprepos.split('https://')
            if len(tmprepos)>=1:
                tmprepos.pop(0)
            tmprepos = ['https://'+x for x in tmprepos]
            oldgenrepos = [get_project_repo_from_stash_url(x) for x in tmprepos]

            deletedrepos = set(oldgenrepos) - set(newgenrepos)
            for deletedrepo in list(deletedrepos):
                delete_repo(deletedrepo[0],deletedrepo[1],stash_user,stash_password)
        except:
            print("Something wrong with the matchings")