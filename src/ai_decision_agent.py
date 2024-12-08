import pandas as pd
import json
import logging
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv
import os


class AIDecisionAgent:
    def __init__(self, config_path='config/settings.json'):
        # Load configuration from JSON
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        load_dotenv()
        key = os.getenv('API_KEY')
        genai.configure(api_key=key)

        # Set up logger
        logging.basicConfig(
            filename='logs/marketing_automation.log',
            level=getattr(logging, self.config['logging']['log_level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_campaigns_data(self, file_path: str) -> pd.DataFrame:
        """
        Load campaign data from CSV file and calculate necessary metrics.
        """
        try:
            campaigns_df = pd.read_csv(file_path)

            # Ensure necessary columns exist
            required_columns = ['Campaign_ID', 'Impressions', 'Clicks', 'Conversions', 'Spend', 'Revenue']
            for col in required_columns:
                if col not in campaigns_df.columns:
                    self.logger.error(f"Missing required column: {col}")
                    raise ValueError(f"Missing required column: {col}")

            # Calculate CTR (Click-Through Rate)
            campaigns_df['CTR'] = campaigns_df['Clicks'] / campaigns_df['Impressions']

            # Calculate CPA (Cost per Acquisition)
            campaigns_df['CPA'] = campaigns_df['Spend'] / campaigns_df['Conversions']

            # Calculate ROAS (Return on Ad Spend)
            campaigns_df['ROAS'] = campaigns_df['Revenue'] / campaigns_df['Spend']

            self.logger.info(f"Successfully loaded and processed {file_path}")
            return campaigns_df

        except Exception as e:
            self.logger.error(f"Error loading campaigns data from {file_path}: {e}")
            raise



    def generate_recommendations(self, issue: str, metrics: Dict) -> str:
        """
        Use Gemini AI to generate dynamic, short, and actionable recommendations based on the issue and campaign metrics.
        """
        # Extract key campaign metrics from the dictionary
        spend = metrics.get('Spend', 0)
        impressions = metrics.get('Impressions', 0)
        clicks = metrics.get('Clicks', 0)
        conversions = metrics.get('Conversions', 0)
        revenue = metrics.get('Revenue', 0)

        # Calculate key ratios if they exist
        ctr = clicks / impressions if impressions > 0 else 0
        roas = revenue / spend if spend > 0 else 0
        cpa = spend / conversions if conversions > 0 else 0

        # Create a dynamic prompt based on the campaign metrics
        prompt = f"""
        A marketing campaign is facing the following issue: {issue}.
        Here are the campaign's key metrics:
        - Spend: ${spend}
        - Impressions: {impressions}
        - Clicks: {clicks}
        - Conversions: {conversions}
        - Revenue: ${revenue}
        - CTR: {ctr*100:.2f}% (Click-Through Rate)
        - ROAS: {roas:.2f} (Return on Ad Spend)
        - CPA: ${cpa:.2f} (Cost Per Acquisition)

        Please provide short, actionable recommendations in bullet points to resolve this issue and improve the campaign's performance. Consider the specific metrics provided and focus on high-impact actions tailored to these values.
        Be concise and suggest actions based on the following:
        - Low CTR (below 1% is a concern).
        - Low ROAS (below 2.0 suggests inefficiency).
        - High CPA (above $50 may need adjustment).
        - High spend with low conversions (could indicate a need to optimize targeting).
        """
        
        try:
            # Generate recommendations using Gemini
            response = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt)
            recommendation = response.text.strip()

            # Post-process the response to make it more concise and formatted as bullet points
            recommendation_lines = recommendation.split("\n")
            concise_recommendation = "\n".join([line.strip() for line in recommendation_lines if line.strip()])
            
            # If recommendations are too long, limit them to 5 concise points
            max_lines = 5  # Limit to 5 concise recommendations
            concise_recommendation = "\n".join(concise_recommendation.splitlines()[:max_lines])

            return concise_recommendation

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return "Unable to generate recommendations due to an error."


    def decide_campaign_actions(self, campaigns_df: pd.DataFrame) -> Dict[str, List[Dict]]:
        """
        Decide actions for campaigns based on predefined rules.
        """
        actions = {
            'pause_campaigns': [],
            'increase_budget': [],
            'decrease_budget': [],
            'insights': []
        }

        try:
            for _, campaign in campaigns_df.iterrows():
                metrics = {
                    "CTR": campaign['CTR'],
                    "CPA": campaign['CPA'],
                    "ROAS": campaign['ROAS'],
                    "Impressions": campaign['Impressions'],
                    "Clicks": campaign['Clicks'],
                    "Conversions": campaign['Conversions'],
                    "Spend": campaign['Spend'],
                    "Revenue": campaign['Revenue']
                }

                # Rule 1: Pause Campaign
                if (campaign['CTR'] < self.config['optimization_rules']['pause_campaign']['ctr_threshold'] and 
                    campaign['CPA'] > self.config['optimization_rules']['pause_campaign']['cpa_multiplier'] * self.config['target_cpa']):
                    actions['pause_campaigns'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Reason': 'Low CTR or High CPA'
                    })
                    recommendation = self.generate_recommendations("Low CTR or High CPA", metrics)
                    actions['insights'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Recommendation': recommendation
                    })
                    self.logger.info(f"Campaign {campaign['Campaign_ID']} paused: Low CTR or High CPA.")

                # Rule 2: Increase Budget
                if (campaign['ROAS'] > self.config['optimization_rules']['increase_budget']['roas_threshold'] or 
                    campaign['Conversions'] > campaign['Conversions'] * (1 + self.config['optimization_rules']['increase_budget']['conversion_increase'])):
                    actions['increase_budget'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Reason': 'High ROAS or Significant Conversion Growth'
                    })
                    recommendation = self.generate_recommendations("High ROAS or Significant Conversion Growth", metrics)
                    actions['insights'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Recommendation': recommendation
                    })
                    self.logger.info(f"Campaign {campaign['Campaign_ID']} budget increased: High ROAS or Significant Conversion Growth.")

                # Rule 3: Decrease Budget
                if campaign['ROAS'] < self.config['optimization_rules']['decrease_budget']['roas_threshold']:
                    actions['decrease_budget'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Reason': 'Low ROAS'
                    })
                    recommendation = self.generate_recommendations("Low ROAS", metrics)
                    actions['insights'].append({
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Recommendation': recommendation
                    })
                    self.logger.info(f"Campaign {campaign['Campaign_ID']} budget decreased: Low ROAS.")

            self.logger.info("Successfully decided campaign actions")
            return actions

        except KeyError as ke:
            self.logger.error(f"Missing column in input data: {ke}")
            raise
        except Exception as e:
            self.logger.error(f"Error in deciding campaign actions: {e}")
            raise

# Example usage
if __name__ == "__main__":
    agent = AIDecisionAgent()

    # Load campaigns data
    campaigns_df = agent.load_campaigns_data('campaigns.csv')

    # Decide campaign actions based on the data
    actions = agent.decide_campaign_actions(campaigns_df)

    # Save insights and actions
    with open(agent.config['reporting']['report_path'], 'w') as report_file:
        json.dump(actions, report_file, indent=4)

    # Print the actions for demonstration
    print(json.dumps(actions, indent=4))
