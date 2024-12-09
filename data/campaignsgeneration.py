import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Generate sample data for campaigns
campaigns = pd.DataFrame({
    'Campaign_ID': range(1, 11),
    'Impressions': np.random.randint(5000, 50000, 10),  
})

# Calculate realistic CTR values
ctr_values = np.random.uniform(0.001, 0.05, 10)  
clicks = campaigns['Impressions'] * ctr_values
clicks = clicks + np.random.choice([0, 10, 20, -10], size=10)  
campaigns['Clicks'] = clicks.clip(lower=0).astype(int)  

# Add Conversions and Spend
campaigns['Conversions'] = np.random.randint(5, 100, 10)  
efficiency_factors = np.random.choice([0.5, 1.0, 2.0], size=10, p=[0.3, 0.5, 0.2]) 
campaigns['Spend'] = campaigns['Conversions'] * np.random.uniform(50, 200, 10) * efficiency_factors

# Add Revenue with diversity
campaigns['Revenue'] = campaigns['Conversions'] * np.random.uniform(50, 300, 10)  
roi_factors = np.random.choice([0.5, 1.0, 2.0], size=10, p=[0.2, 0.6, 0.2])  
campaigns['Revenue'] = campaigns['Revenue'] * roi_factors

# Adjust Spend and Revenue for realism
campaigns['Spend'] = campaigns['Spend'].round(2)
campaigns['Revenue'] = campaigns['Revenue'].round(2)

# Add Campaign Status based on ROI (Revenue to Spend ratio)
roi = campaigns['Revenue'] / campaigns['Spend']
campaigns['Status'] = campaigns.apply(lambda row: 'Active' if roi[row.name] >= 1.5 else 'Paused', axis=1)

# Save to CSV
campaigns.to_csv('campaigns.csv', index=False)

# Display the updated dataset
print(campaigns)
