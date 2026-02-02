# 🗺️ Strategic Governance Mapping Tool - Multi-Framework Analysis

**Comprehensive governance analysis using 5 complementary strategic frameworks with rich visualisations.**

## 🌟 New Features - Enhanced Version

This enhanced version integrates **five strategic frameworks** with sophisticated Visualisations for comprehensive governance analysis.

### 🎯 Integrated Frameworks

1. **Rogers (2003)** - Diffusion of Innovations
2. **Schilling (2022)** - Stakeholder Analysis  
3. **Smith (2024)** - Knowledge Management
4. **Porter** - Value Chain Analysis
5. **Porter** - Five Forces Analysis

---

## 📊 New Visualisations

### 1. Stakeholder Power-Interest Matrix (Schilling)

**What it shows:** Maps governance bodies by their stakeholders' power and interest levels

**Visualisation type:** Interactive scatter plot with quadrants

**Quadrants:**
- **Key Players** (High Power, High Interest) → Manage Closely ⭐
- **Keep Satisfied** (High Power, Lower Interest) → High priority ⚡
- **Keep Informed** (Lower Power, High Interest) → Regular updates 📢
- **Monitor** (Lower Power, Lower Interest) → Minimal effort 👀

**Use case:** Prioritise stakeholder engagement strategies

**Example insight:** Cabinet and Joint Health Board are Key Players requiring close management

---

### 2. Value Chain Coverage Analysis (Porter)

**What it shows:** How governance bodies map to Porter's value chain activities

**Visualisations:**
- **Horizontal bar charts** showing coverage of primary and support activities
- **Sankey flow diagram** showing primary→support activity connections
- **Gap analysis** identifying under-covered activities

**Porter's Value Chain Components:**

**Primary Activities:**
- Service Strategy
- Service Delivery  
- Procurement Operations
- Technology & Innovation
- Marketing & Communications

**Support Activities:**
- Infrastructure
- Technology Development
- Procurement
- Human Resource Management
- Community Development
- Partnership Infrastructure

**Use case:** Identify governance gaps in value creation activities

**Example insight:** Procurement Operations over-covered (Commercial Gateway + Procuring Board duplication)

---

### 3. Five Forces Radar Chart (Porter)

**What it shows:** Governance coverage of Porter's five competitive forces

**Visualisation type:** Radar/spider chart

**Five Forces (adapted for public sector):**

1. **Competitive Rivalry** - Other councils, service providers
   - Example: Cabinet, Joint Health Board
   
2. **Supplier Power** - Contractors, consultants, service suppliers
   - Example: Commercial Gateway Review Board, Procuring Board
   
3. **Buyer Power** - Residents, service users, communities
   - Example: Church Street JV Board, Beyond Lisson Grove Board
   
4. **Threat of Substitutes** - Alternative delivery models (digital, community-led)
   - Example: Climate Leadership Group
   
5. **Threat of New Entrants** - New providers, technologies, approaches
   - Example: Digital Governance Board

**Use case:** Ensure governance addresses all competitive pressures

**Example insight:** All five forces covered, balanced governance response

---

### 4. Governance Network Diagram

**What it shows:** Relationships between governance bodies based on shared attributes

**Visualisation type:** Interactive network graph using NetworkX

**Connections weighted by:**
- Shared Porter's five forces focus (+2)
- Overlapping value chain activities (+1)
- Both have high duplication risk (+2)

**Node properties:**
- **Size** = Value added
- **Colour** = Efficiency score (red → yellow → green)
- **Position** = Spring-layout algorithm showing natural clustering

**Use case:** Identify clusters for potential consolidation

**Example insight:** Commercial Gateway and Procuring Board densely connected (duplication)

---

### 5. Multi-Dimensional Efficiency Matrix

**What it shows:** Cost vs Value vs Duplication in single Visualisation

**Visualisation type:** 3D scatter plot

**Dimensions:**
- **X-axis:** Cost Impact
- **Y-axis:** Value Added
- **Bubble size:** Duplication Risk
- **Colour:** Porter's Five Forces focus

**Use case:** Holistic view of efficiency, value, and duplication

**Example insight:** See which bodies are high-cost/low-value AND have high duplication

---

### 6. Density Heatmap - Value Chain × Level

**What it shows:** Governance concentration across value chain and organizational levels

**Visualisation type:** 2D density heatmap

**Axes:**
- **X:** Value Chain Activities
- **Y:** Organizational Level (Strategic/Tactical/Community)
- **Colour intensity:** Number of governance bodies

**Use case:** Spot over-governed and under-governed areas

**Example insight:** Strategic level concentrated in Service Strategy, gaps in Technology

---

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Navigation

The tool has **8 comprehensive pages:**

