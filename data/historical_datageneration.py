import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Number of campaigns and days for historical data
num_campaigns = 10
days = 30

# Generate campaign IDs
campaign_ids = range(1, num_campaigns + 1)

# Generate a date range
date_range = pd.date_range(end=pd.Timestamp.today(), periods=days)

# Create historical data
historical_data = []

for campaign_id in campaign_ids:
    # Generate base metrics for the campaign
    base_impressions = np.random.randint(5000, 50000)
    base_ctr = np.random.uniform(0.005, 0.05)  # CTR between 0.5% and 5%
    base_clicks = int(base_impressions * base_ctr)
    base_conversions = np.random.randint(5, 100)
    efficiency_factor = np.random.choice([0.5, 1.0, 2.0], p=[0.3, 0.5, 0.2])  # Efficiency categories
    base_spend = base_conversions * np.random.uniform(50, 200) * efficiency_factor
    roi_factor = np.random.choice([0.5, 1.0, 2.0], p=[0.2, 0.6, 0.2])  # ROI categories
    base_revenue = base_conversions * np.random.uniform(50, 300) * roi_factor

    for date in date_range:
        # Simulate daily variations
        impressions = int(base_impressions * np.random.uniform(0.8, 1.2))
        ctr = np.random.uniform(0.005, 0.05)  # Recalculate CTR for daily variation
        clicks = min(int(impressions * ctr), impressions)
        conversions = min(int(base_conversions * np.random.uniform(0.8, 1.2)), clicks)
        spend = base_spend * np.random.uniform(0.8, 1.2)
        revenue = base_revenue * np.random.uniform(0.8, 1.2)
        
        # Calculate derived metrics
        ctr_calculated = clicks / impressions if impressions > 0 else 0  # CTR
        roas = revenue / spend if spend > 0 else 0  # ROAS
        cpa = spend / conversions if conversions > 0 else 0  # CPA
        
        # Determine status based on ROI (Revenue/Spend ratio)
        roi = revenue / spend
        status = 'Active' if roi >= 1.5 else 'Paused'

        # Append record
        historical_data.append({
            'Date': date,
            'Campaign_ID': campaign_id,
            'Impressions': impressions,
            'Clicks': clicks,
            'Conversions': conversions,
            'Spend': round(spend, 2),
            'Revenue': round(revenue, 2),
            'CTR': round(ctr_calculated, 4),
            'ROAS': round(roas, 4),
            'CPA': round(cpa, 2),
            'Status': status
        })

# Convert to DataFrame
historical_df = pd.DataFrame(historical_data)

# Save to CSV
historical_df.to_csv('historical_data.csv', index=False)

print(historical_df.head(10))
