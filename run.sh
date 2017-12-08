git add . && git pull && git commit -m "fastupload"  && git push
ssh -tX s2071275@login2.zih.tu-dresden.de 'ssh -tX s2071275@taurus.hrsk.tu-dresden.de "source ~/.bashrc;source ~/.profile;
cd pythonProjects/tf_rnn;git stash;git pull; sh preInit.sh;
~/pythonProjects/env/bin/python2.7 ~/pythonProjects/tf_rnn/parallelExecutor.py"'
