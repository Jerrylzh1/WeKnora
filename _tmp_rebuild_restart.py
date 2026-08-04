import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=600)

    # 用最新 dist 重新 build 镜像，覆盖 0711-frontend-only
    build = (
        "cd /data/WeKnora-build/frontend && "
        "echo '=== dist css green check ===' && "
        "grep -ro '#3a9c55' dist/assets/*.css | wc -l && "
        "docker build --no-cache -t weknora-ui:0711-frontend-only . 2>&1 | tail -8"
    )
    stdin, stdout, stderr = client.exec_command(build, timeout=600)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("BUILD STDERR:", err)

    # 重启容器
    restart = (
        "cd /data/WeKnora-0.6.0 && docker compose up -d frontend 2>&1 | tail -5; "
        "sleep 3; "
        "CID=$(docker compose ps -q frontend); "
        "echo '=== container image & created ==='; "
        "docker inspect -f '{{.Config.Image}} | {{.Created}}' $CID; "
        "echo '=== container css green count ==='; "
        "docker exec $CID sh -c \"grep -ro '#3a9c55' /usr/share/nginx/html/assets/*.css | wc -l\"; "
        "echo '=== HTTP ==='; "
        "curl -s -o /dev/null -w '%{http_code}\\n' http://127.0.0.1:80/"
    )
    stdin, stdout, stderr = client.exec_command(restart, timeout=120)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err.strip():
        print("RESTART STDERR:", err)

    client.close()


if __name__ == "__main__":
    main()
