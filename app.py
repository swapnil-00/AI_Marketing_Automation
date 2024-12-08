import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
import os
from typing import Dict, Any

# Custom Styling and Configuration
st.set_page_config(
    page_title="Marketing Campaign Analytics", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

class MarketingDashboard:
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize the marketing dashboard with parsed data
        
        Args:
            data (dict): Parsed marketing report data
        """
        self.data = data
        self.setup_custom_styling()

    def setup_custom_styling(self):
        """Set up custom CSS for enhanced dashboard styling"""
        st.markdown("""
        <style>
        /* Global Styling */
        body {
            background-color: #f4f6f9;
            color: #333;
        }
        
        /* Card Styling */
        .metric-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: scale(1.03);
        }
        
        /* Typography */
        .metric-value {
            font-size: 2.5em;
            color: #2c3e50;
            font-weight: bold;
        }
        .metric-label {
            font-size: 1em;
            color: #7f8c8d;
            text-transform: uppercase;
        }
        
        /* Responsive Design */
        @media (max-width: 600px) {
            .metric-value { font-size: 1.5em; }
            .metric-label { font-size: 0.8em; }
        }
        </style>
        """, unsafe_allow_html=True)

    def create_performance_overview(self):
        """
        Create a comprehensive performance overview section
        
        Displays key performance metrics in an attractive card layout
        """
        st.header("📊 Performance Overview")
        
        performance_summary = self.data['performance_summary']
        col1, col2, col3 = st.columns(3)
        
        metrics = {
            'Total Spend': f"${performance_summary['total_spend']:,.2f}",
            'Total Revenue': f"${performance_summary['total_revenue']:,.2f}",
            'Average ROAS': f"{performance_summary['average_roas']:.2f}"
        }
        
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        
        for (metric, value), col, color in zip(metrics.items(), [col1, col2, col3], colors):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 5px solid {color};">
                    <div class="metric-label">{metric}</div>
                    <div class="metric-value" style="color: {color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)

    def create_campaign_status_visualization(self):
        """
        Visualize campaign status with interactive charts
        """
        st.header("🚦 Campaign Status Breakdown")
        
        total_campaigns = self.data['total_campaigns']
        paused_campaigns = self.data['campaign_actions']['pause_campaigns']
        active_campaigns = total_campaigns - len(paused_campaigns)
        
        # Status Pie Chart
        status_data = {
            'Active Campaigns': active_campaigns,
            'Paused Campaigns': len(paused_campaigns)
        }
        
        fig = px.pie(
            values=list(status_data.values()), 
            names=list(status_data.keys()),
            title='Campaign Status Distribution',
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Campaign Status Table
        if paused_campaigns:
            st.subheader("🛑 Paused Campaigns Details")
            pause_df = pd.DataFrame(paused_campaigns)
            st.dataframe(pause_df, use_container_width=True)

    def create_campaign_performance_analysis(self):
        """
        Comprehensive campaign performance analysis
        """
        st.header("📈 Campaign Performance Analysis")
        
        # Top Performing Campaigns
        top_campaigns = self.data['campaign_insights']['top_performing_campaigns']
        
        fig_top = px.bar(
            x=[f'Campaign {camp}' for camp in top_campaigns], 
            y=top_campaigns,
            title='Top Performing Campaigns',
            labels={'x': 'Campaign', 'y': 'Performance Score'},
            color_discrete_sequence=['#3498db']
        )
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Campaign Actions Overview
        st.subheader("🔄 Campaign Budget Actions")
        
        actions = {
            'Paused Campaigns': len(self.data['campaign_actions']['pause_campaigns']),
            'Budget Increased': len(self.data['campaign_actions']['increase_budget']),
            'Budget Decreased': len(self.data['campaign_actions']['decrease_budget'])
        }
        
        fig_actions = px.bar(
            x=list(actions.keys()), 
            y=list(actions.values()),
            title='Campaign Budget Action Distribution',
            labels={'x': 'Action Type', 'y': 'Number of Campaigns'}
        )
        st.plotly_chart(fig_actions, use_container_width=True)
        
        # Detailed Budget Action Tables
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Campaigns with Budget Increase")
            if self.data['campaign_actions']['increase_budget']:
                increase_df = pd.DataFrame(self.data['campaign_actions']['increase_budget'])
                st.dataframe(increase_df, use_container_width=True)
            else:
                st.write("No campaigns had budget increases")
        
        with col2:
            st.subheader("📉 Campaigns with Budget Decrease")
            if self.data['campaign_actions']['decrease_budget']:
                decrease_df = pd.DataFrame(self.data['campaign_actions']['decrease_budget'])
                st.dataframe(decrease_df, use_container_width=True)
            else:
                st.write("No campaigns had budget decreases")

    def display_campaign_recommendations(self):
        """
        Display campaign-specific recommendations
        """
        st.header("🎯 Campaign Optimization Recommendations")
        
        for insight in self.data['campaign_actions']['insights']:
            with st.expander(f"Campaign {insight['Campaign_ID']} Recommendations"):
                st.markdown(insight['Recommendation'])

def load_marketing_data(file_path: str = 'reports\marketing_report.json') -> Dict[str, Any]:
    """
    Load marketing data from JSON file with error handling
    
    Args:
        file_path (str): Path to the marketing report JSON file
    
    Returns:
        dict: Parsed marketing report data
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Error: File {file_path} not found. Please check the file path.")
        return {}
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON format in the marketing report file.")
        return {}

def main():
    """
    Main function to run the Streamlit marketing dashboard
    """
    st.title("🚀 AI Marketing Campaign Dashboard")
    
    # Load marketing data
    data = load_marketing_data()
    
    if data:
        # Initialize dashboard
        dashboard = MarketingDashboard(data)
        
        # Render dashboard sections
        dashboard.create_performance_overview()
        dashboard.create_campaign_status_visualization()
        dashboard.create_campaign_performance_analysis()
        dashboard.display_campaign_recommendations()
    else:
        st.warning("Unable to load marketing data. Please check your data source.")

if __name__ == "__main__":
    main()