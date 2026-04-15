# Workplace Analytics Dashboard Skill

## Description
A unified workplace analytics dashboard providing workplace-specific insights including geographic distribution, category analysis, agent performance, and SLA metrics.

## Capabilities
- Geographic ticket distribution by country
- Resolution time analysis by category
- Agent group performance tracking (workload vs resolution time)
- Category breakdown and trends
- Monthly trend analysis by category
- Resolution time heatmap (Country vs Category)
- Current ticket status overview
- SLA performance tracking with time buckets

## Data Source
- **Database**: SQLite (`data.db`)
- **Table**: `export_category`
- **Key Fields**: Category, Agent Group Name, Country, Created Date, Resolved Date, Status

## Key Metrics
- Total Records
- Unique Categories
- Open Tickets
- Closed Tickets
- Average Resolution Time (hours and days)

## Visualizations
1. **Ticket Volume by Country** - Bar chart showing geographic distribution
2. **Resolution Time Distribution by Category** - Box plot showing statistical distribution
3. **Agent Group Workload vs Resolution Time** - Dual-axis chart (bar + line)
4. **Workplace Ticket Distribution by Category** - Donut chart with percentages
5. **Monthly Ticket Trends by Category** - Multi-line time series
6. **Average Resolution Time Heatmap** - Country vs Category matrix
7. **Current Ticket Status Distribution** - Bar chart with status colors
8. **Resolution Time Performance (SLA Buckets)** - Bar chart with time ranges

## Technical Implementation
- **Framework**: Flask + Plotly
- **Routes**: `/workplace-analytics`, `/export-category`, `/crest-workspace`
- **Template**: `templates/export_category.html`
- **Styling**: IBM Carbon Design System colors

## SLA Buckets
- < 1 day (Green: `#24a148`)
- 1-3 days (Blue: `#0f62fe`)
- 3-7 days (Yellow: `#f1c21b`)
- 7-14 days (Orange: `#ff832b`)
- > 14 days (Red: `#da1e28`)

## Usage
Access the dashboard at:
- `https://g8-app.azurewebsites.net/workplace-analytics`
- `https://g8-app.azurewebsites.net/export-category`
- `https://g8-app.azurewebsites.net/crest-workspace`

## Special Features
- Country extraction from Agent Group Name (format: COUNTRY-GROUP)
- Box plot for statistical distribution analysis
- Dual-axis visualization for workload vs performance
- Heatmap for cross-dimensional analysis
- Multi-category time series tracking

## Color Scheme
- Primary: `#0f62fe` (IBM Blue)
- Secondary: `#8a3ffc` (Purple), `#33b1ff` (Light Blue)
- Status Colors: Green, Yellow, Blue, Red, Purple