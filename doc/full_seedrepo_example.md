Full seedrepo definition
=======================

Follows a full json definition with all possible options for a single job. It
is not common for the jobs to have so many options, as you can easily see from
the templates directory.

```
[
  {
    "project": "project-name" ,
    "repository": "repository-name" | ["repo1","repo2",...],
    "jenkins_hook": true | false,
    "archived": true | false,
    "forked_from": {
      "project": "project1",
      "repository": "repository1",
      "sync": false | true
    },
    "additional_branches": [
      "branch1",
      "branch2"
    ],
    "userpermissions": [
      {
        "user": "user1",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      },
      {
        "user": "user1",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      }
    ],
    "grouppermissions": [
      {
        "group": "group1",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      },
      {
        "group": "group2",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      }      
    ],
    "branchpermissions": [
      {
        "groups": ["group1","group2",...],
        "users": ["user1","user2",....],
        "branch": "branch1"
      },
      {
        "users": ["user1","user2",....],
        "pattern": "pattern1"
      }
    ]
  }
]
```