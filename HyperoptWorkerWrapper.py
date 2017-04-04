import subprocess

ip = '172.24.32.17'
log = open("hyperoptWorker.log", "w")
workerCommand= 'hyperopt-mongo-worker --mongo='+ip+':27017/foo_db --poll-interval=0.1'

p = subprocess.Popen(workerCommand, stdout=log, stderr=log, shell=True)

