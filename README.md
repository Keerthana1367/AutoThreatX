# AutoThreatX - Automotive Cybersecurity Attack Tree Generator

An intelligent attack tree generation system for automotive cybersecurity threat modeling. AutoThreatX automatically generates comprehensive attack trees for surface goals using LLM-powered generation and provides validation, visualization, and persistent storage.

## Features

- **Automated Attack Tree Generation** - Generate attack trees from surface goals using LLM integration
- **CVSS Scoring** - Vulnerability assessment with CVSSv3 metrics for atomic attacks
- **Hierarchical Attack Modeling** - Multi-level attack node representation with parent-child relationships
- **Attack Node Atomicity** - Classify atomic vs composite attacks
- **Persistent Storage** - MongoDB integration for tree persistence
- **Interactive Visualization** - HTML-based attack tree visualization
- **Web Interface** - Streamlit-based UI for browsing and managing attack trees
- **Validation Framework** - Rules-based validation for attack nodes

## Project Structure

```
ThreatX/
├── main.py                 # Core attack tree generation
├── app.py                  # Streamlit web interface
├── generator.py            # LLM-powered attack node generation
├── validator.py            # Attack tree validation
├── validation_rules.py     # Validation rule definitions
├── db.py                   # MongoDB database operations
├── cvss.py                 # CVSSv3 score calculation utility
├── config.py               # Configuration settings
├── models/
│   ├── attacknode.py       # Attack node data model (Pydantic)
│   └── __init__.py
├── llm/
│   └── llm_client.py       # Groq LLM API integration (LLaMA 3.1)
├── visualize.html          # Attack tree visualization template (D3.js)
└── venv/                   # Python virtual environment
```

## Installation

