source ~/pythonProjects/tf_rnn/preInit2.sh ; source ~/pythonProjects/env/bin/activate; hyperopt-mongo-worker --max-jobs=10000 --max-consecutive-failures=10000 --reserve-timeout=50000 --mongo=$1:27017/foo_db --poll-interval=60
