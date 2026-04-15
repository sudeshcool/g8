# Azure DevTools Dashboard - Implementation Guide

## Overview
This document provides detailed implementation notes for the Azure DevTools Dashboard application, including recent modifications and guidance for future updates.

---

## Recent Changes

### 1. Time Series Graph Enhancement (Export Category Dashboard)

**Location**: `app.py` lines 205-243

**What Changed**: Modified the "Tickets Over Time" graph to show separate lines for each category instead of a consolidated view.

**Implementation Details**:

```python
# Time series by category
df_time = df.copy()
df_time['year_month'] = pd.to_datetime(df_time['Created Date']).dt.to_period('M')

# Group by month and category
time_category_counts = df_time.groupby(['year_month', 'Category']).size().reset_index(name='count')
time_category_counts['year_month'] = time_category_counts['year_month'].astype(str)

# Get top categories for the legend
top_categories = df['Category'].value_counts().head(10).index.tolist()

# Create separate traces for each category
traces = []
colors = ['#0f62fe', '#4589ff', '#78a9ff', '#a6c8ff', '#002d9c', '#a6c8ff', '#d0e2ff', '#8a3ffc', '#6929c4', '#491d8b']

for idx, category in enumerate(top_categories):
    category_data = time_category_counts[time_category_counts['Category'] == category]
    traces.append(go.Scatter(
        x=category_data['year_month'].tolist(),
        y=category_data['count'].tolist(),
        mode='lines+markers',
        name=category,
        line=dict(color=colors[idx % len(colors)]),
        marker=dict(size=6)
    ))

time_series_data = {
    'data': traces,
    'layout': go.Layout(
        title='Tickets Over Time by Category',
        font=dict(family="IBM Plex Sans"),
        xaxis_title='Month',
        yaxis_title='Count',
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
}
```

**Key Features**:
- Monthly aggregation instead of daily
- Top 10 categories shown as separate lines
- Color-coded lines with IBM Carbon Design colors
- Legend positioned on the right side
- Unified hover mode for better comparison

---

## Database Analysis Results

### Workplace Health and Safety (74 tickets)
Top ticket types by frequency:
1. Standing desk requests (4 tickets)
2. Vehicle accidents (2 tickets)
3. Weather-related incidents (2 tickets)
4. Individual health/safety concerns (remaining)

### Workplace Security (238 tickets)
Top ticket types by frequency:
1. Unattended laptops (55 tickets)
2. Badge deactivation for leaves (37 tickets)
3. Incident reports (11 tickets)
4. Badge reactivation (4 tickets)
5. Security door issues (3 tickets)

---

## How to Modify the Application

### Adding New Dashboards

1. **Create a new route in `app.py`**:
```python
@app.route('/your-dashboard')
def your_dashboard():
    try:
        # Load data from SQLite
        df = query_to_dataframe('SELECT * FROM your_table')
        
        # Calculate statistics
        total_records = len(df)
        
        # Create visualizations
        # ... your chart code here
        
        return render_template('your_dashboard.html',
                             total_records=total_records,
                             chart_data=json.dumps(chart_data, cls=plotly.utils.PlotlyJSONEncoder))
    except Exception as e:
        return f"Error loading data: {str(e)}", 500
```

2. **Create corresponding template in `templates/your_dashboard.html`**:
```html
{% extends "base.html" %}

{% block title %}Your Dashboard{% endblock %}

{% block content %}
<!-- Your dashboard content -->
{% endblock %}

{% block extra_js %}
<script>
    // Your Plotly charts
    var chartData = {{ chart_data | safe }};
    Plotly.newPlot('chart-div', chartData.data, chartData.layout, {responsive: true});
</script>
{% endblock %}
```

### Modifying Existing Charts

#### Change Time Aggregation
To change from monthly to weekly:
```python
df_time['year_week'] = pd.to_datetime(df_time['Created Date']).dt.to_period('W')
```

To change to quarterly:
```python
df_time['year_quarter'] = pd.to_datetime(df_time['Created Date']).dt.to_period('Q')
```

#### Change Number of Categories Shown
Modify line 214 in `app.py`:
```python
top_categories = df['Category'].value_counts().head(15).index.tolist()  # Show 15 instead of 10
```

#### Change Chart Colors
Modify the colors list (line 217):
```python
colors = ['#your-color-1', '#your-color-2', ...]  # Add your hex colors
```

#### Add Filtering by Date Range
```python
# Add date filter
start_date = '2025-01-01'
end_date = '2025-12-31'
df_filtered = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]
```

### Creating Category-Specific Breakdowns

To create a breakdown for a specific category (like Workplace Security):

```python
@app.route('/workplace-security-breakdown')
def workplace_security_breakdown():
    try:
        # Query specific category
        query = """
        SELECT Subject, COUNT(*) as Count 
        FROM export_category 
        WHERE Category LIKE '%Workplace Security%' 
        GROUP BY Subject 
        ORDER BY Count DESC 
        LIMIT 10
        """
        df = query_to_dataframe(query)
        
        # Create bar chart
        chart_data = {
            'data': [go.Bar(
                x=df['Subject'].tolist(),
                y=df['Count'].tolist(),
                marker=dict(color='#0f62fe')
            )],
            'layout': go.Layout(
                title='Workplace Security - Top Issues',
                font=dict(family="IBM Plex Sans"),
                xaxis_tickangle=-45
            )
        }
        
        return render_template('security_breakdown.html',
                             chart_data=json.dumps(chart_data, cls=plotly.utils.PlotlyJSONEncoder))
    except Exception as e:
        return f"Error: {str(e)}", 500
```

