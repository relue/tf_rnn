import subprocess
import time
import sys
ip = '172.24.32.17'
sys.stdout = open('~/pythonProjects/tf_rnn/hyperoptWorker.log', 'wt')
sys.stderr = open('~/pythonProjects/tf_rnn/hyperoptWorker.log', 'wt')

workerCommand= 'source ~/pythonProjects/tf_rnn/preInit.sh ; source ~/pythonProjects/env/bin/activate; hyperopt-mongo-worker --mongo='+ip+':27017/foo_db --poll-interval=0.1'
print workerCommand
p = subprocess.Popen(workerCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
for line in p.stdout:
    print line
p.wait()
print p.returncode
