#!/bin/bash
rm -rf db_inserter.zip
zip -jr db_inserter.zip db_inserter/
fission pkg update --name db-inserter-pkg --src db_inserter.zip
fission pkg info --name db-inserter-pkg
