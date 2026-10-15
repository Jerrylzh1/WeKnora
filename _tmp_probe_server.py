import os
import sys
import io

if hasattr(sys.stdout, "buffer") and sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = (len(sys.argv) > 1 and sys.argv[1]) or os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=60)

    cmds = [
        ("=== /data 目录 ===",
         "ls -la /data/ | grep -i weknora"),
        ("=== 当前运行的 weknora 容器与镜像 ===",
         "docker ps --format '{{.Names}}\\t{{.Image}}\\t{{.Status}}' | grep -i weknora"),
        ("=== 0.8.3 镜像是否已拉取 ===",
         "docker images | grep -iE 'weknora|wechatopenai' | head -20"),
        ("=== 0.6.0 compose frontend 段 ===",
         "cd /data/WeKnora-0.6.0 && grep -n -A4 '^  frontend:' docker-compose.yml 2>/dev/null"),
        ("=== 是否有 0.8.x compose 目录 ===",
         "ls -d /data/WeKnora-0.8* 2>/dev/null || echo '无 0.8.x 目录'"),
    ]
    for title, cmd in cmds:
        print("==== " + title + " ====")
        stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err.strip():
            print("STDERR:", err)
        print()
    client.close()


if __name__ == "__main__":
    main()
