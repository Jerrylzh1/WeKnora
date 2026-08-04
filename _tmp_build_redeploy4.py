import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def ssh_exec(client, cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode(), stderr.read().decode()


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    out, err = ssh_exec(client, "tail -8 /data/build-frontend4.log 2>/dev/null; echo '---'; docker images | grep 0711-frontend-only", timeout=40)
    print("=== build4 状态 ===")
    print(out.strip())

    out, err = ssh_exec(client, "cd /data/WeKnora-0.6.0 && docker compose up -d frontend 2>&1", timeout=120)
    print("=== up -d frontend ===")
    print(out.strip())
    if err.strip():
        print("STDERR:", err.strip())

    out, err = ssh_exec(client, "sleep 6; docker ps -a --format '{{.Names}}\\t{{.Status}}\\t{{.Image}}' | grep -i frontend", timeout=40)
    print("=== frontend 状态 ===")
    print(out.strip())

    out, err = ssh_exec(client, "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:80/", timeout=30)
    print("=== 首页 ===")
    print(out.strip())

    out, err = ssh_exec(client,
        "docker exec WeKnora-frontend ls -la /usr/share/nginx/html/assets/ | grep -i 'weknora-CzW' || echo 'NO TRANSPARENT LOGO'", timeout=30)
    print("=== 容器内透明 logo ===")
    print(out.strip())

    client.close()


if __name__ == "__main__":
    main()
