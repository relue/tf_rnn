#!/bin/bash
ls -rt *pu-* | shuf | xargs cat >> cpuLog
grep "no job" cpuLog | wc -l
grep "finished" cpuLog | wc -l