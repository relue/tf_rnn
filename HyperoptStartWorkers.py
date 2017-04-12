import subprocess
import time
import socket
import os
import signal
import subprocess


def createBatchFile(singleCommand):
    with open("hyperOptScript.sh", "rt") as fin:
        with open("hyperOptScriptMain.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip=s.getsockname()[0]
s.close()

log = open("logs/main.log", "w")
logDB = open("logs/mongo.log", "w")

startDB = "mongod --dbpath ~/mongo/mongodb/mongodb-linux-x86_64-3.4.2/data/db"
startOptimizer = "source ../env/bin/activate; python HyperoptOptimizer.py "+ip

createBatchFile("srun --time=12:00:00 --mem=10000 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/hyperoptSpamWorkers.py "+ip)


pMongo = subprocess.Popen(startDB, stdout=logDB, stderr=logDB, shell=True, preexec_fn=os.setsid)
pOpti = subprocess.Popen(startOptimizer, stdout=log, stderr=log, shell=True, preexec_fn=os.setsid)
p = subprocess.Popen("sbatch hyperOptScriptMain.sh", stdout=log, stderr=log, shell=True)

start_time = time.time()
while 1:
    exec_time = time.time()-start_time
    if exec_time > 1800:
        os.killpg(os.getpgid(pMongo.pid), signal.SIGTERM)
        os.killpg(os.getpgid(pOpti.pid), signal.SIGTERM)
        time.sleep(30)
        pMongo = subprocess.Popen(startDB, stdout=logDB, stderr=logDB, shell=True, preexec_fn=os.setsid)
        pOpti = subprocess.Popen(startOptimizer, stdout=log, stderr=log, shell=True, preexec_fn=os.setsid)
        start_time = time.time()
    time.sleep(60)

