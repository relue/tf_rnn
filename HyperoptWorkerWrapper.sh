source ~/pythonProjects/tf_rnn/preInit.sh ; source ~/pythonProjects/env/bin/activate; hyperopt-mongo-worker --reserve-timeout=10 --mongo=$1:27017/foo_db --poll-interval=10
