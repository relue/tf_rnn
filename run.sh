git add . && git commit -m "fastupload"  && git push
ssh -tX s2071275@login2.zih.tu-dresden.de 'ssh -tX s2071275@taurus.hrsk.tu-dresden.de "source ~/.bashrc;source ~/.profile;cd pythonProjects/tf_rnn;git pull;sh ~/pythonProjects/tf_rnn/init.sh ~/pythonProjects/tf_rnn/finalRNN.py 1"'
