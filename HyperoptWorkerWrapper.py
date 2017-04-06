import subprocess
import time
import sys
ip = sys.argv[1]
log = open('logs/hyperoptWorker.log', 'w')

workerCommand= 'source ~/pythonProjects/tf_rnn/preInit.sh ; source ~/pythonProjects/env/bin/activate; hyperopt-mongo-worker --mongo='+ip+':27017/foo_db --poll-interval=0.1'
print workerCommand
p = subprocess.Popen(workerCommand, stdout=log, stderr=log, shell=True)

