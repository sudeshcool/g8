# Azure Deployment Summary

## Deployment Date
2026-04-14

## Changes Deployed

### 1. Time Series Graph Enhancement
**File Modified**: `app.py` (lines 205-243)

**Change Description**:
Modified the "Tickets Over Time" graph in the Export Category dashboard to display separate lines for each category instead of a consolidated view.

**Technical Details**:
- Changed from daily to monthly aggregation
- Created separate Plotly traces for top 10 categories
- Each category has its own colored line
- Added legend for category identification
- Fixed Period object serialization issue by converting to string earlier in the process

**Code Change**:
```python
# Before: Consolidated view
df_time['date'] = pd.to_datetime(df_time['Created Date']).dt.date
time_counts = df_time.groupby('date').size().reset_index(name='count')

# After: Category-separated view
df_time['year_month'] = pd.to_datetime(df_time['Created Date']).dt.to_period('M').astype(str)
time_category_counts = df_time.groupby(['year_month', 'Category']).size().reset_index(name='count')
```

### 2. Bug Fix
**Issue**: JSON serialization error - "Object of type DataFrame is not JSON serializable"

**Root Cause**: Period objects from pandas were not being properly converted to strings before JSON serialization

**Solution**: Convert Period objects to strings immediately after creation using `.astype(str)`

## Database Analysis Results

### Workplace Health and Safety (74 tickets)
Top issues:
1. Standing desk requests - 4 tickets
2. Vehicle accidents - 2 tickets  
3. Weather-related incidents - 2 tickets
4. Individual health/safety concerns - remaining tickets

### Workplace Security (238 tickets)
Top issues:
1. Unattended laptops - 55 tickets (23%)
2. Badge deactivation for leaves - 37 tickets (16%)
3. Incident reports - 11 tickets (5%)
4. Badge reactivation - 4 tickets (2%)
5. Security door issues - 3 tickets (1%)

## Deployment Configuration

**Resource Group**: my-flask-rg
**App Service**: g8-app
**Location**: East Asia
**SKU**: B1
**App Service Plan**: my-flask-plan

## Deployment URL
https://g8-app.azurewebsites.net

## Dashboard URLs
- Home: https://g8-app.azurewebsites.net/
- Crest Workspace: https://g8-app.azurewebsites.net/crest-workspace
- Export Category: https://g8-app.azurewebsites.net/export-category
- Decisions: https://g8-app.azurewebsites.net/decisions

## Files Included in Deployment
- app.py (main application)
- requirements.txt (dependencies)
- data.db (SQLite database)
- templates/ (HTML templates)
- static/ (CSS, JS, images)
- startup.txt (gunicorn configuration)
- IMPLEMENTATION_GUIDE.md (documentation)
- convert_to_sqlite.py (utility script)

## Deployment Method
Azure CLI zip deployment:
```bash
az webapp deployment source config-zip \
  --resource-group my-flask-rg \
  --name g8-app \
  --src app.zip
```

## Post-Deployment Verification Steps
1. ✓ Check app service status (Running)
2. ⏳ Access Export Category dashboard
3. ⏳ Verify time series graph shows separate category lines
4. ⏳ Confirm monthly aggregation is working
5. ⏳ Test other dashboards for regressions

## Known Issues
None currently identified after bug fix.

## Next Steps
1. Monitor application logs for any runtime errors
2. Gather user feedback on the new visualization
3. Consider adding date range filters for better data exploration
4. Evaluate performance with larger datasets

## Rollback Plan
If issues arise, redeploy previous version:
```bash
# Restore from previous deployment slot or
# Redeploy previous app.zip version
```

## Support Contacts
- Azure Subscription: Pay-As-You-Go (ca1e6b7d-7b60-4b42-9263-5ebf88134ddf)
- Tenant: sudeshkmsn.onmicrosoft.com

## Additional Documentation
- See IMPLEMENTATION_GUIDE.md for detailed implementation notes
- See app.py for code comments and structure
- See requirements.txt for dependency versions