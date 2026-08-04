import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def run(cmd: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=20)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err


def section(title, cmd):
    out, err = run(cmd)
    lines = ["=== " + title + " ===", out.strip()]
    if err.strip():
        lines.append("STDERR: " + err.strip())
    lines.append("")
    return lines


if __name__ == "__main__":
    result = []
    try:
        result += section("find compose files",
                           "find /data /root /opt /srv -maxdepth 4 -name 'docker-compose*.yml' 2>/dev/null; "
                           "find / -maxdepth 5 -name 'docker-compose*.yml' 2>/dev/null | grep -i weknora")
        result += section("weknora containers",
                           "docker ps -a --filter 'name=weknora' --format '{{.Names}}\\t{{.Image}}\\t{{.Status}}'")
        result += section("weknora volumes",
                           "docker volume ls | grep -i weknora")
        result += section("weknora networks",
                           "docker network ls | grep -i weknora")
        result += section("running version (system/info)",
                           "for p in 8080 80 8888 8000; do "
                           "r=$(curl -s --max-time 3 http://127.0.0.1:$p/api/v1/system/info 2>/dev/null); "
                           "if [ -n \"$r\" ]; then echo \"PORT $p: $r\"; fi; done")
        result += section("app env (engine/db)",
                           "docker inspect weknora-app 2>/dev/null | grep -iE 'VECTOR|MILVUS|POSTGRES|ELASTIC|INFINITY|QDRANT|DATABASE' | head -20")
    except Exception as e:
        result.append("连接或执行失败: " + repr(e))
    with open("_tmp_probe_server.out", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print("done -> _tmp_probe_server.out")
