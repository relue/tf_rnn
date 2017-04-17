import subprocess

p = subprocess.Popen("sh update.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in iter(p.stdout.readline, ''): print line,
retval = p.wait()

