Creating a new repo
==================
Creating a new repo is simply perfomed by adding a new json file to the templates
folder of seed-job, or modifying an existing one.


Process
=======

1. Clone the repository
2. Create a branch for your feature request with `git checkout -b <branch-name>`
3. Modify the desired template or create a new one!
4. Run your json file through a json validator.  [You have various options to do so](json_validate.md).
5. Commit `git commit -m "<commit-message>"`
6. Perform a push to create the remote branch `git push origin <branch-name>`
7. Perform the pull request and wait for the approval


Documentation
=============
A good start is to simply copy one of the existing templates and adapt it to 
your project.

Full documentation on the different nodes accepted by seed-repo JSON can be
found in the root [Syntax document](seedrepo_syntax.md)