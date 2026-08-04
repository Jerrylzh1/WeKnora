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
        ("=== 访问根路径 / 是否含有 app 挂载点 ===",
         "curl -s http://127.0.0.1:80/ | grep -o '<div id=\"[^\"]*\">' ; "
         "curl -s http://127.0.0.1:80/login | grep -o '<div id=\"[^\"]*\">'"),
        ("=== Login.js 头部是否有异常/源码map ===",
         "CID=$(docker compose -f /data/WeKnora-0.6.0/docker-compose.yml ps -q frontend); "
         "docker exec $CID sh -c 'head -c 400 /usr/share/nginx/html/assets/Login-BkL3FUfE.js'"),
        ("=== 检查 router 默认重定向（本地源码） ===",
         "grep -rn \"path: ''\\|redirect:\\|path: '/',\" /data/WeKnora-build/frontend/dist/assets/*.js 2>/dev/null | head -5 || echo 'no match in dist'"),
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
