# Validating your JSON

Before sending any JSON for a pull request we kindly ask that this JSON
is previously validated.


## Git hooks

The most practical way to check the jsons is to set up a git hook to do so.

Activate the pre-commit hook

```
   mv .git/hooks/pre-commit.sample .git/hooks/pre-commit
```

And modify it to check for the changed JSON files. Add this code snippet
at the beginning of the file. This assumes that python is installed
in your system

```
LIST=$(git diff-index --cached --name-only --diff-filter=ACMR HEAD)
for file in $LIST
do
    extension="${file##*.}"
    if [ $extension = "json" ];
    then
        OUTPUT=$(python -mjson.tool ${file})
        ERR=$?
        if [ $ERR -ne 0 ];
        then
            echo $file " - invalid json"
            exit $ERR
        fi
    fi
done
```

This commit hook will check the committed files and block the commit
in case that one of the JSON files is invalid.

## online validators

Just copy paste your json file to an online validator like [jsonlint](http://jsonlint.com/)