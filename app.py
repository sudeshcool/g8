from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime
import numpy as np
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_to_dataframe(query, params=None):
    """Execute SQL query and return pandas DataFrame"""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()

def create_pie_chart(labels, values, title):
    """Create a pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=['#0f62fe', '#4589ff', '#78a9ff', '#d0e2ff', '#002d9c', '#a6c8ff'])
    )])
    fig.update_layout(
        title=title,
        font=dict(family="IBM Plex Sans", size=12),
        showlegend=True,
        height=400
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_bar_chart(x, y, title, orientation='v'):
    """Create a bar chart"""
    fig = go.Figure(data=[go.Bar(
        x=x if orientation == 'v' else y,
        y=y if orientation == 'v' else x,
        orientation=orientation,
        marker=dict(color='#0f62fe')
    )])
    fig.update_layout(
        title=title,
        font=dict(family="IBM Plex Sans", size=12),
        xaxis_title=None,
        yaxis_title=None,
        height=400
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/service-requests')
def service_requests():
    """Service Requests Dashboard - Comprehensive analytics for Crest Workspace SR data"""
    try:
        # Load data from SQLite
        df = query_to_dataframe('SELECT * FROM crest_workspace')
        
        # Calculate statistics
        total_records = len(df)
        unique_service_types = df['Service Item'].nunique()
        unique_statuses = df['Status'].nunique()
        
        # Calculate average resolution time
        df['Created Date'] = pd.to_datetime(df['Created Date'])
        df['Resolved Date'] = pd.to_datetime(df['Resolved Date'])
        df['resolution_time'] = (df['Resolved Date'] - df['Created Date']).dt.total_seconds() / (3600 * 24)  # in days
        avg_resolution_time = round(df['resolution_time'].mean(), 2)
        
        # 1. Monthly Ticket Volume Trend
        df['year_month'] = pd.to_datetime(df['Created Date']).dt.to_period('M').astype(str)
        monthly_counts = df.groupby('year_month').size().reset_index(name='count')
        monthly_trend_data = {
            'data': [go.Bar(
                x=monthly_counts['year_month'].tolist(),
                y=monthly_counts['count'].tolist(),
                marker=dict(color='#0f62fe'),
                text=monthly_counts['count'].tolist(),
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Monthly Ticket Volume Trend',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Month',
                yaxis_title='Number of Tickets',
                height=400
            )
        }
        
        # 2. Top 10 Service Types by Volume
        service_type_counts = df['Service Item'].value_counts().head(10)
        top_service_types_data = {
            'data': [go.Bar(
                x=service_type_counts.values.tolist(),
                y=service_type_counts.index.tolist(),
                orientation='h',
                marker=dict(color='#ff832b'),
                text=service_type_counts.values.tolist(),
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Top 10 Service Types by Volume',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Number of Tickets',
                yaxis_title='Service Type',
                height=500,
                margin=dict(l=250)
            )
        }
        
        # 3. Average Resolution Time by Service Type (Top 10)
        resolution_by_service = df.groupby('Service Item')['resolution_time'].mean().sort_values(ascending=False).head(10)
        avg_resolution_data = {
            'data': [go.Bar(
                x=resolution_by_service.values.tolist(),
                y=resolution_by_service.index.tolist(),
                orientation='h',
                marker=dict(color=['#198038' if x < 5 else '#da1e28' if x > 10 else '#f1c21b' for x in resolution_by_service.values]),
                text=[f'{x:.1f}d' for x in resolution_by_service.values],
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Average Resolution Time by Service Type (Top 10)',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Average Days to Resolve',
                yaxis_title='Service Type',
                height=500,
                margin=dict(l=250)
            )
        }
        
        # 4. Ticket Status Distribution
        status_counts = df['Status'].value_counts()
        status_colors = {'Closed': '#198038', 'Open': '#da1e28', 'Pending': '#f1c21b', 'Approved': '#0f62fe'}
        status_data = {
            'data': [go.Pie(
                labels=status_counts.index.tolist(),
                values=status_counts.values.tolist(),
                hole=0.4,
                marker=dict(colors=[status_colors.get(s, '#0f62fe') for s in status_counts.index]),
                textinfo='label+percent',
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Ticket Status Distribution',
                font=dict(family="IBM Plex Sans"),
                height=400,
                showlegend=True
            )
        }
        
        # 5. Ticket Creation by Day of Week
        df['day_of_week'] = pd.to_datetime(df['Created Date']).dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
        day_of_week_data = {
            'data': [go.Bar(
                x=day_counts.index.tolist(),
                y=day_counts.values.tolist(),
                marker=dict(color='#8a3ffc'),
                text=day_counts.values.tolist(),
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Ticket Creation by Day of Week',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Day of Week',
                yaxis_title='Number of Tickets',
                height=400
            )
        }
        
        # 6. Ticket Creation by Hour of Day
        df['hour_of_day'] = pd.to_datetime(df['Created Date']).dt.hour
        hour_counts = df['hour_of_day'].value_counts().sort_index()
        hour_of_day_data = {
            'data': [go.Scatter(
                x=hour_counts.index.tolist(),
                y=hour_counts.values.tolist(),
                mode='lines+markers',
                line=dict(color='#ff832b', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(255, 131, 43, 0.2)'
            )],
            'layout': go.Layout(
                title='Ticket Creation by Hour of Day',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Hour of Day',
                yaxis_title='Number of Tickets',
                height=400,
                xaxis=dict(tickmode='linear', tick0=0, dtick=2)
            )
        }
        
        # 7. Resolution Time Distribution (histogram with 530 days limit)
        resolution_filtered = df[df['resolution_time'] <= 530]['resolution_time'].dropna()
        mean_resolution = resolution_filtered.mean()
        median_resolution = resolution_filtered.median()
        
        resolution_dist_data = {
            'data': [
                go.Histogram(
                    x=resolution_filtered.tolist(),
                    nbinsx=50,
                    marker=dict(color='#0f62fe'),
                    name='Frequency'
                )
            ],
            'layout': go.Layout(
                title='Resolution Time Distribution (≤530 days)',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Resolution Time (days)',
                yaxis_title='Frequency',
                height=400,
                shapes=[
                    dict(
                        type='line',
                        x0=mean_resolution,
                        x1=mean_resolution,
                        y0=0,
                        y1=1,
                        yref='paper',
                        line=dict(color='red', width=2, dash='dash'),
                        name=f'Mean: {mean_resolution:.1f}d'
                    ),
                    dict(
                        type='line',
                        x0=median_resolution,
                        x1=median_resolution,
                        y0=0,
                        y1=1,
                        yref='paper',
                        line=dict(color='green', width=2, dash='dash'),
                        name=f'Median: {median_resolution:.1f}d'
                    )
                ],
                annotations=[
                    dict(
                        x=mean_resolution,
                        y=1,
                        yref='paper',
                        text=f'Mean: {mean_resolution:.1f}d',
                        showarrow=True,
                        arrowhead=2,
                        ax=40,
                        ay=-40,
                        font=dict(color='red')
                    ),
                    dict(
                        x=median_resolution,
                        y=0.9,
                        yref='paper',
                        text=f'Median: {median_resolution:.1f}d',
                        showarrow=True,
                        arrowhead=2,
                        ax=-40,
                        ay=-40,
                        font=dict(color='green')
                    )
                ]
            )
        }
        
        # 8. Priority Distribution
        priority_counts = df['Priority'].value_counts()
        priority_colors = {'Low': '#198038', 'Medium': '#ff832b', 'High': '#da1e28'}
        priority_data = {
            'data': [go.Bar(
                x=priority_counts.index.tolist(),
                y=priority_counts.values.tolist(),
                marker=dict(color=[priority_colors.get(p, '#0f62fe') for p in priority_counts.index]),
                text=priority_counts.values.tolist(),
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Priority Distribution',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Priority Level',
                yaxis_title='Number of Tickets',
                height=400
            )
        }
        
        return render_template('service_requests.html',
                             total_records=total_records,
                             unique_service_types=unique_service_types,
                             unique_statuses=unique_statuses,
                             avg_resolution_time=avg_resolution_time,
                             monthly_trend_data=json.dumps(monthly_trend_data, cls=plotly.utils.PlotlyJSONEncoder),
                             top_service_types_data=json.dumps(top_service_types_data, cls=plotly.utils.PlotlyJSONEncoder),
                             avg_resolution_data=json.dumps(avg_resolution_data, cls=plotly.utils.PlotlyJSONEncoder),
                             status_data=json.dumps(status_data, cls=plotly.utils.PlotlyJSONEncoder),
                             day_of_week_data=json.dumps(day_of_week_data, cls=plotly.utils.PlotlyJSONEncoder),
                             hour_of_day_data=json.dumps(hour_of_day_data, cls=plotly.utils.PlotlyJSONEncoder),
                             resolution_dist_data=json.dumps(resolution_dist_data, cls=plotly.utils.PlotlyJSONEncoder),
                             priority_data=json.dumps(priority_data, cls=plotly.utils.PlotlyJSONEncoder))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("ERROR DETAILS:")
        print(error_details)
        return f"Error loading Service Requests data: {str(e)}<br><pre>{error_details}</pre>", 500

@app.route('/workplace-analytics')
@app.route('/export-category')
@app.route('/crest-workspace')
def workplace_analytics():
    """Unified Workplace Analytics Dashboard - Workplace-specific insights"""
    try:
        import traceback
        # Load data from SQLite
        df = query_to_dataframe('SELECT * FROM export_category')
        
        # Calculate statistics
        total_records = len(df)
        unique_categories = df['Category'].nunique()
        
        # Calculate resolution metrics
        df['Created Date'] = pd.to_datetime(df['Created Date'])
        df['Resolved Date'] = pd.to_datetime(df['Resolved Date'])
        df['resolution_time'] = (df['Resolved Date'] - df['Created Date']).dt.total_seconds() / 3600
        avg_resolution_time = round(df['resolution_time'].mean(), 2)
        
        # Extract country code from Agent Group Name
        df['Country'] = df['Agent Group Name'].str.split('-').str[0]
        
        # 1. Geographic Distribution - Country-wise ticket volume
        country_counts = df['Country'].value_counts()
        geo_data = {
            'data': [go.Bar(
                x=country_counts.index.tolist(),
                y=country_counts.values.tolist(),
                marker=dict(color='#0f62fe'),
                text=country_counts.values.tolist(),
                textposition='auto'
            )],
            'layout': go.Layout(
                title='Ticket Volume by Country',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Country',
                yaxis_title='Number of Tickets',
                showlegend=False
            )
        }
        
        # 2. Resolution Time by Category - Box plot showing distribution
        resolved_df = df[df['Resolved Date'].notna()].copy()
        resolved_df['resolution_days'] = resolved_df['resolution_time'] / 24
        
        category_resolution_data = {
            'data': [
                go.Box(
                    y=resolved_df[resolved_df['Category'] == cat]['resolution_days'],
                    name=cat,
                    boxmean='sd'
                ) for cat in df['Category'].unique()
            ],
            'layout': go.Layout(
                title='Resolution Time Distribution by Category (Days)',
                font=dict(family="IBM Plex Sans"),
                yaxis_title='Resolution Time (Days)',
                showlegend=True
            )
        }
        
        # 3. Agent Group Performance - Workload vs Avg Resolution Time
        agent_perf = df.groupby('Agent Group Name').agg({
            'ID': 'count',
            'resolution_time': 'mean'
        }).reset_index()
        agent_perf.columns = ['Agent Group', 'Ticket Count', 'Avg Resolution (hrs)']
        agent_perf = agent_perf.sort_values('Ticket Count', ascending=False).head(15)
        agent_perf['Avg Resolution (hrs)'] = agent_perf['Avg Resolution (hrs)'].fillna(0).round(2)
        
        agent_performance_data = {
            'data': [
                go.Bar(
                    name='Ticket Count',
                    x=agent_perf['Agent Group'].tolist(),
                    y=agent_perf['Ticket Count'].tolist(),
                    marker=dict(color='#0f62fe'),
                    yaxis='y'
                ),
                go.Scatter(
                    name='Avg Resolution Time (hrs)',
                    x=agent_perf['Agent Group'].tolist(),
                    y=agent_perf['Avg Resolution (hrs)'].tolist(),
                    marker=dict(color='#da1e28', size=10),
                    yaxis='y2',
                    mode='lines+markers'
                )
            ],
            'layout': go.Layout(
                title='Agent Group Workload vs Resolution Time',
                font=dict(family="IBM Plex Sans"),
                xaxis=dict(tickangle=-45),
                yaxis=dict(title='Ticket Count', side='left'),
                yaxis2=dict(title='Avg Resolution Time (hrs)', side='right', overlaying='y'),
                showlegend=True,
                legend=dict(x=0.01, y=0.99)
            )
        }
        
        # 4. Category Breakdown - Pie chart with percentages
        category_counts = df['Category'].value_counts()
        category_breakdown_data = {
            'data': [go.Pie(
                labels=category_counts.index.tolist(),
                values=category_counts.values.tolist(),
                hole=0.4,
                marker=dict(colors=['#0f62fe', '#8a3ffc', '#33b1ff']),
                textinfo='label+percent',
                textposition='outside'
            )],
            'layout': go.Layout(
                title='Workplace Ticket Distribution by Category',
                font=dict(family="IBM Plex Sans"),
                showlegend=True
            )
        }
        
        # 5. Monthly Trend by Category - Multi-line time series
        df_time = df.copy()
        df_time['year_month'] = pd.to_datetime(df_time['Created Date']).dt.to_period('M').astype(str)
        time_category_counts = df_time.groupby(['year_month', 'Category']).size().reset_index(name='count')
        
        traces = []
        colors = ['#0f62fe', '#8a3ffc', '#33b1ff']
        
        for idx, category in enumerate(df['Category'].unique()):
            cat_data = time_category_counts[time_category_counts['Category'] == category]
            traces.append(go.Scatter(
                x=cat_data['year_month'].tolist(),
                y=cat_data['count'].tolist(),
                mode='lines+markers',
                name=category,
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=6)
            ))
        
        time_series_data = {
            'data': traces,
            'layout': go.Layout(
                title='Monthly Ticket Trends by Category',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Month',
                yaxis_title='Number of Tickets',
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
        }
        
        # 6. Resolution Time Heatmap - Country vs Category
        heatmap_data = df.groupby(['Country', 'Category'])['resolution_time'].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='Country', columns='Category', values='resolution_time')
        heatmap_pivot = heatmap_pivot.fillna(0).round(2)
        
        resolution_heatmap_data = {
            'data': [go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns.tolist(),
                y=heatmap_pivot.index.tolist(),
                colorscale='Blues',
                text=heatmap_pivot.values,
                texttemplate='%{text:.1f}h',
                textfont={"size": 10},
                colorbar=dict(title="Hours")
            )],
            'layout': go.Layout(
                title='Average Resolution Time: Country vs Category (Hours)',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Category',
                yaxis_title='Country'
            )
        }
        
        # 7. Status Overview - Current workload
        status_counts = df['Status'].value_counts()
        status_data = {
            'data': [go.Bar(
                x=status_counts.index.tolist(),
                y=status_counts.values.tolist(),
                marker=dict(color=['#24a148', '#f1c21b', '#0f62fe', '#da1e28', '#8a3ffc']),
                text=status_counts.values.tolist(),
                textposition='auto'
            )],
            'layout': go.Layout(
                title='Current Ticket Status Distribution',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Status',
                yaxis_title='Count',
                showlegend=False
            )
        }
        
        # 8. SLA Performance - Resolution time buckets
        resolved_df['sla_bucket'] = pd.cut(
            resolved_df['resolution_days'],
            bins=[0, 1, 3, 7, 14, float('inf')],
            labels=['< 1 day', '1-3 days', '3-7 days', '7-14 days', '> 14 days']
        )
        sla_counts = resolved_df['sla_bucket'].value_counts().sort_index()
        
        sla_performance_data = {
            'data': [go.Bar(
                x=sla_counts.index.tolist(),
                y=sla_counts.values.tolist(),
                marker=dict(color=['#24a148', '#0f62fe', '#f1c21b', '#ff832b', '#da1e28']),
                text=sla_counts.values.tolist(),
                textposition='auto'
            )],
            'layout': go.Layout(
                title='Resolution Time Performance (SLA Buckets)',
                font=dict(family="IBM Plex Sans"),
                xaxis_title='Resolution Time',
                yaxis_title='Number of Tickets',
                showlegend=False
            )
        }
        
        # Summary metrics for cards
        open_tickets = len(df[df['Status'].isin(['Open', 'Pending', 'Work in Progress'])])
        closed_tickets = len(df[df['Status'] == 'Closed'])
        avg_resolution_days = round(avg_resolution_time / 24, 2)
        
        return render_template('export_category.html',
                             total_records=total_records,
                             unique_categories=unique_categories,
                             open_tickets=open_tickets,
                             closed_tickets=closed_tickets,
                             avg_resolution_time=avg_resolution_time,
                             avg_resolution_days=avg_resolution_days,
                             geo_data=json.dumps(geo_data, cls=plotly.utils.PlotlyJSONEncoder),
                             category_resolution_data=json.dumps(category_resolution_data, cls=plotly.utils.PlotlyJSONEncoder),
                             agent_performance_data=json.dumps(agent_performance_data, cls=plotly.utils.PlotlyJSONEncoder),
                             category_breakdown_data=json.dumps(category_breakdown_data, cls=plotly.utils.PlotlyJSONEncoder),
                             time_series_data=json.dumps(time_series_data, cls=plotly.utils.PlotlyJSONEncoder),
                             resolution_heatmap_data=json.dumps(resolution_heatmap_data, cls=plotly.utils.PlotlyJSONEncoder),
                             status_data=json.dumps(status_data, cls=plotly.utils.PlotlyJSONEncoder),
                             sla_performance_data=json.dumps(sla_performance_data, cls=plotly.utils.PlotlyJSONEncoder))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("ERROR DETAILS:")
        print(error_details)
        return f"Error loading Export Category data: {str(e)}<br><pre>{error_details}</pre>", 500

@app.route('/decisions', methods=['GET', 'POST'])
def decisions():
    """Decision Logic Tool"""
    result = None
    
    if request.method == 'POST':
        # Get form data
        location = float(request.form.get('location', 0))
        transport = float(request.form.get('transport', 0))
        building_size = float(request.form.get('building_size', 0))
        rental_cost = float(request.form.get('rental_cost', 0))
        lease_term = float(request.form.get('lease_term', 0))
        
        # Calculate amenities within building
        amenities_building = 0
        amenities_building += float(request.form.get('amenity_eot', 0))
        amenities_building += float(request.form.get('amenity_wellness', 0))
        amenities_building += float(request.form.get('amenity_prayer', 0))
        amenities_building += float(request.form.get('amenity_meeting', 0))
        amenities_building += float(request.form.get('amenity_coworking', 0))
        
        # Calculate amenities in vicinity
        amenities_vicinity = 0
        amenities_vicinity += float(request.form.get('vicinity_fnb', 0))
        amenities_vicinity += float(request.form.get('vicinity_retail', 0))
        amenities_vicinity += float(request.form.get('vicinity_gym', 0))
        amenities_vicinity += float(request.form.get('vicinity_bank', 0))
        amenities_vicinity += float(request.form.get('vicinity_childcare', 0))
        
        # Calculate weighted scores
        weights = {
            'location': 0.20,
            'amenities_building': 0.15,
            'amenities_vicinity': 0.15,
            'transport': 0.15,
            'building_size': 0.10,
            'rental_cost': 0.15,
            'lease_term': 0.10
        }
        
        # Normalize building size (assuming 20000-35000 sq ft range)
        size_score = min(10, (building_size / 3000))
        
        # Normalize rental cost (lower is better, assuming $5-$15 per sq ft range)
        cost_score = max(0, 10 - (rental_cost / 1.5))
        
        scores = {
            'location': location,
            'amenities_building': amenities_building,
            'amenities_vicinity': amenities_vicinity,
            'transport': transport,
            'building_size': size_score,
            'rental_cost': cost_score,
            'lease_term': lease_term
        }
        
        # Calculate weighted scores
        weighted_scores = {}
        for key in scores:
            weighted_scores[key] = round(scores[key] * weights[key] * 10, 2)
        
        total_score = round(sum(weighted_scores.values()), 2)
        
        # Create breakdown
        breakdown = [
            {'criteria': 'Location', 'weight': 20, 'raw_score': location, 'weighted_score': weighted_scores['location']},
            {'criteria': 'Building Amenities', 'weight': 15, 'raw_score': amenities_building, 'weighted_score': weighted_scores['amenities_building']},
            {'criteria': 'Vicinity Amenities', 'weight': 15, 'raw_score': amenities_vicinity, 'weighted_score': weighted_scores['amenities_vicinity']},
            {'criteria': 'Public Transport', 'weight': 15, 'raw_score': transport, 'weighted_score': weighted_scores['transport']},
            {'criteria': 'Building Size', 'weight': 10, 'raw_score': round(size_score, 2), 'weighted_score': weighted_scores['building_size']},
            {'criteria': 'Rental Cost', 'weight': 15, 'raw_score': round(cost_score, 2), 'weighted_score': weighted_scores['rental_cost']},
            {'criteria': 'Lease Flexibility', 'weight': 10, 'raw_score': lease_term, 'weighted_score': weighted_scores['lease_term']}
        ]
        
        result = {
            'total_score': total_score,
            'breakdown': breakdown
        }
    
    return render_template('decisions.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

# Made with Bob
