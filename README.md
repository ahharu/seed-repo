Seed Repo
========
Seed-repo is a script used to automatically generate stash repositories
according to a set of JSON files.

* [Creating a new repository](doc/new_repo.md)
* [Seed-Repo JSON syntax](doc/seedrepo_syntax.md)

On config.py configure which is the job that will run this scripts. It is used to
get the information from last run and compare for changes in repo configs

Also the Jenkins and Stash URLs , it is important!

For Jenkins Password, use the Token

You will need a jenkins job that does

* fab -f ${WORKSPACE}/update_stash.py update_all_from_templates

and this variables

* stash_username
* stash_password

It supports

* Creating Repository
* Branches
* Branches Permissions
* Repository Permissions
* Moving Repositories
* Deleting Repositories
* Forking from a repository
* Archive repository ( Move to repository with codename 'AR' )
* Activating Jenkins Hook

Other
-----

* [Full JSON definition](doc/full_seedrepo_example.md)


