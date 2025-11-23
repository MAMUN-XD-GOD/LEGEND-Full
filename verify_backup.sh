#!/bin/bash
set -e
LATEST=$(ls -1 backups | tail -n1)
if [ -z "$LATEST" ]; then echo 'No backups'; exit 1; fi
file=backups/$LATEST
echo 'Verifying' $file
sqlite3 $file 'SELECT count(*) FROM candles;' || echo 'DB corrupt?'
