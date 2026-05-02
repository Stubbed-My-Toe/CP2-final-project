import subprocess,sys
try:
    subprocess.check_call([sys.executable,"-m","pip","install","-r","requirements.txt"])
except:
    pass
try:
    subprocess.check_call([sys.executable,"-m","pip3","install","-r","requirements.txt"])
except Exception as e:
    pass