### Prerequisites
- Python 3.9+
- MongoDB instance (local or cloud) with connection URI
- Groq API key (get from https://console.groq.com)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Keerthana1367/AutoThreatX.git
   cd ThreatX
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit pymongo pydantic requests cvss
   ```

4. **Configure environment variables**
   Set the following environment variables:
   ```bash
   $env:MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/attack_tree_db"
   $env:GROQ_API_KEY="your_groq_api_key_here"
   ```
   
   Or create a `.env` file in the project root:
   ```
   MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/attack_tree_db
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Configuration

### Environment Variables
- **MONGO_URI**: MongoDB connection string (required)
- **GROQ_API_KEY**: Groq API key for LLM access (required)

### Code Configuration
Edit `config.py` to customize:
- Attack tree generation parameters (`min`, `max` children per node)
- Node hierarchies (surface_goal → attack_vector → method → technique)
- Validation rule thresholds

## Usage

### Generate Attack Trees

```python
from main import generate_attack_tree

# Generate attack tree for a surface goal
tree = generate_attack_tree("CAN Gateway Compromise", max_depth=4)
print(tree)
```

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Access the interactive UI at `http://localhost:8501` to browse and visualize attack trees.

### Command Line

```bash
python main.py
```

Generates and saves attack trees to MongoDB automatically.

## Data Models

### AttackNode (Pydantic)
```python
- id: str (UUID)
- goal: str (attack objective)
- level: int (tree depth, 0 = root)
- node_type: str ("surface_goal", "attack_vector", "atomic_attack")
- parent_id: Optional[str] (parent node reference)
- children: List[AttackNode] (child nodes)
- is_atomic: bool (leaf node indicator)
- atomic_reason: Optional[str] (why atomic)
- attacker_role: Optional[str] (required role)
- cvss: Optional[CVSSv3] (vulnerability score)
- validation_score: int (0-100 validation result)
- approved: bool (manual approval flag)
```

### CVSSv3 Scoring
```python
- attack_vector: str (AV:N, AV:A, AV:L, AV:P)
- attack_complexity: str (AC:L, AC:H)
- privileges_required: str (PR:N, PR:L, PR:H)
- user_interaction: str (UI:N, UI:R)
- scope: str (S:U, S:C)
- confidentiality: str (C:N, C:L, C:H)
- integrity: str (I:N, I:L, I:H)
- availability: str (A:N, A:L, A:H)
- base_score: float (0.0-10.0)
```

## API Reference

### Core Functions

#### `generate_attack_tree(surface_goal: str, max_depth: int = 7) -> dict`
Generates complete attack tree for a given surface goal.
- Handles list inputs by extracting first element
- Returns tree as dictionary for JSON serialization

#### `expand_tree(node: AttackNode, max_depth: int)`
Recursively expands tree nodes up to specified depth.

#### `generate_children(node: AttackNode) -> List[AttackNode]`
Generates child attack nodes using LLM.

### Database Functions

#### `get_tree(surface_goal: str) -> dict | None`
Retrieves saved attack tree from MongoDB.

#### `save_tree(surface_goal: str, tree_json: dict)`
Saves attack tree with timestamp to MongoDB.

#### `get_all_surface_goals() -> List[str]`
Retrieves all unique surface goals from database.

## Validation & CVSS Scoring

Attack trees are validated against rules in `validation_rules.py`:
- **Node Completeness** - All required fields present
- **Goal Clarity** - Well-defined, specific goals
- **Attack Feasibility** - Realistic automotive attacks
- **Atomicity Check** - Proper leaf node classification

**CVSS Scoring** (for atomic nodes only):
- Calculated using `cvss.py` utility based on attack vector, complexity, and impact
- Base scores range from 0.0 to 10.0
- Applied only to terminal attack nodes (is_atomic = True)
- Metrics: AV (Attack Vector), AC (Attack Complexity), PR (Privileges Required), UI (User Interaction), C/I/A (Confidentiality/Integrity/Availability)

Validation results scored 0-4, minimum score of 3 for approval.

## Key Design Principles

- **LLM-Assisted Only** - LLMs used only for node generation, not decision-making
- **Deterministic Validation** - All nodes validated against explicit rules
- **Structured Output** - JSON-based attack trees for easy integration
- **Persistence Layer** - MongoDB for scalable tree storage
- **Rule-Based Filtering** - Invalid nodes automatically discarded

## Technologies Used

- **Framework**: Python 3.9+
- **Web UI**: Streamlit
- **Data Model**: Pydantic v2
- **Database**: MongoDBGroq (LLaMA 3.1)
- **CVSS Scoring**: CVSSv3 calculation engine
- **Visualization**: HTML/D3.js

## Core Dependencies

- **pydantic** - Data validation and modeling
- **pymongo** - MongoDB database driver
- **streamlit** - Web UI framework
- **requests** - HTTP client for LLM API calls
- **cvss** - CVSSv3 base score calculation

Install all dependencies:
```bash
pip install streamlit pymongo pydantic requests cvss
```
- openai / groq (LLM providers)

## Academic Context

Developed as a **final-year academic project** extending undergraduate research on systematic attack tree modeling for automotive cybersecurity. Focus on controlled, validated, goal-oriented attack tree generation.

## Contributing

Contributions welcome! Please ensure:
- Code follows PEP 8 style guide
- All existing tests pass
- New validation rules documented
- MongoDB operations properly error-handled

## License

MIT License - See LICENSE file for details

## Author

**Keerthana** - AutoThreatX Project Lead

## Contact & Links

- **GitHub**: [@Keerthana1367](https://github.com/Keerthana1367)
- **Repository**: [AutoThreatX](https://github.com/Keerthana1367/AutoThreatX)

## References & Standards

- [CVSS v3.1 Specification](https://www.first.org/cvss/v3.1/specification-document)
- [Attack Tree Analysis - Wikipedia](https://en.wikipedia.org/wiki/Attack_tree)
- [ISO/SAE 21434 - Automotive Cybersecurity](https://www.iso.org/standard/68383)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
