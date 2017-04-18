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

    with open("hyperOptScript.sh", "rt") as fin:
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

    with open("hyperOptScriptGPU.sh", "rt") as fin:
        with open("hyperOptScriptExecuteGPUFill.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', com2)
                fout.write(line)

workerCount = 3000
ip=sys.argv[1]
comLong = "srun --ntasks=1 --time=06:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
comFast = "srun --ntasks=1 --time=06:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
#comMid1 = "srun --ntasks=1 --time=03:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
#comMid2 = "srun --ntasks=1 --time=06:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
createBatchFile(comLong,comFast)
comLongGPU = "srun --time=12:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
comFastGPU = "srun --time=06:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip
createBatchFileGPU(comLongGPU, comFastGPU)
limitHigh= "ulimit -u 30000 "
p = subprocess.Popen("ulimit -u 10000", stdout=log, stderr=log, shell=True)
for i in range(1, workerCount):
    #p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    p = subprocess.Popen("sbatch hyperOptScriptExecuteFill.sh", stdout=log, stderr=log, shell=True)
    #p = subprocess.Popen("sbatch hyperOptScriptExecuteGPU.sh", stdout=log, stderr=log, shell=True)
    if i % 50 == 0:
        p = subprocess.Popen("sbatch hyperOptScriptExecuteGPUFill.sh", stdout=log, stderr=log, shell=True)
    if i % 10 == 0:
        p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    if i < 8000:
        st = 0.3
    else:
        st = 30

    time.sleep(st)

while 1:
    hold=1
