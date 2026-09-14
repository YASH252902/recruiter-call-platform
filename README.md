# 🚀 Recruiter Call Platform

A high-performance, AI-powered system console for recruiters. This platform fetches candidate profiles with lightning-fast Redis caching and uses the Gemini AI API to generate real-time, personalized opening call scripts.

Built with a dark-mode, system-monitor-style frontend featuring live telemetry, Chart.js metrics, and a simulated terminal console.

## 🔗 Public Links

*   **Live App (Render):** https://recruiter-call-platform.onrender.com
*   **GitHub Repository:** https://github.com/YASH252902/recruiter-call-platform

---

## ✨ Features

*   **⚡ Candidate Lookup Node:** Queries candidate data and caches the results in Redis. Repeat queries hit the cache for instant retrieval.
*   **🧠 AI Script Generator:** Streams real-time candidate data into Gemini to generate custom opening lines for recruiter calls, displayed with a terminal-style typing animation.
*   **📊 Live Telemetry:** Real-time Chart.js graphs tracking network traffic and cache efficiency (Hits vs. Misses).
*   **💻 Command Center UI:** A glassmorphism dark-mode UI with pulsing neon indicators and a live scrolling system log terminal.
*   **☁️ Cloud-Ready Architecture:** Designed to run locally with Docker Compose (including Redis/Kafka containers) and seamlessly degrade gracefully to a serverless/cloud environment on Render.

---

## 🛠️ Tech Stack

*   **Backend:** Python, FastAPI
*   **AI Integration:** Google Gemini API
*   **Data & Caching:** Redis, Kafka (Local event streaming)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js
*   **Infrastructure:** Docker, Docker Compose, Render (Cloud Hosting)

---

## 💻 Local Setup & Installation

You can run this entire platform locally in isolated containers using Docker.

### 1. Clone the repository
```bash
git clone [https://github.com/YASH252902/recruiter-call-platform.git](https://github.com/YASH252902/recruiter-call-platform.git)
cd recruiter-call-platform