# coding=utf-8
from jenkinsapi.jenkins import Jenkins
from urlparse import urlparse
from xml.etree import ElementTree as ET
from config import JENKINS_JOB


class JenkinsManagment(Jenkins):
    def update_stash_config(self, job):
        print("Updating %s job" % job)
        if not job.is_enabled():
            return
        xml_instance = ET.fromstring(job.get_config())
        gitconfig = xml_instance.find('.//hudson.plugins.git.UserRemoteConfig')
        if gitconfig is not None:
            triggers = xml_instance.find('triggers')
            if triggers is not None:
                scmtrigger = triggers.find('hudson.triggers.SCMTrigger')
                if scmtrigger is not None:
                    specs = scmtrigger.find('spec')
                    if specs is not None:
                        specs.text = ""
                    else:
                        spec = ET.Element("spec")
                        scmtrigger.append(spec)
                else:
                    newel = ET.Element("hudson.triggers.SCMTrigger")
                    pch = ET.Element("ignorePostCommitHooks")
                    pch.text = 'false'
                    spec = ET.Element("spec")
                    newel.append(pch)
                    newel.append(spec)
                    triggers.append(newel)

                newxmlstring = ET.tostring(xml_instance)
                job.update_config(newxmlstring)
                url_text = xml_instance.find('.//hudson.plugins.git.UserRemote'
                                             'Config//url').text
                url_parsed = urlparse(url_text).path.split('/')[1:]
                return [url_parsed[0], url_parsed[1].rstrip('git').rstrip(
                    "."),url_text,True]

    def get_stash_config(self, job):
        try:
            print("Fetching %s job" % job)
            xml_instance = ET.fromstring(job.get_config())
            gitconfig = xml_instance.find('.//hudson.plugins.git.UserRemoteConfig')
            if gitconfig is not None:
                triggers = xml_instance.find('triggers')
                if triggers is not None:

                    url_text = xml_instance.find('.//hudson.plugins.git.UserRemote'
                                                 'Config//url').text
                    branches = xml_instance.find('.//branches')
                    branchlist = []
                    for branch in branches:
                        branchlist.append(branch.find('name').text)
                    url_parsed = urlparse(url_text).path.split('/')[1:]
                    return [job, url_parsed[0], url_parsed[1].rstrip('git').rstrip(
                        "."),url_text, branchlist]
        except:
            print("No Api Found")
            return

    def get_last_build_console(self):
        try:
            console = self.get_job(JENKINS_JOB).get_last_build().get_console()
        except:
            return ""
        return console


    def update_stash_config_all_jobs(self):
        return_list = []
        for job in self.get_jobs_list():
            try:
                job2add = self.get_job(job)
                return_list.append(self.update_stash_config(job2add))
            except:
                print("ApiError for job %s" % job)
        return return_list

    def get_stash_config_all_jobs(self):
        return_list = []
        for job in self.get_jobs_list():
            try:
                job2add = self.get_job(job)
                return_list.append(self.get_stash_config(job2add))
            except:
                print("ApiError for job %s" % job)
        return return_list

    def update_stash_config_list_jobs(self, jobs_list):
        updated_jobs_list = self.get_jobs_list()
        return_list = []
        for job in self.get_jobs_list():
            try:
                job2add = self.get_job(job)
                if job in updated_jobs_list:
                    return_list.append(self.update_stash_config(job2add))
            except:
                print("ApiError for job %s" % job)
        return return_list

    def update_stash_config_pattern_jobs(self, pattern):
        updated_jobs_list = self.get_jobs_list()
        filtered_job_list = [item for item in updated_jobs_list if pattern
                             in item ]
        return_list = []
        for job in filtered_job_list:
            try:
                job2add = self.get_job(job)
                if job in updated_jobs_list:
                    return_list.append(self.update_stash_config(job2add))
            except:
                print("ApiError for job %s" % job)
        return return_list
