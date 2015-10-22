# Userpermissions (node)

## Description
Add User-Specific repo access permissions

Add them as a list of dictionaries that will contain
the user and the permission for each user

Values for permissions are

REPO_ADMIN
REPO_WRITE
REPO_READ

## Definition 

```
"userpermissions" : ]
      {
        "user": "user1",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      },
      {
        "user": "user2",
        "permission": "REPO_ADMIN" | "REPO_WRITE" | "REPO_READ"
      }

]
```