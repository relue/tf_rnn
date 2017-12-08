git add . && git pull && git commit -m "fastupload"  && git push
ssh -tX s2071275@login2.zih.tu-dresden.de 'ssh -tX s2071275@taurus.hrsk.tu-dresden.de "source ~/.bashrc;source ~/.profile;
cd pythonProjects/tf_rnn;git stash;git pull; sbatch ~/pythonProjects/tf_rnn/php5tf.sh"'
