# coding=utf-8
import stashy
from fabric.api import task, settings, local
from git import Repo

from config import JENKINS_URL


class StashyManagment():
    def __init__(self, user, password, url="https://scm.scytl.net/stash/"):
        self.stash_server = stashy.connect(url, user, password)

    def is_permission_valid(self, permission):
        valid_permissions = ['REPO_ADMIN','REPO_WRITE','REPO_READ']
        if permission in valid_permissions:
            return True
        else:
            return False

    def update_hook_repo(self, project_name, repo_name, sshurl, enable=True):
        repohook = self.stash_server.projects[project_name].repos[
            repo_name].settings.hooks[
            'com.nerdwin15.stash-stash-webhook-jenkins:jenkinsPostReceiveHook']

        config = {"jenkinsBase": JENKINS_URL,
                  "gitRepoUrl": sshurl,
                  "ignoreCerts": True,
                  "omitHashCode": False,
                  "ignoreCommitters": "",
                  "branchOptions": "",
                  "branchOptionsBranches": ""}

        repohook.configure(config)
        if enable:
            repohook.enable()
        else:
            repohook.disable()

    def update_branch_permissions(self,project_name,repo_name,
                                  branch_permissions):

        newrepo = self.stash_server.projects[project_name].repos[
            repo_name]
        for entry in newrepo.branch_permissions.restricted.list():
            newrepo.branch_permissions.restricted.__getitem__('%s'% entry['id']).delete()
        for branch_perm in branch_permissions:
            users = branch_perm['users'] if 'users' in branch_perm else None
            groups = branch_perm['groups'] if 'groups' in branch_perm else None
            pattern = True if 'pattern' in branch_perm else False
            value = branch_perm['pattern'] if 'pattern' \
                                                              in \
                                                 branch_perm else \
                "refs/heads/%s" % branch_perm['branch']
            newrepo.branch_permissions.restricted.create(value,
                users=users, groups=groups, pattern=pattern)

    def update_group_permissions(self,project_name,repo_name,
                                  group_permissions):
        newrepo = self.stash_server.projects[project_name].repos[
                  repo_name]
        ## Clean Old Data
        for permission in newrepo.repo_permissions.groups.list():
            newrepo.repo_permissions.groups.revoke(
                permission['group']['name'])
        for group_perm in group_permissions:
            if self.is_permission_valid(group_perm['permission']):
                newrepo.repo_permissions.groups.grant(group_perm[
                    'group'], group_perm['permission'])
                
    def update_user_permissions(self,project_name,repo_name,
                                  user_permissions):
        newrepo = self.stash_server.projects[project_name].repos[
                  repo_name]
        ## Clean Old Data
        for permission in newrepo.repo_permissions.groups.list():
            newrepo.repo_permissions.groups.revoke(
                newrepo.repo_permissions.users
            .list()[0]['user']['name'])
        for user_perm in user_permissions:
            if self.is_permission_valid(user_perm['permission']):
                newrepo.repo_permissions.users.grant(user_perm[
                    'user'], user_perm['permission'])


    def start_and_init_repo(self,project_name,repo_name,
                            stash_user,stash_password, fork=None, sync=False):

        if not fork:
            self.stash_server.projects[project_name].repos.create(repo_name)
        else:
            self.stash_server.projects[fork['project']].repos[fork['repository']].fork(repo_name,project_name)
            self.stash_server.projects[project_name].repos[repo_name].update_sync(sync)
        newrepo = self.stash_server.projects[project_name].repos[repo_name]

        ## get http clone url

        repourl = newrepo.get()['links']['clone'][0]['href'].encode('ascii')

        ## Initialize it..

        ## patch url with password
        urlwithpwd = repourl.replace(stash_user,
                                     stash_user+':'+stash_password,1)
        with settings(warn_only=True):
            local("rm -rf /tmp/%s" % repo_name)
            local("mkdir /tmp/%s" % repo_name)
        localrepo = Repo.clone_from(urlwithpwd, '/tmp/'+repo_name)
        open('/tmp/'+repo_name+'/'+'.gitignore', 'wb').close()
        localrepo.index.add(['.gitignore'])
        localrepo.index.commit("[Automatic Generated Initial Commit by "
                               "RepoGen]")
        localrepo.remotes['origin'].push(localrepo.head)

        ## Now create additional branch and give permissions to hudson

        newrepo.repo_permissions.users.grant('hudson','REPO_WRITE')

    def create_branches(self,project_name,repo_name,
                            branch_list):
        newrepo = self.stash_server.projects[project_name].repos[repo_name]
        branchlist = [x['displayId'].encode('ascii') for x in newrepo.branches()]
        todelete = set(branchlist) - set(branch_list) - set(['master'])

        for deleting in todelete:
            newrepo.delete_branch(deleting)
        for branch in branch_list:
            if branch not in branchlist:
                newrepo.create_branch(branch)

    def archive_repo(self,project_name,repo_name,
                            ):
        newrepo = self.stash_server.projects[project_name].repos[repo_name]

        newrepo.move("AR")

    def unarchive_repo(self,project_name,repo_name,
                            ):
        newrepo = self.stash_server.projects['AR'].repos[repo_name]

        newrepo.move(project_name)

    def delete_repo(self,project_name,repo_name,
                            ):
        getrepo = self.stash_server.projects[project_name].repos[repo_name]
        getrepo.delete()