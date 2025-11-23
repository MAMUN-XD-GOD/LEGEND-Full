#!/bin/bash
set -e
DB=quantumapex.db
OUT=backups/quantumapex-$(date +%Y%m%d-%H%M%S).db
mkdir -p backups
cp $DB $OUT
echo "Backed up to $OUT"
