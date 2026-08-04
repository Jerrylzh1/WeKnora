import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def run(cmd: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=15)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err


if __name__ == "__main__":
    result = []
    try:
        result.append("=== docker images ===")
        out, err = run("docker images")
        result.append(out)
        if err.strip():
            result.append("STDERR: " + err)
    except Exception as e:
        result.append("连接或执行失败: " + repr(e))
    with open("_tmp_view_images.out", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
