# 🗺️ Governance Mapping Tool

A Streamlit-based tool for mapping and analysing governance structures to achieve **small, effective governance** through systematic cost reduction and efficiency improvement.

## 🎯 Purpose

This governance mapping tool supports organisations facing **cost-cutting pressures** and the **need for efficiency** by:

- Identifying duplication and overlap in governance structures
- Analysing high-cost, low-value boards and forums
- Revealing gaps in decision-making coverage
- Supporting evidence-based consolidation and streamlining
- Integrating with ongoing process diagnostic work

## 🌟 Key Features

### Governance Mapping
- Document all boards, forums, networks, and committees
- Capture decision rights, mandates, and meeting cadence
- Categorise by outcome focus (Fairer Westminster principles)
- Distinguish place-based (e.g., Church Street) vs functional governance
- Map governance to innovation lifecycle stages

### Process Diagnostic Integration
- Document operational processes alongside governance
- Distinguish tacit (undocumented) vs explicit (documented) processes
- Link processes to governance touchpoints
- Capture findings from consultant-led diagnostic work

### Efficiency Analysis
- Calculate governance overhead costs
- Identify high-cost, low-value bodies for elimination
- Flag duplication risk between bodies
- Generate cost-value matrices for reform prioritisation
- Recommend consolidation opportunities

### Theoretical Frameworks
Integrates three complementary frameworks:
- **Rogers (2003)**: Diffusion of Innovations - phasing governance reforms
- **Schilling (2022)**: Innovation Management - structural design choices
- **Smith (2024)**: Innovation Strategy - exploration/exploitation balance

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/governance-mapper.git
cd governance-mapper
```

2. **Create a virtual environment** (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Home Page
- Understand the goal: small, effective governance
- Learn different approaches to achieving efficiency
- Review theoretical foundations

### 2. Governance Bodies
- **Add bodies**: Document all boards, forums, committees
- **Categorise**: By outcome focus, innovation posture, Rogers category
- **Assess**: Efficiency scores, cost impact, duplication risk
- **Distinguish**: Place-based vs functional, community-led vs corporate

### 3. Processes & Diagnostic
- **Map processes**: Commercial, place-based prevention, etc.
- **Document type**: Tacit vs explicit knowledge
- **Capture findings**: Notes from ongoing consultant work
- **Link to governance**: Which bodies govern which processes

### 4. Tacit vs Explicit Knowledge
- Understand the difference between documented and undocumented processes
- Identify conversion opportunities (tacit to explicit)
- Calculate knowledge preservation priorities
- Reduce dependency on key individuals

### 5. Efficiency Analysis
- Identify high-cost, low-value bodies
- Flag duplication risks
- Generate cost-value matrices
- Prioritise reform opportunities

### 6. Visualisations
- Outcome focus distribution (Fairer Westminster principles)
- Innovation posture balance (exploit vs explore)
- Rogers adoption readiness
- Process documentation status

### 7. Export Data
- Download CSV or JSON formats
- Export diagnostic notes
- Create comprehensive governance maps
- Import previously exported work

## 🎯 Governance Design Approaches

This tool supports analysis through multiple strategic lenses:

**1. Consolidation Approach** (Centralised)
- Merge multiple boards into fewer, more powerful bodies
- Reduced overhead, faster strategic decisions

**2. Distributed Approach** (Decentralised)
- Push decisions closer to delivery
- Better local context, faster operational decisions

**3. Hybrid Approach** (Strategic-Operational Split)
- Small strategic layer for policy and resources
- Distributed operational layer for delivery decisions

**4. Outcome-Based Approach** (Fairer Westminster Principles)
- Organise governance around outcome themes
- Cross-cutting boards focused on measurable results

**5. Place-Based Approach** (Community & Geographic)
- Governance organised by place (Church Street, Queen's Park, etc.)
- Community-led boards with local decision-making

## 📊 Key Concepts

### Outcome Focus (Fairer Westminster Principles)
Governance should be organised around strategic outcomes:
- Fairer Westminster (reducing inequality)
- Net zero and climate resilience
- Inclusive economic growth
- Housing affordability and quality
- Public health and wellbeing
- Community safety
- Place-based outcomes

### Tacit vs Explicit Knowledge
**Tacit**: Knowledge in people's heads, difficult to transfer
- Risk: Lost when people leave
- Priority: Convert to explicit where cost-effective

**Explicit**: Documented knowledge, easily shared
- Benefit: Preserved, scalable, improvable
- Enables: Efficiency, onboarding, automation

### Innovation Posture (Schilling)
**Exploit**: Focus on efficiency, cost reduction, incremental improvement
**Explore**: Focus on transformation, radical change, new approaches
**Ambidextrous**: Balance both

For cost-cutting objectives, exploit-focused governance is typically appropriate.

## 💡 Use Cases

### Strategic Planning
- Design optimal governance structure for strategic priorities
- Balance efficiency with operational flexibility
- Align governance with organisational strategy

### Cost Reduction
- Identify high-cost, low-value governance
- Eliminate unnecessary boards and forums
- Consolidate duplicative structures
- Reduce meeting overhead

### Process Improvement
- Link process diagnostic findings to governance
- Identify processes with excessive governance burden
- Reveal processes with insufficient governance
- Document tacit knowledge to reduce dependency

### Reform Implementation
- Phase reforms using Rogers adopter categories
- Demonstrate success with innovators and early adopters
- Build evidence base for wider rollout
- Address concerns of cautious adopters

## 📁 Project Structure

```
governance-mapper/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── sample_data.json      # Example Westminster governance map
└── docs/
    ├── QUICKSTART.md     # Quick start guide
    └── THEORY.md         # Detailed theoretical background
