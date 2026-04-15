# Service Requests Dashboard Skill

## Description
A comprehensive analytics dashboard for Crest Workspace Service Request data, providing insights into ticket volumes, resolution times, service types, and operational metrics.

## Capabilities
- Monthly ticket volume trend analysis
- Top 10 service types by volume
- Average resolution time by service type
- Ticket status distribution
- Ticket creation patterns by day of week and hour
- Resolution time distribution with statistical analysis
- Priority level distribution

## Data Source
- **Database**: SQLite (`data.db`)
- **Table**: `crest_workspace`
- **Key Fields**: Service Item, Status, Priority, Created Date, Resolved Date

## Key Metrics
- Total Records
- Unique Service Types
- Unique Statuses
- Average Resolution Time (days)

## Visualizations
1. **Monthly Ticket Volume Trend** - Bar chart showing ticket creation over time
2. **Top 10 Service Types** - Horizontal bar chart of most common service requests
3. **Average Resolution Time by Service Type** - Color-coded bar chart (green/yellow/red based on resolution speed)
4. **Ticket Status Distribution** - Donut chart with status breakdown
5. **Ticket Creation by Day of Week** - Bar chart showing weekly patterns
6. **Ticket Creation by Hour of Day** - Line chart showing daily patterns
7. **Resolution Time Distribution** - Histogram with mean and median indicators (≤530 days)
8. **Priority Distribution** - Bar chart showing priority levels

## Technical Implementation
- **Framework**: Flask + Plotly
- **Route**: `/service-requests`
- **Template**: `templates/service_requests.html`
- **Styling**: IBM Carbon Design System colors

## Usage
Access the dashboard at: `https://g8-app.azurewebsites.net/service-requests`

## Color Scheme
- Primary: `#0f62fe` (IBM Blue)
- Success: `#198038` (Green)
- Warning: `#f1c21b` (Yellow)
- Error: `#da1e28` (Red)
- Secondary: `#ff832b` (Orange), `#8a3ffc` (Purple)