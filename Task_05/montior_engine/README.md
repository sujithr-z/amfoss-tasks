# Monitor engine ⚓

> A lightweight, cross-platform terminal-based system monitoring tool inspired by `htop` and `btop++`.

Monitor Engine was one of the most interesting projects I've worked on so far.

I had actually been thinking about building a system-monitoring application before, and this task gave me the opportunity to finally build a simple version of that idea. 

This project is intentionally a **simple version of a process-monitoring system**. The goal was not to reproduce `htop` or `btop++`, but to understand the core ideas behind them and build the system from the ground up.

If I get more time in the future, I would like to extend this into a much more advanced and visually polished monitoring application with richer terminal UI, process controls, system graphs, historical statistics, resource alerts, and more detailed system information.

Honestly, this was a really cool task.

---

## What Does It Do?

Grand Line Guardian monitors active processes and continuously displays information such as:

- **Process ID (PID)**
- **Process Name**
- **CPU Usage**
- **Memory Usage**
- **Total Active Process Count**

The application detects whether it is running on **Windows or Linux** and uses the appropriate process-information backend for the operating system.

The collected information is then converted into a common process representation and displayed through a live terminal interface using **Rich**.

---

## Architecture

The project follows a simple platform-independent architecture:

```text
                    Grand Line Guardian
                            │
                            ▼
                    Operating System
                       Detection
                            │
                ┌───────────┴───────────┐
                │                       │
              Linux                  Windows
                │                       │
                ▼                       ▼
          Linux Collector        Windows Collector
                │                       │
             /proc             Windows process interface
                │                       │
                └───────────┬───────────┘
                            ▼
                    Common Process Model
                            │
                            ▼
                    Monitoring Engine
                            │
                            ▼
                       Rich UI
                            │
                            ▼
                         Terminal