#  AutoThreatX — Automotive Cyber Attack Tree Modele

> **AI-powered attack tree generation for automotive ECU security — compliant with ISO/SAE 21434**

🔗 **[Live Demo → autothreatx.onrender.com](https://autothreatx.onrender.com)**

---

##  Demo

<img width="1912" height="866" alt="image" src="https://github.com/user-attachments/assets/ff640bff-7150-4bfb-9b80-4f0e48fb1389" />


*Interactive D3.js attack tree for ABS (Anti-lock Braking System) — 61 nodes generated, Max CVSS 9.9, 39 High Severity Alerts*

---

##  What is AutoThreatX?

AutoThreatX is an AI-powered cybersecurity tool built for automotive security engineers. Given a high-level attack surface (like `CAN Gateway` or `Telematics Control Unit`), it automatically generates a complete, validated, scored attack tree — work that would normally take a security analyst hours or days.

It is built in alignment with **ISO/SAE 21434** (Road Vehicle Cybersecurity Engineering).

---

##  How It Works

```
Surface Goal (e.g. "ABS Compromise")
        │
        ▼
Level 1 — Attack Vectors       (e.g. Wireless, Physical, Network)
        │
        ▼
Level 2 — Methods              (e.g. Firmware Injection, CAN Spoofing)
        │
        ▼
Level 3 — Techniques           (e.g. Buffer Overflow, Replay Attack)
        │
        ▼
Level 4 — Atomic Attacks       (Exact step-by-step attacker actions)
                                + CVSSv3 Score + Validation Score
```

Each node is:
- **Generated** by Llama 3.1 (via Groq API) with strict prompt engineering
- **Validated** against automotive-specific feasibility rules
- **Scored** with a full CVSSv3.1 vector string
- **Stored** in MongoDB for reuse
- **Visualized** as a zoomable, clickable D3.js tree

---

##  Key Features

| Feature | Description |
|---|---|
|  **AI Tree Generation** | Recursive LLM decomposition — Goal → Vectors → Methods → Techniques → Atomic Actions |
|  **Threat Validation** | Every node scored 0–4 against automotive-specific rules; invalid nodes rejected |
|  **CVSS v3.1 Scoring** | Full vector strings + base scores (0.0–10.0) for every atomic attack |
|  **Interactive Visualization** | Zoomable D3.js tree with clickable CVSS side panel |
|  **MongoDB Persistence** | Generate once, reuse forever — full tree stored and retrievable |
|  **Excel Export** | Auto-generates `.xlsx` reports for compliance auditors |

---

##  Tech Stack

- **LLM:** Llama 3.1 via [Groq API](https://console.groq.com)
- **Backend:** Python 3.9+, Pydantic v2
- **Frontend:** Streamlit + D3.js
- **Database:** MongoDB (Atlas)
- **Scoring:** CVSSv3.1 (`cvss` library)
- **Deployment:** Docker + Render

---

##  Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Keerthana1367/AutoThreatX.git
cd AutoThreatX
```

### 2. Install dependencies
```bash
pip install streamlit pymongo pydantic requests cvss
```

### 3. Set environment variables
Create a `.env` file:
```env
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/attack_tree_db
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Generate an attack tree
```bash
python main.py
```

### 5. Launch the web UI
```bash
streamlit run app.py
```
Open `http://localhost:8501` → enter a surface goal → view the attack tree.

---

##  Project Structure

```
AutoThreatX/
├── app.py                  # Streamlit web interface
├── main.py                 # Core attack tree generation
├── generator.py            # LLM-powered node generation (Groq)
├── validator.py            # Attack tree validation engine
├── validation_rules.py     # Automotive-specific rule definitions
├── cvss.py                 # CVSSv3.1 score calculation
├── db.py                   # MongoDB operations
├── config.py               # Config & generation parameters
├── visualize.html          # D3.js interactive tree template
├── models/
│   └── attacknode.py       # Pydantic AttackNode data model
├── llm/
│   └── llm_client.py       # Groq LLM API client
├── Dockerfile
└── render.yaml
```

---

##  Sample Output

For surface goal **"ABS (Anti-lock Braking System)"**:
-  **61 attack nodes** generated
-  **Max CVSS Score: 9.9**
-  **39 High Severity Alerts** (CVSS 7+)
-  **Validation Status: Verified**

---

##  Standards & References

- [ISO/SAE 21434 — Road Vehicle Cybersecurity](https://www.iso.org/standard/68383.html)
- [CVSS v3.1 Specification — FIRST](https://www.first.org/cvss/v3.1/specification-document)
- [MITRE ATT&CK for Vehicles](https://attack.mitre.org/)

---

## 👤 Author

**T. Keerthana**
- GitHub: [@Keerthana1367](https://github.com/Keerthana1367)
- LinkedIn: [keerthanatadkal](https://linkedin.com/in/keerthanatadkal)

---

