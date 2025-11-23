#!/bin/bash
set -e
if [ -z "$1" ]; then echo 'Usage: restore_db.sh backups/file.db'; exit 1; fi
cp $1 quantumapex.db
echo 'Restored' 
