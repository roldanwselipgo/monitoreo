#!/bin/bash                       
# Gerardo Ocampos       

dir=$(echo $PWD)

$dir/venv/bin/python collector.py > custom-exporter-$(date +"%m-%d-%Y").log 2>&1 &
