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
        result += section("COMPOSE_PROJECT_NAME in .env",
                           "grep -nE 'COMPOSE_PROJECT_NAME|PROJECT_NAME|^[A-Z_]*VERSION' /data/WeKnora-0.6.0/.env")
        result += section("compose volumes block (tail)",
                           "tail -60 /data/WeKnora-0.6.0/docker-compose.yml")
        result += section("postgres/app volume mounts",
                           "grep -nE 'volumes:|/-|/data|:/var|postgres|data-files' /data/WeKnora-0.6.0/docker-compose.yml | head -40")
        result += section("git branch/commit of deployed source (if any)",
                           "cd /data/WeKnora-0.6.0 && (git log --oneline -1 2>/dev/null; git branch 2>/dev/null; ls -la | head)")
        result += section("disk usage of /data",
                           "df -h /data; du -sh /data/WeKnora-0.6.0 2>/dev/null")
    except Exception as e:
        result.append("连接或执行失败: " + repr(e))
    with open("_tmp_probe_env.out", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print("done -> _tmp_probe_env.out")
