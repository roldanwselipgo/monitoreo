#!/bin/bash                       

dir=$(echo $PWD)

$dir/../celery_exporter/exp/bin/python3 ../celery_exporter/collector.py 
