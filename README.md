# 🔥 Server Stress Testing Suite 🔥

<div align="center">

![Banner](https://via.placeholder.com/800x200/0d1117/ffffff?text=Server+Stress+Testing+Suite)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)

**A comprehensive toolkit for evaluating server performance under extreme conditions**

</div>

## 📋 Overview

This toolkit provides a collection of utilities for stress testing web servers and network applications. Test the limits of your infrastructure and identify potential bottlenecks before they become problems in production.

> ⚠️ **IMPORTANT**: These tools should only be used on servers and infrastructure that you own or have explicit permission to test.

## 🛠️ Tools Included

### 1. `stress_test.py`
A configurable network stress tester with TCP and UDP support. Generates realistic mixed traffic patterns to simulate high load scenarios.

### 2. `virtual_server.py`
A simple test server that can be used as a target for stress tests. Supports both HTTP and raw socket modes.

### 3. `monitor.py`
Real-time resource monitoring tool to track the impact of stress tests on your server.

### 4. `obliterate.py`
⚠️ **EXTREME CAUTION** ⚠️ - Advanced stress testing tool designed to push systems to their absolute limits. For controlled testing environments only.

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- `psutil` library (install via `pip install psutil`)

### Basic Usage

1. **Start a test server:**
   ```bash
   python virtual_server.py --port 8080 --mode http
   ```

2. **Monitor server resources:**
   ```bash
   # Get the PID of your server process first
   python monitor.py <SERVER_PID>
   ```

3. **Run a stress test:**
   ```bash
   python stress_test.py 127.0.0.1 8080 --threads 100 --duration 60 --mode tcp
   ```

## 📊 Advanced Usage

### TCP Flood Testing
```bash
python stress_test.py 127.0.0.1 8080 --threads 200 --duration 120 --mode tcp
```

### UDP Flood Testing
```bash
python stress_test.py 127.0.0.1 8080 --threads 200 --duration 120 --mode udp
```

### Extreme Load Testing (Use with caution)
```bash
python obliterate.py 127.0.0.1 8080 --duration 300
```

## 📈 Interpreting Results

- **High connection errors**: May indicate connection limits being reached
- **Memory usage spikes**: Could suggest memory leaks or inefficient resource handling
- **CPU saturation**: Look for bottlenecks in request processing

## 🔒 Ethical Use Guidelines

- Always obtain proper authorization before testing
- Start with low thread counts and short durations
- Be mindful of potential impact on shared infrastructure
- Schedule tests during off-peak hours when possible
- Never use these tools against systems you don't own or control

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions to improve this toolkit are welcome. Please feel free to submit pull requests.

---

<div align="center">
<p>Created with ❤️ by <a href="https://github.com/Jabaldoo">Jabaldoo</a></p>
</div>
