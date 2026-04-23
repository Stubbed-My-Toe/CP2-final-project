import subprocess,sys
try:
    subprocess.check_call([sys.executable,"-m","pip","install","-r","requirements.txt"])
except Exception as e:
    print(f"some error happen {e}")
    raise e