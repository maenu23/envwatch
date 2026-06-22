import subprocess
import os
import importlib.util
import re
import time
from datetime import datetime


# =========================
# CONFIG
# =========================
REPORT_DIR = "reports"
PLUGIN_DIR = "plugins"
DASH_FILE = f"{REPORT_DIR}/dashboard.html"

MAX_HISTORY = 100
MAX_ALERTS = 30

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(PLUGIN_DIR, exist_ok=True)


# =========================
# EXEC
# =========================
def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=4
        )
        return {
            "ok": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    except Exception as e:
        return {"ok": False, "output": "", "error": str(e)}


# =========================
# ANALYZE + ALERT LEVEL
# =========================
def analyze(cmd, output):

    tool = cmd[0]

    alert = None

    if tool == "ping":
        latency = re.findall(r"time=([\d\.]+)", output)
        ms = float(latency[-1]) if latency else None

        if ms and ms > 250:
            alert = ("CRITICAL", f"High latency detected: {ms}ms")
        elif ms and ms > 120:
            alert = ("WARN", f"Elevated latency: {ms}ms")

        return {"type": "ping", "latency": ms, "alert": alert}

    if tool == "curl":
        status = re.findall(r"HTTP/\d\.\d\s+(\d+)", output)
        code = int(status[0]) if status else None

        if code and code >= 500:
            alert = ("CRITICAL", f"Server error {code}")
        elif code and code >= 400:
            alert = ("WARN", f"HTTP issue {code}")

        return {"type": "http", "status": code, "alert": alert}

    if tool == "nmap":
        ports = re.findall(r"(\d+)/tcp\s+open", output)

        if len(ports) > 3:
            alert = ("WARN", f"Multiple open ports: {len(ports)}")

        return {"type": "scan", "ports": ports, "alert": alert}

    return {"type": "generic", "alert": None}


# =========================
# LOAD PLUGINS
# =========================
def load_plugins():

    plugins = {}

    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py"):

            path = os.path.join(PLUGIN_DIR, file)
            name = file.replace(".py", "")

            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "register"):
                plugins[name] = module.register()

    return plugins


# =========================
# ALERT STORE
# =========================
alerts = []


def push_alert(level, message, plugin):

    alerts.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "message": message,
        "plugin": plugin
    })

    if len(alerts) > MAX_ALERTS:
        del alerts[:-MAX_ALERTS]


# =========================
# RUN PLUGIN
# =========================
def run_plugin(name, plugin, target):

    results = []

    for t in plugin["tests"]:

        cmd = [c.replace("{target}", target) for c in t["cmd"]]

        res = run_cmd(cmd)
        parsed = analyze(cmd, res["output"])

        if parsed["alert"]:
            level, msg = parsed["alert"]
            push_alert(level, msg, name)

        results.append({
            "plugin": name,
            "desc": t["desc"],
            "parsed": parsed,
            "time": datetime.now().strftime("%H:%M:%S")
        })

    return results


# =========================
# DASHBOARD
# =========================
def render_dashboard(history, target):

    rows = ""
    alert_rows = ""

    for h in history[-MAX_HISTORY:]:

        color = "#2ea043"

        if h["parsed"]["alert"]:
            level, _ = h["parsed"]["alert"]

            if level == "WARN":
                color = "#d29922"
            if level == "CRITICAL":
                color = "#f85149"

        rows += f"""
        <tr style="color:{color}">
            <td>{h['time']}</td>
            <td>{h['plugin']}</td>
            <td>{h['desc']}</td>
            <td>{h['parsed']}</td>
        </tr>
        """

    for a in alerts[-MAX_ALERTS:]:

        color = "#2ea043"
        if a["level"] == "WARN":
            color = "#d29922"
        if a["level"] == "CRITICAL":
            color = "#f85149"

        alert_rows += f"""
        <tr style="color:{color}">
            <td>{a['time']}</td>
            <td>{a['level']}</td>
            <td>{a['plugin']}</td>
            <td>{a['message']}</td>
        </tr>
        """

    html = f"""
<html>
<head>
<meta http-equiv="refresh" content="2">
<title>ENVWATCH v36 ALERT ENGINE</title>

<style>
body {{
    background:#0d1117;
    color:#e6edf3;
    font-family:Arial;
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-bottom:20px;
}}

td, th {{
    border:1px solid #30363d;
    padding:6px;
    font-size:12px;
}}

h1 {{ color:#58a6ff; }}
h2 {{ color:#79c0ff; }}
</style>
</head>

<body>

<h1>ENVWATCH ALERT ENGINE</h1>

<p><b>Target:</b> {target}</p>

<h2>EVENTS</h2>
<table>
<tr><th>Time</th><th>Plugin</th><th>Desc</th><th>Parsed</th></tr>
{rows}
</table>

<h2>ALERTS</h2>
<table>
<tr><th>Time</th><th>Level</th><th>Plugin</th><th>Message</th></tr>
{alert_rows}
</table>

</body>
</html>
"""

    with open(DASH_FILE, "w") as f:
        f.write(html)


# =========================
# MAIN LOOP
# =========================
def main():

    plugins = load_plugins()

    if not plugins:
        print("No plugins found")
        return

    target = input("Target: ").strip()

    history = []
    cycle = 0

    print("\nENVWATCH v36 ALERT ENGINE STARTED\n")

    while True:

        cycle += 1

        for name, plugin in plugins.items():

            results = run_plugin(name, plugin, target)

            for r in results:

                history.append(r)

        if len(history) > MAX_HISTORY:
            del history[:-MAX_HISTORY]

        render_dashboard(history, target)

        print(f"CYCLE {cycle} | EVENTS {len(history)} | ALERTS {len(alerts)}")

        time.sleep(2)


if __name__ == "__main__":
    main()
