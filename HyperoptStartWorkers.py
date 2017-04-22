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
ipLog = open("logs/ip.log", "w")
ipLog.write(ip)
ipLog.close()
#backup: cp -ar /lustre/ssd/s2071275/mongo ~/mongo/mongodb/mongodb-linux-x86_64-3.4.2/data/db
startDB = "ulimit -u 100000 && mongod --dbpath /lustre/ssd/s2071275/mongo/db"
startOptimizer = "ulimit -u 100000 && source ../env/bin/activate; python HyperoptOptimizer.py "+ip
#foo = Popen("source the_script.sh", shell=True, executable="/bin/bash")
#createBatchFile("srun --time=12:00:00 --mem-per-cpu=10000 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/hyperoptSpamWorkers.py "+ip)


pMongo = subprocess.Popen(startDB, stdout=logDB, stderr=logDB, shell=True, preexec_fn=os.setsid)
pOpti = subprocess.Popen(startOptimizer, stdout=log, stderr=log, shell=True, preexec_fn=os.setsid)
p = subprocess.Popen("cp hyperoptArrayTemplate.sh logs/cache/hyperoptArrayTemplate.sh && cp HyperoptWorkerWrapper.sh logs/cache/HyperoptWorkerWrapper.sh && cd logs/cache/ && rm -rf logs/arr/*pu* && sbatch hyperoptArrayTemplate.sh "+ip, stdout=log, stderr=log, shell=True)
p = subprocess.Popen("cp hyperoptArrayTemplateGPU.sh logs/cache/hyperoptArrayTemplateGPU.sh && cd logs/cache/ && sbatch hyperoptArrayTemplateGPU.sh "+ip, stdout=log, stderr=log, shell=True)

start_time = time.time()
while 1:
    exec_time = time.time()-start_time
    if exec_time > 7600:
        os.killpg(os.getpgid(pMongo.pid), signal.SIGTERM)
        os.killpg(os.getpgid(pOpti.pid), signal.SIGTERM)
        log.write(str(time.time())+'kill db process\n')  # python will convert \n to os.linesep

        time.sleep(60)
        pMongo = subprocess.Popen(startDB, stdout=logDB, stderr=logDB, shell=True, preexec_fn=os.setsid)
        pOpti = subprocess.Popen(startOptimizer, stdout=log, stderr=log, shell=True, preexec_fn=os.setsid)
        start_time = time.time()
        log.write(str(time.time()) + 'restart\n')
    time.sleep(60)

