#!/bin/bash
## with Tensorflow
module purge
module load modenv/eb
module load Keras
module load tensorflow
# if you see 'broken pipe error's (might happen in interactive session after the second srun command)
module load h5py/2.6.0-intel-2016.03-GCC-5.3-Python-3.5.2-HDF5-1.8.17-serial

export KERAS_BACKEND=tensorflow      # configure Keras to use tensorflow

srun python singleExecution.py "{\"indexID\": 2}" 1
