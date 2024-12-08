import logging
from src.data_loader import DataLoader
from src.metrics_calculator import MetricsCalculator
from src.ai_decision_agent import AIDecisionAgent
from src.action_executor import ActionExecutor
from src.reporting import Reporting
import json
from tqdm import tqdm
import time

def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/marketing_automation.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Marketing Automation Pipeline")

        # Step 1: Load Data
        logger.info("Loading campaign and historical data...")
        data_loader = DataLoader()
        campaigns_df = data_loader.load_campaigns()
        historical_df = data_loader.load_historical_data()

        # Adding a progress bar for loading data
        for _ in tqdm(range(1), desc="Loading Data", ncols=100):
            time.sleep(1)  # Simulating work done in the loading process

        # Step 2: Calculate Metrics
        logger.info("Calculating metrics...")
        metrics_calculator = MetricsCalculator()
        campaigns_df = metrics_calculator.calculate_metrics(campaigns_df)
        insights = metrics_calculator.analyze_trends(historical_df)

        for _ in tqdm(range(1), desc="Calculating Metrics", ncols=100):
            time.sleep(1)

        # Step 3: AI Decision Making
        logger.info("AI making decisions on campaign actions...")
        decision_agent = AIDecisionAgent()
        campaign_actions = decision_agent.decide_campaign_actions(campaigns_df)

        for _ in tqdm(range(1), desc="AI Decision Making", ncols=100):
            time.sleep(1)

        # Step 4: Execute Actions
        logger.info("Executing campaign actions...")
        action_executor = ActionExecutor()
        updated_campaigns_df = action_executor.execute_actions(campaigns_df, campaign_actions)

        for _ in tqdm(range(1), desc="Executing Actions", ncols=100):
            time.sleep(1)

        # Step 5: Generate Reports
        logger.info("Generating reports...")
        reporting = Reporting()
        reporting.generate_report(updated_campaigns_df, campaign_actions, insights)

        for _ in tqdm(range(1), desc="Generating Report", ncols=100):
            time.sleep(1)

        logger.info("Marketing Automation Pipeline Completed Successfully")

    except Exception as e:
        logger.error(f"Marketing Automation Pipeline Failed: {e}")

if __name__ == "__main__":
    main()
