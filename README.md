# ENVWATCH

ENVWATCH is a lightweight security readiness audit tool for Linux/Termux environments.

It evaluates system toolchain coverage, network reliability, and basic security posture scoring to determine whether the environment is suitable for cybersecurity workflows.

---

## 🚀 Features

- Security toolchain analysis (Recon, OSINT, Crypto, Debug)
- Network connectivity and DNS validation
- Storage health check
- Security posture scoring (0–100)
- Automated report generation

---

## 📊 Output Example

- LOW RISK: Ready for security tasks
- MEDIUM RISK: Limited capability
- HIGH RISK: Not recommended

---

## 🧰 Tested Tools

- Termux (Android)
- Linux environments

---

## ⚙️ Usage

```bash
python envwatch.py
