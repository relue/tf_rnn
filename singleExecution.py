import modelKeras
import json
import subprocess
import logging
logging.basicConfig(filename='parallelExecDetail.log',level=logging.DEBUG)
pre = subprocess.Popen("sh ~/pythonProjects/tf_rnn/preInit.sh ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

data=json.loads(argv[1])
modelOut = modelKeras.kerasModel(**data)
