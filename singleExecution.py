import modelKeras
import json

import logging
import sys
logging.basicConfig(filename='parallelExecDetail2.log',level=logging.DEBUG)


data=json.loads(sys.argv[1])
logging.warning('command'+sys.argv[1])
modelOut = modelKeras.kerasModel(**data)
