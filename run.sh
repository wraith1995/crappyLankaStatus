#!/bin/bash
cd /home/teoc/crappyLankaStatus
NAME=`date +%d%m%y`
python3 /home/teoc/crappyLankaStatus/report.py > $NAME".json"
cp $NAME".json" "status.json"
git add $NAME".json" status.json
sleep 5
git commit -m "${NAME}.json"
sleep 5
#ssh-agent bash -c 'ssh-add /home/teoc/id;  git push'
GIT_SSH_COMMAND='ssh -i /home/teoc/id -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' git push
