import modelKeras
import json

data=json.loads(argv[1])
modelOut = modelKeras.kerasModel(**data)
