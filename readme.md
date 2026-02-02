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

### Fairer Westminster Principles

The tool assesses governance against five key principles:

1. **Strong Voice** - Residents at the heart of decision-making
2. **Opportunity** - Everyone can participate and succeed
3. **Quality of Life** - High quality of life for all
4. **Safe & Inclusive** - A safe and inclusive city
5. **Greener City** - Leading on climate action

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

The tool contains 9 main sections:

1. **🏠 Home** - Overview, metrics, and framework information
2. **🏛️ Governance Bodies** - View, add, edit, and delete governance bodies
3. **📊 Efficiency Analysis** - Cost-value matrices and efficiency scoring
4. **👥 Stakeholder Analysis** - Power-interest mapping (Schilling framework)
5. **⛓️ Value Chain Mapping** - Activity analysis (Porter framework adapted)
6. **⚡ Five Forces Analysis** - Governance pressure analysis (Porter framework adapted)
7. **🌐 Network View** - Interactive network visualisation
8. **🎯 Fairer Westminster Dashboard** - Principle alignment analysis
9. **📥 Export** - Download data and generate PDF reports

### Edit Mode

Enable **Edit Mode** in the sidebar to:
- Add new governance bodies
- Edit existing entries
- Delete bodies
- Update RAG statuses and recommendations

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

### v4.0 (Current)
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
