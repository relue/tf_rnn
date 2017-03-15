import modelKeras
import json
import subprocess

pre = subprocess.Popen("~/pythonProjects/tf_rnn/preInit.sh ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

data=json.loads(argv[1])
modelOut = modelKeras.kerasModel(**data)
