import subprocess
import time
import sys

log = open("logs/startWorker.log", "w")

def createBatchFile(singleCommand, com2):
    with open("hyperOptScript.sh", "rt") as fin:
        with open("hyperOptScriptExecute.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)
        with open("hyperOptScriptExecuteFill.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', com2)
                fout.write(line)

def createBatchFileGPU(singleCommand, com2):
    with open("hyperOptScriptGPU.sh", "rt") as fin:
        with open("hyperOptScriptExecuteGPU.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)
        with open("hyperOptScriptExecuteGPUFill.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', com2)
                fout.write(line)

workerCount = 5000
#ip=sys.argv[1]
ip="127"
comLong = "srun --ntasks=1 --time=12:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
comFast = "srun --ntasks=1 --time=01:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
createBatchFile(comLong,comFast)
comLongGPU = "srun --gres=gpu:1 --time=12:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
comFastGPU = "srun --gres=gpu:1 --time=01:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
createBatchFileGPU(comLongGPU, comFastGPU)

for i in range(1, workerCount):
    p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    p = subprocess.Popen("sbatch hyperOptScriptExecuteFill.sh", stdout=log, stderr=log, shell=True)
    p = subprocess.Popen("sbatch hyperOptScriptExecuteGPU.sh", stdout=log, stderr=log, shell=True)
    p = subprocess.Popen("sbatch hyperOptScriptExecuteGPUFill.sh", stdout=log, stderr=log, shell=True)


    if workerCount > 100:
        st = 0.5
    else:
        st = 4

    time.sleep(st)

while 1:
    hold=1