---

## Database Schema

### export_category Table
```sql
CREATE TABLE IF NOT EXISTS "export_category" (
    "ID" TEXT,
    "Subject" TEXT,
    "Status" TEXT,
    "Priority" TEXT,
    "Category" TEXT,
    "Ticket type" TEXT,
    "Type" TEXT,
    "Created Date" TIMESTAMP,
    "Resolved Date" TIMESTAMP
);
```

**Indexes**:
- `idx_export_status` on Status
- `idx_export_priority` on Priority
- `idx_export_category` on Category

### Useful SQL Queries

**Get category breakdown**:
```sql
SELECT Category, COUNT(*) as Total 
FROM export_category 
GROUP BY Category 
ORDER BY Total DESC;
```

**Get monthly trends for a category**:
```sql
SELECT 
    strftime('%Y-%m', "Created Date") as Month,
    COUNT(*) as Count
FROM export_category
WHERE Category = 'Your Category'
GROUP BY Month
ORDER BY Month;
```

**Get top subjects by category**:
```sql
SELECT Subject, COUNT(*) as Count
FROM export_category
WHERE Category LIKE '%Your Category%'
GROUP BY Subject
ORDER BY Count DESC
LIMIT 10;
```

---

## Chart Types Available

### 1. Pie Chart
```python
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Creates donut chart
    marker=dict(colors=['#0f62fe', '#4589ff', '#78a9ff'])
)])
```

### 2. Bar Chart
```python
fig = go.Figure(data=[go.Bar(
    x=x_values,
    y=y_values,
    orientation='v',  # 'h' for horizontal
    marker=dict(color='#0f62fe')
)])
```

### 3. Line Chart (Time Series)
```python
fig = go.Figure(data=[go.Scatter(
    x=dates,
    y=values,
    mode='lines+markers',
    line=dict(color='#0f62fe'),
    marker=dict(size=6)
)])
```

### 4. Multi-Line Chart
```python
traces = []
for category in categories:
    traces.append(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name=category
    ))
fig = go.Figure(data=traces)
```

---

## IBM Carbon Design Colors

Primary colors used in the application:
- `#0f62fe` - Primary blue
- `#4589ff` - Light blue
- `#78a9ff` - Lighter blue
- `#a6c8ff` - Very light blue
- `#d0e2ff` - Pale blue
- `#002d9c` - Dark blue
- `#8a3ffc` - Purple
- `#6929c4` - Dark purple
- `#491d8b` - Darker purple

---

## Testing Changes

1. **Start the application**:
```bash
cd my-azure-func
python app.py
```

2. **Access dashboards**:
- Home: http://localhost:5000/
- Crest Workspace: http://localhost:5000/crest-workspace
- Export Category: http://localhost:5000/export-category
- Decisions: http://localhost:5000/decisions

3. **Check database**:
```bash
sqlite3 data.db
.tables
SELECT COUNT(*) FROM export_category;
.quit
```

---

## Common Modifications

### Add a New Metric Card
In your template:
```html
<div class="col-md-3 mb-3">
    <div class="stat-card">
        <h3>{{ your_metric }}</h3>
        <p>Your Metric Name</p>
    </div>
</div>
```

In your route:
```python
your_metric = df['column'].some_calculation()
return render_template('template.html', your_metric=your_metric)
```

### Add Interactive Filtering
Use Plotly's built-in features:
```python
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="All", method="update", args=[{"visible": [True, True, True]}]),
                dict(label="Category 1", method="update", args=[{"visible": [True, False, False]}]),
            ]),
            direction="down",
        )
    ]
)
```

### Export Data to Excel
```python
from flask import send_file
import io

@app.route('/export-excel')
def export_excel():
    df = query_to_dataframe('SELECT * FROM export_category')
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return send_file(output, download_name='export.xlsx', as_attachment=True)
```

---

## Troubleshooting

### Charts Not Displaying
- Check browser console for JavaScript errors
- Verify Plotly.js is loaded in base.html
- Ensure JSON data is properly serialized with `cls=plotly.utils.PlotlyJSONEncoder`

### Database Errors
- Verify database file exists: `ls -la data.db`
- Check table exists: `sqlite3 data.db ".tables"`
- Verify data: `sqlite3 data.db "SELECT COUNT(*) FROM export_category;"`

### Performance Issues
- Add database indexes for frequently queried columns
- Limit data returned in queries (use LIMIT)
- Cache frequently accessed data
- Use pagination for large datasets

---

## Future Enhancements

### Suggested Features
1. **Date Range Filters**: Add UI controls to filter data by date range
2. **Export Functionality**: Add buttons to export charts as images or data as CSV/Excel
3. **Real-time Updates**: Implement WebSocket for live data updates
4. **User Authentication**: Add login system for secure access
5. **Custom Dashboards**: Allow users to create custom dashboard layouts
6. **Drill-down Views**: Click on chart elements to see detailed breakdowns
7. **Alerts/Notifications**: Set up alerts for specific thresholds
8. **Comparative Analysis**: Compare metrics across different time periods

### Performance Optimizations
1. Implement caching with Flask-Caching
2. Use database views for complex queries
3. Add pagination for large datasets
4. Implement lazy loading for charts
5. Optimize SQL queries with proper indexes

---

## Contact & Support

For questions or issues with this implementation:
- Review this guide first
- Check the Flask and Plotly documentation
- Examine existing code patterns in `app.py`
- Test changes in a development environment before deploying

---

**Last Updated**: 2026-04-14
**Version**: 1.0