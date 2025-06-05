# 🧠 Leon Autonomous AI Assistant – Functionalities & Use Cases

This document outlines the full capabilities of the upgraded **Leon AI system**, now acting as a **fully offline, multi-step autonomous agent** for productivity, document intelligence, and AI-powered task execution.

---

## 🧠 CORE SYSTEM FEATURES

| Category                   | Functionality                    | Description                                                                                    |
| -------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Natural Language Goals** | Goal-to-Workflow Agent           | Accepts complex goals (e.g., “Prepare a grant proposal for RHV”) and executes multi-step plans |
| **Local LLM Integration**  | Ollama + TinyLlama / Mistral     | Executes all reasoning, summarization, tagging, and writing locally                            |
| **Cloud LLM Option**       | GPT-4 / Claude (optional toggle) | Use if cloud APIs are enabled in `.env`                                                        |

---

## 📂 DOCUMENT, EMAIL & MIND MAP INTELLIGENCE

| Category                    | Functionality              | Description / Use Case                                    |
| --------------------------- | -------------------------- | --------------------------------------------------------- |
| **File Parsing & Indexing** | PDF, DOCX, TXT, XLSX       | Reads all text from supported file formats                |
| **Mind Map Intelligence**   | `.xmind` parsing + tagging | Extracts, summarizes, and semantically searches mind maps |
| **Email Analysis**          | Thunderbird / .eml parsing | Summarizes email threads, drafts replies                  |
| **Semantic Search (RAG)**   | Ask about your files       | “What did we promise to RHV in March?”                    |
| **Automatic Tagging**       | Topic & entity tagging     | Auto-categorizes files and mind maps                      |

---

## 📊 AGENT-POWERED OUTPUT GENERATION

| Category                         | Functionality                | Description / Use Case                                |
| -------------------------------- | ---------------------------- | ----------------------------------------------------- |
| **Proposal / Report Generation** | Agent composes .docx files   | “Write a 1-pager from these files”                    |
| **Meeting Summary Generator**    | Audio → Text → Summary       | Auto-transcribes and summarizes meetings              |
| **Mind Map Summaries**           | Node extraction + AI summary | “Summarize deliverables in the Osler map”             |
| **Email Drafting**               | From context or summary      | “Reply to Sarah thanking her for the contract update” |
| **Custom Templates**             | Structured output writer     | Write grant proposals, briefs, weekly reports, etc.   |

---

## 🎤 MULTIMODAL INPUT

| Category                | Functionality       | Description                                            |
| ----------------------- | ------------------- | ------------------------------------------------------ |
| **Audio Transcription** | Whisper integration | Transcribes `.mp3` or `.mp4` meeting recordings        |
| **OCR**                 | Tesseract           | Extracts text from images, scans, or handwritten notes |
| **Voice Commands**      | (Optional skill)    | Say “Hey Leon” + goal via mic (planned feature)        |

---

## 🧠 AGENT ARCHITECTURE

| Category          | Component                           | Description                                            |
| ----------------- | ----------------------------------- | ------------------------------------------------------ |
| **Planner**       | Converts goal to action plan        | “Prepare a proposal” → search → summarize → write      |
| **Executor**      | Runs tools to complete steps        | Uses `search`, `summarize`, `write`, `confirm`, `save` |
| **Memory**        | Tracks steps + intermediate results | Remembers file sources, draft versions, outputs        |
| **Feedback Loop** | Confirms outputs with user          | Asks “Is this draft okay to save/send?”                |

---

## 🌐 UI & MULTI-USER ACCESS

| Category           | Functionality                   | Description                                       |
| ------------------ | ------------------------------- | ------------------------------------------------- |
| **Gradio UI**      | Clean, browser-based dashboard  | Access via `localhost:7860` or `192.168.X.X:7860` |
| **Chat Interface** | Ask anything from indexed data  | “What’s the status of the Tuiris project?”        |
| **Upload Panel**   | Upload files into `user_files/` | Index them immediately for search                 |
| **User Login**     | Role-based auth (admin, viewer) | Simple `users.json` login system                  |
| **LAN Sharing**    | Accessible over Wi-Fi           | Use from other devices on same network            |

---

## 📅 FILE ORGANIZATION & STORAGE

| Folder             | Purpose                                |
| ------------------ | -------------------------------------- |
| `data/user_files/` | Where your source files live           |
| `data/chroma_db/`  | Embedding vector storage               |
| `data/output/`     | Final documents, proposals, summaries  |
| `agent/memory.py`  | Tracks agent run logs and past results |

---

## 🔒 PRIVACY & SECURITY

| Feature                 | Description                                       |
| ----------------------- | ------------------------------------------------- |
| **Fully Offline Mode**  | All AI, file processing, and planning run locally |
| **Optional Cloud Mode** | Use GPT/Claude only if `USE_CLOUD_LLM=true`       |
| **No External Logging** | No data leaves your device unless explicitly sent |
| **User Access Roles**   | Viewers can’t change files or plans               |

---

## 🧠 EXAMPLE USER QUERIES (WORKFLOWS)

| Query                                                             | Result                                                |
| ----------------------------------------------------------------- | ----------------------------------------------------- |
| “Prepare a 1-pager investor brief for RHV using latest documents” | Agent searches, summarizes, writes, and saves `.docx` |
| “Summarize Tuiris mind map and draft a progress report”           | Pulls `.xmind`, tags nodes, generates report          |
| “Transcribe and summarize the strategy meeting from Tuesday”      | Whisper transcribes `.mp4`, LLM summarizes            |
| “Reply to Bandwidth Global thanking them for the partnership”     | Agent finds thread and drafts polite reply            |
| “Show all tasks mentioned in files tagged ‘Osler’”                | Lists actionable items from those files               |

---

This document can be included in the root of your repository as `FUNCTIONALITY.md`, presented in the Gradio UI, or used as onboarding documentation for future collaborators and Codex agents.
