# Branchpermissions (node)

## Description
Add Branch-Specific repo access permissions

Add them as a list of dictionaries that will contain
the users and groups and the branch or the users/groups and a pattern

## Definition 

```
"userpermissions" : ]
      {
        "groups": ["group1"],
        "users": ["user1"],
        "branch": "master"
      },
      {
        "users": ["user1"],
        "groups": ["group1"]
        "pattern": "pattern1"
      }

]
```