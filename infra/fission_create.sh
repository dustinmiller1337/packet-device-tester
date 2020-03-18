#!/bin/bash
fission env create --name python --image fission/python-env --builder fission/python-builder
rm -rf db_inserter.zip
zip -jr db_inserter.zip db_inserter/
fission pkg create --name db-inserter-pkg --src db_inserter.zip --env python --buildcmd "./build.sh"
fission fn create --name db-inserter-fn --pkg db-inserter-pkg --entrypoint "db_inserter.main"
fission route create --name db-inserter-route --method POST --url /insert --function db-inserter-fn
