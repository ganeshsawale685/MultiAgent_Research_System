# 🔬 Multi-Agent Research System

An AI-powered research assistant that automates web research using multiple specialized agents.

### 🚀 Live Demo

👉 **[Try the Multi-Agent Research System](https://multiagentresearchsystemgit-57yzrlkgoppv3c8csznh3t.streamlit.app/)**

## ✨ Features

* 🔎 **Search Agent** — Finds relevant information from the web using Tavily.
* 📖 **Reader Agent** — Extracts and analyzes webpage content.
* ✍️ **Writer Agent** — Generates a structured research report.
* 🧠 **Critic Agent** — Reviews the generated report for quality and completeness.
* 🖥️ **Streamlit UI** — Interactive interface for running research and viewing results.

## 🏗️ Workflow

```text
Research Topic
      ↓
Search Agent
      ↓
Reader Agent
      ↓
Writer Agent
      ↓
Critic Agent
      ↓
Final Research Report
```

## 🛠️ Tech Stack

**Python • LangChain • Groq • Tavily • BeautifulSoup • Streamlit**

## ⚙️ Setup

```bash
git clone https://github.com/ganeshsawale685/MultiAgent_Research_System.git
cd MultiAgent_Research_System
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 👨‍💻 Author

**Ganesh Sawale**

[GitHub](https://github.com/ganeshsawale685) • [LinkedIn](https://linkedin.com/in/ganesh-sawale)
