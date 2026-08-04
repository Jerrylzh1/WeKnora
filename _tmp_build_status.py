import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)
    cmd = (
        "echo '--- build 进程 ---'; "
        "pgrep -af 'docker compose build' | head; "
        "echo '--- 日志末尾 ---'; "
        "tail -15 /data/build-0.7.1.log 2>/dev/null; "
        "echo '--- 已出镜像 ---'; "
        "docker images --format '{{.Repository}}:{{.Tag}}\\t{{.CreatedSince}}' | grep 0.7.1-dev"
    )
    stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("STDERR:", err)
    client.close()


if __name__ == "__main__":
    main()
