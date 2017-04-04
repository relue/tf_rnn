import subprocess
import time
ip = '172.24.32.17'
log = open("hyperoptWorker.log", "w")
workerCommand= 'source ~/pythonProjects/tf_rnn/preInit.sh ; hyperopt-mongo-worker --mongo='+ip+':27017/foo_db --poll-interval=0.1'

p = subprocess.Popen(workerCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
for line in p.stdout:
    print line
p.wait()
print p.returncode
