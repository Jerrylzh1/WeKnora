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
        "echo '--- frontend/dist 是否存在 ---'; "
        "ls -la /data/WeKnora-build/frontend/dist 2>&1 | head; "
        "echo '--- compose frontend build 配置 ---'; "
        "grep -nA8 'frontend:' /data/WeKnora-build/docker-compose.yml | head -30; "
        "echo '--- 当前 build 日志 ---'; "
        "tail -10 /data/build-frontend.log"
    )
    stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("STDERR:", err)
    client.close()


if __name__ == "__main__":
    main()
