# Grouppermissions (node)

## Description
Add Group-Specific repo access permissions

Add them as a list of dictionaries that will contain
the user and the permission for each user

Values for permissions are

REPO_ADMIN
REPO_WRITE
REPO_READ

## Definition 

```
"grouppermissions" : ]
      {
        "group": "group1",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      },
      {
        "group": "group2",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      }

]
```