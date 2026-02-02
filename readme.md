# Westminster Governance Mapping Tool

A comprehensive governance analysis and mapping tool for Westminster City Council, aligned with Fairer Westminster principles.

## Features

### Core Capabilities
- **Multi-Framework Analysis**: Integrates Rogers, Schilling, Smith, and Porter frameworks adapted for public sector
- **Fairer Westminster Alignment**: Full integration with Westminster's five key principles
- **RAG Status Assessment**: Traffic light system with Keep/Merge/Close recommendations
- **Interactive Editing**: Add, edit, and delete governance bodies in real-time
- **PDF Export**: Generate comprehensive reports for stakeholders
- **Network Visualisation**: Interactive network graphs showing stakeholder overlaps
- **Professional Styling**: Josefin Sans font for modern, clean presentation

### Analytical Frameworks

#### Highly Applicable to Public Sector ✅
1. **Rogers (2003)** - Diffusion of Innovations
2. **Schilling (2022)** - Stakeholder Analysis
3. **Smith (2024)** - Knowledge Management

#### Adapted for Public Sector ⚠️
4. **Porter** - Value Chain Analysis
5. **Porter** - Five Forces Analysis

### Fairer Westminster Pillars

The tool assesses governance against Westminster's five key pillars:

1. **Fairer Communities** - Reducing inequality, enhancing safety (including doubling CCTV), and improving access to education and culture
2. **Fairer Housing** - Delivering greener, more affordable, and social housing (70% on council-owned developments) and reducing homelessness
3. **Fairer Economy** - Supporting local businesses, boosting high streets, and promoting inclusive growth for all residents
4. **Fairer Environment** - Targeting net-zero for council by 2030 and city by 2040 through sustainability, air quality improvements, and climate action
5. **Fairer Council** - Listening to and acting on resident feedback through citizens' assemblies and participatory, transparent decision-making

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Required Python Packages

Install all required packages using pip:

```bash
pip install streamlit pandas plotly networkx reportlab
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Requirements.txt

Create a `requirements.txt` file with the following content:

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
networkx>=3.1
reportlab>=4.0.0
```

## Usage

### Running the Application

1. Navigate to the directory containing `governance_mapping_enhanced.py`

2. Run the Streamlit application:

```bash
streamlit run governance_mapping_enhanced.py
```

3. The application will open in your default web browser at `http://localhost:8501`

### Navigation

The tool contains 10 main sections:

1. **🏠 Home** - Overview, metrics, and framework information
2. **➕ Manage Bodies** - **NEW!** User-friendly forms to add new bodies and edit existing entries
3. **🏛️ Governance Bodies** - View and filter all governance bodies
4. **📊 Efficiency Analysis** - Cost-value matrices and efficiency scoring
5. **👥 Stakeholder Analysis** - Power-interest mapping (Schilling framework)
6. **⛓️ Value Chain Mapping** - Activity analysis (Porter framework adapted)
7. **⚡ Five Forces Analysis** - Governance pressure analysis (Porter framework adapted)
8. **🌐 Network View** - Interactive network visualisation
9. **🎯 Fairer Westminster Dashboard** - Pillar alignment analysis
10. **📥 Export** - Download data and generate PDF reports

### Managing Data - Easy-to-Use Forms

Navigate to the **➕ Manage Bodies** page for a streamlined interface to:

#### Adding New Bodies
1. Click the **"Add New Body"** tab
2. Fill in the comprehensive form with helpful tooltips
3. All required fields are clearly marked with *
4. Use select sliders for intuitive scoring (1-5)
5. Multi-select Fairer Westminster pillars
6. Click **"Add Body"** to save
7. All visualisations update automatically!

#### Editing Existing Bodies
1. Click the **"Edit Existing Body"** tab
2. Select a body from the dropdown
3. View current metrics at the top
4. Modify any fields in the form
5. Click **"Save Changes"** to update
6. Or click **"Delete Body"** to remove
7. All visualisations update automatically!

**No more Edit Mode toggle!** The new dedicated page makes managing governance bodies much easier and more intuitive.

### Dynamic Visualisations

**All visualisations update instantly** when you add, edit, or delete governance bodies:

- **Home page** - RAG status pie chart and efficiency scatter plots
- **Efficiency Analysis** - Cost-value matrices, box plots, and bar charts
- **Stakeholder Analysis** - Power-interest matrices and sunburst charts
- **Value Chain Mapping** - Activity frequency bars and treemaps
- **Five Forces Analysis** - Radar charts (editable separately)
- **Network View** - Network graphs showing stakeholder overlaps
- **Fairer Westminster Dashboard** - Pillar alignment bars and multi-principle scatter plots
- **Export** - PDF reports with updated data

Simply make your changes in the Manage Bodies page and navigate to any analysis page to see the updated visualisations!

### Exporting Data

#### CSV/JSON Export
Download governance data in CSV or JSON format from the Export page.

#### PDF Report Generation
1. Navigate to the **📥 Export** page
2. Click **"Generate PDF Report"**
3. Download the comprehensive PDF including:
   - Executive summary
   - Key metrics
   - Fairer Westminster alignment
   - Detailed body assessments
   - Strategic recommendations
   - Financial impact estimates

## Data Structure

Each governance body includes:

### Core Information
- **Name**: Body identifier
- **Type**: Board, Cabinet, Committee, Place-Based Board, Partnership
- **Level**: Strategic, Tactical, Operational, Community

