git add . && git commit -m "fastupload"  && git push
ssh -tX s2071275@login2.zih.tu-dresden.de 'ssh -tX s2071275@taurus.hrsk.tu-dresden.de "source ~/.bashrc;source ~/.profile;
cd pythonProjects/tf_rnn;git stash;git pull; scancel -u s2071275; sbatch ~/pythonProjects/tf_rnn/HyperoptStartWorkerJob.sh"'
