#!/usr/bin/env bash
git add . && git commit -m "fastupload"  && git pull && git push
ssh -tX s2071275@login2.zih.tu-dresden.de 'ssh -tX s2071275@taurus.hrsk.tu-dresden.de "source ~/.bashrc;source ~/.profile;
cd pythonProjects/tf_rnn;git stash;git pull;"'