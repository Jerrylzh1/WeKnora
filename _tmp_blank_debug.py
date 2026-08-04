import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=60)

    cmds = [
        ("=== 容器内 index.html 内容 ===",
         "CID=$(docker compose -f /data/WeKnora-0.6.0/docker-compose.yml ps -q frontend); "
         "docker exec $CID cat /usr/share/nginx/html/index.html"),
        ("=== 容器 assets 目录文件 ===",
         "CID=$(docker compose -f /data/WeKnora-0.6.0/docker-compose.yml ps -q frontend); "
         "docker exec $CID sh -c 'ls -la /usr/share/nginx/html/assets/ | head -20'"),
        ("=== 首页 HTTP 返回前 30 行（确认 body 是否空） ===",
         "curl -s http://127.0.0.1:80/ | head -30"),
        ("=== nginx 容器日志（看是否有 404/500） ===",
         "CID=$(docker compose -f /data/WeKnora-0.6.0/docker-compose.yml ps -q frontend); "
         "docker logs --tail 15 $CID 2>&1"),
    ]
    for title, cmd in cmds:
        print("==== " + title + " ====")
        stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err.strip():
            print("STDERR:", err)
        print()

    client.close()


if __name__ == "__main__":
    main()
