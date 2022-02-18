#!/bin/bash
sreport user top  -t percent -p -n start=$1 end=$2 | awk -F "|" '{print $2, $5}'  > log
