import os
import tarfile
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")

LOCAL_DIST = r"d:/AI-plat-form/01-githubcode/WeKnora/frontend/dist"
LOCAL_TAR = r"d:/weknora-dist3.tar.gz"
REMOTE_TAR = "/data/frontend-dist3.tar.gz"
REMOTE_FRONTEND = "/data/WeKnora-build/frontend"


def ssh_exec(client, cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode(), stderr.read().decode()


def main():
    if os.path.exists(LOCAL_TAR):
        os.remove(LOCAL_TAR)
    with tarfile.open(LOCAL_TAR, "w:gz") as tar:
        tar.add(LOCAL_DIST, arcname="dist")
    print(f"[local] 打包 {LOCAL_TAR} ({os.path.getsize(LOCAL_TAR)/1024/1024:.2f} MB)")

    transport = paramiko.Transport((HOST, 22))
    transport.connect(username=USER, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(LOCAL_TAR, REMOTE_TAR)
    sftp.close()
    transport.close()
    print("[sftp] 上传完成")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    for title, c in [
        ("备份旧 dist", f"if [ -d {REMOTE_FRONTEND}/dist ]; then mv {REMOTE_FRONTEND}/dist {REMOTE_FRONTEND}/dist.bak.$(date +%s); echo BACKED_UP; else echo NO_OLD; fi"),
        ("解压新 dist", f"cd {REMOTE_FRONTEND} && tar -xzf {REMOTE_TAR} && echo EXTRACTED"),
        ("校验透明 logo 资源", f"ls -la {REMOTE_FRONTEND}/dist/assets/weknora-*.png 2>&1 | head"),
    ]:
        out, err = ssh_exec(client, c, timeout=90)
        print(f"=== {title} ===")
        print(out.strip())
        if err.strip():
            print("STDERR:", err.strip())
    client.close()
    print("[done]")


if __name__ == "__main__":
    main()
