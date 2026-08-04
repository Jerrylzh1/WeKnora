import os
import paramiko

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
    build_cmd = (
        "setsid bash -c 'cd /data/WeKnora-build/frontend && "
        "docker build -t weknora-ui:0711-frontend-only -f Dockerfile . "
        "> /data/build-frontend4.log 2>&1' >/dev/null 2>&1 & "
        "sleep 2; echo LAUNCHED"
    )
    out, err = ssh_exec(client, build_cmd, timeout=60)
    print("launch:", out.strip(), err.strip())
    client.close()
    print("已触发后台 build frontend4，日志: /data/build-frontend4.log")


if __name__ == "__main__":
    main()
