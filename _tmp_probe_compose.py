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
        result += section("all containers",
                           "docker ps -a --format '{{.Names}}\\t{{.Image}}\\t{{.Status}}' | grep -iE 'weknora|qdrant|minio|neo4j|postgres|app|ui|docreader'")
        result += section("compose top (env/project name)",
                           "head -30 /data/WeKnora-0.6.0/docker-compose.yml")
        result += section(".env (project name / compose_project_name)",
                           "grep -iE 'PROJECT_NAME|COMPOSE_PROJECT|PROJECT' /data/WeKnora-0.6.0/.env 2>/dev/null; echo '--- env file list ---'; ls -la /data/WeKnora-0.6.0/ | grep -iE 'env|yml'")
        result += section("image lines in compose",
                           "grep -nE 'image:|wechatopenai|weknora-' /data/WeKnora-0.6.0/docker-compose.yml | head -40")
        result += section("volumes section",
                           "grep -nE 'volumes:|external:|weknora-060|name:' /data/WeKnora-0.6.0/docker-compose.yml | head -60")
    except Exception as e:
        result.append("连接或执行失败: " + repr(e))
    with open("_tmp_probe_compose.out", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print("done -> _tmp_probe_compose.out")
