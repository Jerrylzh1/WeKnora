import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")

LOCAL = r"d:/weknora-dev.tar.gz"
REMOTE = "/data/weknora-dev.tar.gz"


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    # 1. SFTP 上传
    sftp = client.open_sftp()
    print("上传中 ...")
    sftp.put(LOCAL, REMOTE)
    sftp.close()
    print("上传完成:", REMOTE)

    # 2. 服务器校验 + 预留解压目录
    cmd = (
        "ls -lh /data/weknora-dev.tar.gz && "
        "mkdir -p /data/WeKnora-build && "
        "echo 'dir ready'"
    )
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("STDERR:", err)

    client.close()
    print("done")


if __name__ == "__main__":
    main()
