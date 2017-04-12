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

def createBatchFileGPU(singleCommand):
    with open("hyperOptScriptGPU.sh", "rt") as fin:
        with open("hyperOptScriptExecuteGPU.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)

workerCount = 1000
ip=sys.argv[1]

createBatchFile("srun --ntasks=1 --time=01:00:00 --mem=3900 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip)
createBatchFileGPU("srun --time=01:00:00 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip)

for i in range(1, workerCount):
    p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    p = subprocess.Popen("sbatch hyperOptScriptExecuteGPU.sh", stdout=log, stderr=log, shell=True)


    if workerCount > 200:
        st = 0.4
    else:
        st = 3

    time.sleep(st)

while 1:
    hold=1
