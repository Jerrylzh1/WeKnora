import sys
import io

if hasattr(sys.stdout, "buffer") and sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = (len(sys.argv) > 1 and sys.argv[1]) or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=60)

    cmds = [
        ("=== /data/weknora 目录 ===",
         "ls -la /data/weknora/"),
        ("=== compose 文件名 ===",
         "ls /data/weknora/*compose* /data/weknora/*.yml /data/weknora/*.yaml 2>/dev/null"),
        ("=== docker volume ls (weknora) ===",
         "docker volume ls | grep -i weknora"),
        ("=== 当前 compose 全部服务与镜像 ===",
         "cd /data/weknora && docker compose config --services 2>/dev/null; echo '--- images ---'; cd /data/weknora && docker compose images 2>/dev/null"),
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
