import subprocess
import time
import sys

log = open("logs/startWorker.log", "w")

def createBatchFile(singleCommand):
    with open("hyperOptScript.sh", "rt") as fin:
        with open("hyperOptScriptExecute.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)

workerCount = 1000
ip=sys.argv[1]

createBatchFile("srun --time=02:00:00 --mem=2000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip)

for i in range(1, workerCount):
    p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    time.sleep(0.5)

while 1:
    hold=1
