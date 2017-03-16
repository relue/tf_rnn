import modelKeras
import json
import subprocess
import logging
import sys
logging.basicConfig(filename='parallelExecDetail.log',level=logging.DEBUG)
pre = subprocess.Popen("sh ~/pythonProjects/tf_rnn/preInit.sh ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

data=json.loads(sys.argv[1])
logging.warning('command'+sys.argv[1])
modelOut = modelKeras.kerasModel(**data)
