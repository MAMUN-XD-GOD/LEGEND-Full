#!/bin/bash
set -e
DAYS=${1:-30}
find backups -type f -mtime +$DAYS -delete
echo 'Rotated backups older than' $DAYS 'days'