```

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualisations
- **Python 3.8+**: Core programming language

### Data Storage
- Uses Streamlit session state for runtime data
- Exports to CSV and JSON formats
- No database required - runs entirely in browser

## 📚 Theoretical Foundations

### Rogers' Diffusion of Innovations (2003)
Application: Phase governance reforms by adopter category
- **Innovators** (2.5%): Pilot reforms in progressive areas
- **Early Adopters** (13.5%): Demonstrate success
- **Early Majority** (34%): Roll out proven reforms
- **Late Majority** (34%): Address concerns, provide support
- **Laggards** (16%): Mandate once established

### Schilling's Innovation Management (2022)
Application: Inform governance structure design
- **Lifecycle Stages**: Map governance coverage across idea→learning
- **Structural Choices**: Centralised/distributed, formal/informal
- **Innovation Posture**: Exploit (efficiency) vs Explore (transformation)

### Smith's Innovation Strategy (2024)
Application: Guide governance optimisation
- **Exploration vs Exploitation**: Balance efficiency and adaptation
- **Value Creation**: Governance should add value, not overhead
- **Knowledge Management**: Convert tacit to explicit knowledge

## 🔧 Best Practices

### Starting Your Map
1. Begin with comprehensive inventory of all governance bodies
2. Be brutally honest about efficiency and value
3. Identify duplication early
4. Link processes to governance from the start
5. Document diagnostic findings as they emerge

### Data Quality
- Use consistent terminology across all entries
- Be specific about decision rights and mandates
- Quantify meeting cadence and costs where possible
- Validate with stakeholders before making recommendations

### Reform Recommendations
- Ground recommendations in efficiency analysis
- Quantify cost savings where possible
- Phase reforms using Rogers categories
- Build evidence through pilots before rollout
- Address tacit knowledge risks in transition plans

## 📝 License

This project is licensed under the MIT Licence - see the LICENSE file for details.

## 🙋 Support

For questions, issues, or suggestions:
- Open an issue on GitHub

## 🌟 Acknowledgements

Based on theoretical frameworks from:
- **Rogers, E. M.** (2003). *Diffusion of Innovations* (5th ed.). Free Press.
- **Schilling, M. A.** (2022). *Strategic Management of Technological Innovation* (7th ed.). McGraw-Hill.
- **Smith, D.** (2024). *Exploring Innovation* (4th ed.). McGraw-Hill.

---

**Version**: 2.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready
