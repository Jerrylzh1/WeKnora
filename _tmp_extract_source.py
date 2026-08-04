import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def run(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out, err


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    cmd = (
        "cd /data/WeKnora-build && "
        "tar xzf /data/weknora-dev.tar.gz && "
        "echo '--- 解压后顶层目录 ---' && "
        "ls -a && "
        "echo '--- 关键文件存在性 ---' && "
        "ls -l docker-compose.yml docker/Dockerfile.app frontend/Dockerfile 2>&1 && "
        "echo '--- 复用原 .env ---' && "
        "cp /data/WeKnora-0.6.0/.env /data/WeKnora-build/.env && "
        "echo 'env copied' && "
        "grep -c '' /data/WeKnora-build/.env"
    )
    out, err = run(client, cmd)
    print(out)
    if err.strip():
        print("STDERR:", err)
    client.close()
    print("done")


if __name__ == "__main__":
    main()
