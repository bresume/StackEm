# StackEm

**StackEm** is a command-line tool that analyzes `.utrace` profiling files from Unreal Engine using OpenAI's GPT-4 API. It helps you identify bottlenecks in your game or simulation and suggests practical optimizations.
NOTE::Unreal Insights currently doesn't support exporting stack traces to csvs. I'm looking into how to get around that.

---

## 🚀 Features

- Exports `.utrace` to CSV using `UnrealInsights`
- Extracts top timing events
- Sends data to GPT-4 for intelligent analysis
- Returns actionable performance insights
- Supports environment variables and CLI overrides
- A simple GUI that can be used if you're not comfortable with the command line.
- COMING SOON: Multiple options for analysis AI engine.

---

## 📦 Requirements

- Python 3.8+
- OpenAI API Key
- Unreal Engine's `UnrealInsights.exe` (found in your UE install)

---

## 🛠 Setup

1. Clone the repo:

```bash
git clone https://github.com/bresume/StackEm.git
cd StackEm
