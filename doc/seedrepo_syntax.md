#Seed repo Syntax
Each json file defines one or more stash reposiroties. The json file must be either
a list of seedjob definitions (as a json map)



```
[
  {<node> : <def>, ...}
  {<node> : <def>, ...}
  ...
]
```

## Seed-job job nodes
This is the list of commonly used nodes to generate jobs.

* [project](node_project.md)                project name where it will be created
* [repository](node_repository.md)          repository name 
* [jenkins_hook](node_type.md)              do you want jenkins hook on? ( you will still need to put SCM option ON at jenkins and put a comment on the schedule )
* [archived](node_archived.md)              do you to archive this repo¿?
* [additional_branches](node_branches.md)        create other branches aside of master branch
* [forked_from](node_forked.md)                Fork from another repo?
* [userpermissions](node_userperms.md)     User-Specific Permissions
* [grouppermissions](node_groupperms.md)         Group Specific Permissions
* [branchpermissions](node_branchperms.md)        Branch Permissions

