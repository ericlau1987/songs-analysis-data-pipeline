# songs-analysis-data-pipeline

https://github.com/viirya/eventsim
https://mimesis.name/master/

#TODO: update github passkey - Done
#TODO: set a principal iam role for the project on aws - Done
#TODO: prepare terraform - in progress
#TODO: prepare github actions to automate the whole deployment to dev/prod
#TODO: prepare makefile
#TODO: set the cursor the left bar same as vscode - Done


# Installation
## pre-commit

```
pip install pre-commit
```

prepare the config at `.pre-commit-config.yaml`
```
pre-commit run --all-files
```

streaming data
https://github.com/viirya/eventsim/blob/master/README.md

run the streaming data in streaming folder
```
sh ./spark-submit.sh pyspark_consumer.py --topic auth_events
```