1. **🏠 Home** - Dashboard with key metrics and overview charts
2. **🏛️ View Bodies** - Detailed view with filters by power, level, forces
3. **📈 Efficiency Analysis** - Cost-value matrix, duplication identification
4. **👥 Stakeholder Analysis** - Schilling's power-interest matrix with engagement strategies
5. **⛓️ Value Chain Mapping** - Porter's value chain coverage, Sankey flow, gap analysis
6. **⚔️ Five Forces Analysis** - Radar chart, forces detail, gap identification
7. **🌐 Network View** - Interactive network diagram showing body relationships
8. **📥 Export** - Download data and comprehensive executive summary

---

## 📚 Framework Details

### Schilling's Stakeholder Analysis (2022)

**Theoretical basis:** Maps stakeholders by two dimensions:
- **Power:** Ability to influence decisions (1-5)
- **Interest:** Level of concern about outcomes (1-5)

**Application to governance:**
- Each governance body assessed for its key stakeholders' power and interest
- Determines engagement strategy
- Example: Cabinet has both high power (5) and high interest (5) = Key Player

**Recommended strategies:**
- **Key Players (4-5, 4-5):** Fully engage, involve in decisions, regular updates
- **Keep Satisfied (4-5, 1-3):** Keep satisfied but don't overwhelm  
- **Keep Informed (1-3, 4-5):** Adequate information, consult on issues
- **Monitor (1-3, 1-3):** Minimal effort, general communications

---

### Porter's Value Chain

**Theoretical basis:** Organizations create value through:
- **Primary activities:** Directly create value (operations, service delivery)
- **Support activities:** Enable primary activities (IT, HR, procurement)

**Application to governance:**
- Map each governance body to primary and support activities it governs
- Identify gaps where no governance exists
- Spot duplication where multiple bodies govern same activity

**Example findings:**
- Procurement Operations: 2 bodies (duplication!)
- Technology & Innovation: 1 body (Digital Governance Board)
- Marketing & Communications: Gap - no dedicated governance

---

### Porter's Five Forces

**Theoretical basis:** Five competitive forces shape strategy:
1. Rivalry among existing competitors
2. Threat of new entrants
3. Threat of substitute products/services
4. Bargaining power of buyers
5. Bargaining power of suppliers

**Adaptation for public sector governance:**
- **Competitive Rivalry:** Other councils, alternative providers
- **Supplier Power:** Contractors, consultants, outsourced services
- **Buyer Power:** Residents, service users, community voice
- **Threat of Substitutes:** Digital services, community-led delivery, privatization
- **Threat of New Entrants:** New technologies, disruptive providers, policy changes

**Application to governance:**
- Each body assessed for which competitive force it primarily addresses
- Radar chart shows balanced coverage
- Gaps indicate strategic vulnerabilities

**Example insights:**
- Strong coverage of Supplier Power (2 procurement boards)
- Good Buyer Power representation (2 place-based boards)
- All forces covered (balanced strategic governance)

---

## 💡 Using Multiple Frameworks Together

### Example Analysis Workflow:

**Step 1: Efficiency Analysis**
- Identify Commercial Gateway + Procuring Board duplication
- Both score high on duplication risk (4 and 5)

**Step 2: Stakeholder Analysis**  
- Both have Power=4, Interest=4 (Key Players quadrant)
- Consolidation won't lose critical stakeholder engagement

**Step 3: Value Chain Analysis**
- Both govern "Procurement Operations" (primary)
- Both link to "Procurement" (support)
- Confirms functional overlap

**Step 4: Five Forces Analysis**
- Both address "Supplier Power"
- Only these two address this force
- Consolidation still leaves force covered

**Step 5: Network Analysis**
- Dense connection between these two bodies
- Clustered together (shared attributes)
- Visual confirmation of consolidation opportunity

**Conclusion:** Multiple frameworks converge on same recommendation: **consolidate procurement governance**

---

## 📊 Visualisation Best Practices

### Design Principles Applied:

**1. Colour Coding Consistency**
- Red-Yellow-Green for efficiency (bad → good)
- Blues for primary activities
- Greens for support activities
- Consistent across all charts

**2. Interactive Elements**
- Hover tooltips show detailed data
- Click to filter and explore
- Responsive to user interaction

**3. Multi-Dimensional Display**
- Use of size, color, position simultaneously
- Packs more information without clutter
- Example: Network diagram (size=value, color=efficiency, position=relationships)

**4. Quadrant/Segment Analysis**
- Clear visual boundaries (dotted lines)
- Labelled regions with recommendations
- Examples: Stakeholder matrix, Cost-Value matrix

**5. Flow and Connection**
- Sankey diagrams show process flows
- Network graphs show relationships
- Lines indicate connections and dependencies

---

## 🎯 Key Questions Answered

### Strategic Questions:

