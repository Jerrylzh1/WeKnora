import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def run(client, cmd, timeout=60):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode(), stderr.read().decode()


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    # 1. 当前 daemon 配置
    out, err = run(client, "cat /etc/docker/daemon.json 2>/dev/null; echo '--- docker info mirrors ---'; docker info 2>/dev/null | grep -iA3 mirror")
    print("=== DAEMON ===")
    print(out)
    if err.strip():
        print("ERR:", err)

    # 2. 测试能否访问阿里云镜像加速器
    out2, err2 = run(client, "curl -s -o /dev/null -w 'aliyun mirror http=%{http_code}\\n' --max-time 8 https://xxxx.mirror.aliyuncs.com/v2/ 2>&1; "
                              "curl -s -o /dev/null -w 'dockerhub direct http=%{http_code}\\n' --max-time 8 https://registry-1.docker.io/v2/ 2>&1")
    print("=== NET ===")
    print(out2)
    if err2.strip():
        print("ERR:", err2)

    # 3. 当前运行的全部容器（重启 docker 会影响）
    out3, err3 = run(client, "docker ps -q | wc -l; docker ps --format '{{.Names}}' | head -40")
    print("=== CONTAINERS ===")
    print(out3)
    if err3.strip():
        print("ERR:", err3)

    client.close()


if __name__ == "__main__":
    main()
