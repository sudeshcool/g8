# Dashboard Skills Collection

This folder contains skill documentation for the Azure-deployed analytics dashboards. Each skill represents a distinct capability or dashboard within the application.

## Available Skills

### 1. Service Requests Dashboard
**File**: [`service-requests-dashboard.skill.md`](./service-requests-dashboard.skill.md)

Comprehensive analytics for Crest Workspace Service Request data with 8 visualizations covering ticket volumes, resolution times, and operational patterns.

**Key Features**:
- Monthly trend analysis
- Service type breakdown
- Resolution time tracking
- Status and priority distribution

**Access**: https://g8-app.azurewebsites.net/service-requests

---

### 2. Workplace Analytics Dashboard
**File**: [`workplace-analytics-dashboard.skill.md`](./workplace-analytics-dashboard.skill.md)

Unified workplace analytics with geographic distribution, agent performance, and SLA tracking across 8 comprehensive visualizations.

**Key Features**:
- Geographic ticket distribution
- Agent group performance
- Category trend analysis
- SLA performance buckets

**Access**: https://g8-app.azurewebsites.net/workplace-analytics

---

### 3. Decision Logic Tool
**File**: [`decisions-tool.skill.md`](./decisions-tool.skill.md)

Interactive decision-making tool for evaluating office space options using weighted multi-criteria analysis.

**Key Features**:
- 7 weighted evaluation criteria
- Building and vicinity amenities scoring
- Cost optimization analysis
- Detailed score breakdown

**Access**: https://g8-app.azurewebsites.net/decisions

---

## Technology Stack

- **Backend**: Flask (Python)
- **Visualization**: Plotly
- **Database**: SQLite
- **Deployment**: Azure App Service
- **Design System**: IBM Carbon Design System

## Data Sources

- **Crest Workspace SR**: Service request tickets and resolution data
- **Export Category**: Workplace analytics with geographic and category data
- **Decisions**: User input for real estate evaluation

## Common Features

All dashboards share:
- Responsive design
- IBM Carbon Design System styling
- Interactive Plotly visualizations
- Real-time data from SQLite database
- Professional color schemes

## Usage

Each skill document contains:
- Detailed capability descriptions
- Data source information
- Key metrics and KPIs
- Visualization specifications
- Technical implementation details
- Access URLs
- Color schemes and styling

## Deployment Information

- **Resource Group**: my-flask-rg
- **App Service**: g8-app
- **Region**: East Asia
- **Base URL**: https://g8-app.azurewebsites.net

## Maintenance

To update any dashboard:
1. Modify the corresponding code in [`app.py`](../my-azure-func/app.py)
2. Update templates in [`templates/`](../my-azure-func/templates/)
3. Redeploy using Azure CLI
4. Update skill documentation if capabilities change

## Support

For issues or questions:
- Review the skill documentation
- Check [`DEPLOYMENT_SUMMARY.md`](../my-azure-func/DEPLOYMENT_SUMMARY.md)
- Consult [`IMPLEMENTATION_GUIDE.md`](../my-azure-func/IMPLEMENTATION_GUIDE.md)