✅ **"Who are our key stakeholders?"** → Stakeholder Power-Interest Matrix  
✅ **"Where do we have governance gaps?"** → Value Chain Coverage Analysis  
✅ **"Which competitive forces lack governance?"** → Five Forces Radar  
✅ **"How do governance bodies relate to each other?"** → Network Diagram  
✅ **"Where should we focus stakeholder engagement?"** → Schilling Quadrants  

### Operational Questions:

✅ **"Which boards have duplication?"** → Network clustering + Value Chain overlap  
✅ **"What's the cost-value-duplication trade-off?"** → Multi-dimensional scatter  
✅ **"Which activities are over/under-governed?"** → Density heatmap  
✅ **"Should we consolidate these boards?"** → Check all 5 frameworks  

---

## 📈 Expected Outputs

### Quantitative:
- **Stakeholder metrics:** Number in each power-interest quadrant
- **Value chain coverage:** % of activities with governance
- **Five forces balance:** Coverage score for each force  
- **Network density:** Clustering coefficient showing potential consolidation
- **Efficiency scores:** Average, distribution, improvement potential

### Qualitative:
- **Stakeholder engagement strategies** for each quadrant
- **Value chain gap analysis** with recommendations
- **Five forces response assessment**
- **Network insights** on natural groupings
- **Consolidation recommendations** backed by multiple frameworks

### Visual:
- **8 interactive visualisations** across 8 pages
- **Executive dashboard** with key metrics
- **Export-ready charts** for reports and presentations
- **Evidence base** for governance reform proposals

---

## 🔄 Updating to Enhanced Version

### If you have the basic version:

1. **Replace app.py** with the enhanced version
2. **Update requirements.txt** to include `networkx>=3.0`
3. **Redeploy** on Streamlit Cloud (auto-updates in 1-2 minutes)

Your data structure is compatible - the enhanced version adds new fields but works with existing data.

---

## 💼 Example Use Case: Procurement Governance

**Problem:** Two boards govern procurement (Commercial Gateway + Procuring)

**Multi-Framework Analysis:**

| Framework | Finding | Recommendation |
|-----------|---------|----------------|
| **Efficiency** | Both high cost, medium value, duplication 4-5 | Consolidate |
| **Stakeholder (Schilling)** | Both Power=4, Interest=4 (Key Players) | Won't lose engagement |
| **Value Chain (Porter)** | Both govern "Procurement Operations" | Functional overlap confirmed |
| **Five Forces (Porter)** | Both address "Supplier Power" only | Can merge without gaps |
| **Network** | Densely connected, clustered together | Natural consolidation candidates |

**Integrated Recommendation:** **Merge into single Strategic Procurement Board**

**Evidence base:** 5 frameworks × 3+ visualisations = Compelling case

**Estimated saving:** £85,000 annually

---

## 🎨 Visualisation Gallery

This tool provides:
- ✅ **Scatter plots** with size, colour, and hover tooltips
- ✅ **Radar charts** showing balanced coverage
- ✅ **Sankey flow diagrams** showing process flows
- ✅ **Network graphs** with physics-based layouts
- ✅ **Heatmaps** showing concentration patterns
- ✅ **Bar charts** (horizontal and vertical) with colour scales
- ✅ **Quadrant matrices** with strategic recommendations
- ✅ **Multi-dimensional plots** combining 3+ variables

All visualisations are:
- **Interactive** (hover, zoom, pan)
- **Export-ready** (PNG, SVG download)
- **Professionally styled** (consistent colours, fonts, labels)
- **Insight-driven** (clear recommendations)

---

## 📖 Further Reading

**Rogers, E. M.** (2003). *Diffusion of Innovations* (5th ed.). Free Press.

**Schilling, M. A.** (2022). *Strategic Management of Technological Innovation* (7th ed.). McGraw-Hill.
- Chapter 2: Sources of Innovation
- Chapter 14: Managing the New Product Development Process (includes stakeholder analysis)

**Smith, D.** (2024). *Exploring Innovation* (4th ed.). McGraw-Hill.

**Porter, M. E.** (1985). *Competitive Advantage: Creating and Sustaining Superior Performance*. Free Press.
- Value Chain Analysis framework
- Five Forces framework

---

## 🆘 Support

**Questions about:**
- Theoretical frameworks → See framework sections above
- Visualisations → Check Visualisation Gallery section
- Technical issues → Open GitHub issue
- Deployment → See DEPLOYMENT.md (if available)

---

**Version:** 2.1 - Enhanced Multi-Framework Analysis  
**Frameworks:** Rogers + Schilling + Smith + Porter (Value Chain) + Porter (Five Forces)  
**Visualisations:** 8 pages, 15+ interactive charts  
**Status:** Production Ready 🚀
