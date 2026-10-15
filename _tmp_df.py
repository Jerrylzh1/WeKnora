import sys, io
if hasattr(sys.stdout, "buffer") and sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import paramiko
HOST = "10.56.5.140"; USER = "root"
PASSWORD = (len(sys.argv) > 1 and sys.argv[1]) or input("pass: ")
c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PASSWORD, timeout=60)
for cmd in ["df -h /data", "echo '--- backup size ---'; du -sh /data/backup/*"]:
    o, e = c.exec_command(cmd, timeout=60)[1], c.exec_command(cmd, timeout=60)[2]
    print(o.read().decode()); 
    err = e.read().decode()
    if err.strip(): print("ERR", err)
c.close()
