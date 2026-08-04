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
        result += section("WEKNORA_VERSION in .env",
                           "grep -nE '^WEKNORA_VERSION' /data/WeKnora-0.6.0/.env")
        result += section("app image id",
                           "docker inspect WeKnora-app --format '{{.Image}}' ; docker images wechatopenai/weknora-app")
        result += section("docker buildx / compose available",
                           "docker compose version; docker buildx version 2>/dev/null | head -1")
    except Exception as e:
        result.append("连接或执行失败: " + repr(e))
    with open("_tmp_probe_ver.out", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print("done -> _tmp_probe_ver.out")
