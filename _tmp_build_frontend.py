import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    # 单独 build frontend（基础镜像 nginx alpine digest，绕过 node:20-slim 限流）
    cmd = (
        "cd /data/WeKnora-build && export WEKNORA_VERSION=0.7.1-dev && "
        "nohup docker compose build frontend > /data/build-frontend.log 2>&1 & "
        "echo started; sleep 15; tail -12 /data/build-frontend.log"
    )
    stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("STDERR:", err)
    client.close()


if __name__ == "__main__":
    main()
