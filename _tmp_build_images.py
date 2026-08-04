import os
import paramiko
import time

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def ssh_exec(client, cmd, timeout=60):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode(), stderr.read().decode()


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    # 触发后台 build：打独立 tag 0.7.1-dev，避免覆盖现有 latest(0.6.0)
    trigger = (
        "cd /data/WeKnora-build && "
        "export WEKNORA_VERSION=0.7.1-dev && "
        "nohup docker compose build app frontend docreader sandbox "
        "> /data/build-0.7.1.log 2>&1 & "
        "echo \"build pid started\"; sleep 3; "
        "tail -5 /data/build-0.7.1.log"
    )
    out, err = ssh_exec(client, trigger, timeout=60)
    print("=== TRIGGER ===")
    print(out)
    if err.strip():
        print("STDERR:", err)

    client.close()
    print("done-trigger")


if __name__ == "__main__":
    main()