### Fairer Westminster
- **Fairer Westminster Alignment**: Which principles the body supports
- **Outcome Focus**: Primary outcomes targeted

### Performance Metrics
- **Efficiency Score**: 1-5 rating
- **Value Added**: 1-5 rating
- **Duplication Risk**: 1-5 rating
- **Cost Impact**: Low, Medium, High, Very High

### RAG Assessment
- **RAG Status**: Green, Amber, Red
- **RAG Recommendation**: Keep, Merge, Close

### Stakeholder Information
- **Primary Stakeholders**: Key participants
- **Secondary Stakeholders**: Other affected parties
- **Stakeholder Power**: Low, Medium, High
- **Stakeholder Interest**: Low, Medium, High, Very High

### Operational Details
- **Process Type**: Explicit, Partially Explicit, Mixed, Tacit
- **Decision Speed**: Fast, Medium, Slow
- **Innovation Posture**: Exploit, Explore, Ambidextrous
- **Value Chain Activities**: Comma-separated activities

## Example Data

The tool loads with Westminster City Council sample data demonstrating:
- 8 governance bodies across different levels
- Mix of RAG statuses (Green, Amber, Red)
- Various Fairer Westminster alignments
- Duplication risks and merge recommendations

## Customisation

### Adding Your Own Data

1. Enable **Edit Mode** in the sidebar
2. Use the **"Add New Governance Body"** form
3. Fill in all required fields (marked with *)
4. Click **"Add Governance Body"**

### Modifying Existing Entries

1. Enable **Edit Mode**
2. Navigate to **🏛️ Governance Bodies**
3. Expand the body you want to edit
4. Update fields in the edit form
5. Click **"Save Changes"**

### Updating Five Forces

To modify Five Forces analysis values, you'll need to edit the `SAMPLE_DATA` dictionary in the code:

```python
"five_forces": {
    "Threat of New Entrants": 3,
    "Bargaining Power of Stakeholders": 4,
    "Threat of Alternative Models": 2,
    "Pressure for Accountability": 5,
    "Resource Competition": 4
}
```

## Technical Notes

### Fonts
The application uses **Josefin Sans** font loaded from Google Fonts via CSS. Internet connection required for font loading.

### PDF Generation
PDF reports use ReportLab library with:
- A4 page size
- Professional table formatting
- Colour-coded RAG statuses
- Multi-page comprehensive output

### Network Visualisation
Network graphs use NetworkX for calculations and Plotly for interactive visualisation. Connections represent stakeholder overlap between bodies.

### Data Persistence
- Data persists during a session via Streamlit session state
- To permanently save data, use Export functions
- Closing the browser/session resets to example data

## Browser Compatibility

Tested and optimised for:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Troubleshooting

### Common Issues

**Problem**: Font not displaying correctly
- **Solution**: Ensure internet connection for Google Fonts

**Problem**: PDF generation fails
- **Solution**: Check ReportLab installation: `pip install --upgrade reportlab`

**Problem**: Graphs not displaying
- **Solution**: Verify Plotly installation: `pip install --upgrade plotly`

**Problem**: Session state errors
- **Solution**: Refresh the page to reinitialise

## Performance Considerations

- Optimised for up to 50 governance bodies
- PDF generation may take 10-15 seconds for large datasets
- Network visualisation performance decreases with >30 bodies
- Consider filtering data for better visualisation with large datasets

## Licence

This tool is designed for Westminster City Council internal use. All frameworks cited are used for analytical purposes with appropriate attribution.

## Framework Citations

- Rogers, E.M. (2003). *Diffusion of Innovations*, 5th Edition. Free Press.
- Schilling, M.A. (2022). *Strategic Management of Technological Innovation*, 6th Edition. McGraw-Hill.
- Smith, H.A. & McKeen, J.D. (2024). *Knowledge Management*. Academic Press.
- Porter, M.E. (1985). *Competitive Advantage: Creating and Sustaining Superior Performance*. Free Press.

## Support

For technical support or questions:
- Review this README
- Check the Streamlit documentation: https://docs.streamlit.io
- Verify all dependencies are correctly installed

## Version History

### v5.0 (Current) - Enhanced User Interface
- **NEW: Dedicated Manage Bodies page** with user-friendly forms
- Updated to correct Fairer Westminster pillars (Communities, Housing, Economy, Environment, Council)
- Intuitive form interface with helpful tooltips and validation
- Select sliders for better user experience
- Tab-based interface for adding vs editing
- Removed edit mode toggle - dedicated page instead
- All visualisations update automatically from form changes
- Enhanced field descriptions and placeholders

### v4.0
- Added full Fairer Westminster principle integration
- Implemented RAG status system with recommendations
- Added edit mode for data management
- Implemented PDF export functionality
- Applied Josefin Sans font styling
- Enhanced all visualisations with RAG colour coding

### v3.0
- Multi-framework integration
- Network analysis
- Stakeholder power-interest mapping

## Future Enhancements

Potential additions:
- Data import from Excel/CSV
- Historical tracking of changes
- Automated RAG status calculation
- Integration with council systems
- Multi-user collaboration features
- Advanced filtering and search

## Contact

For questions about Westminster's Fairer Westminster principles, visit:
https://www.westminster.gov.uk/delivering-our-plan-build-fairer-westminster
