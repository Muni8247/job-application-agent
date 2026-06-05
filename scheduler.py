#!/usr/bin/env python3
"""
Scheduler for running the job application agent at regular intervals
"""

import schedule
import time
import logging
import json
import subprocess
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error("config.json not found")
        sys.exit(1)

def run_agent():
    """Run the main job application agent"""
    logger.info("=" * 60)
    logger.info(f"Running job application agent at {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, 'main.py'], capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0:
            logger.info("Agent execution completed successfully")
        else:
            logger.error(f"Agent execution failed with return code {result.returncode}")
            logger.error(f"Stderr: {result.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("Agent execution timed out after 1 hour")
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}", exc_info=True)

def main():
    """Main scheduler loop"""
    logger.info("=" * 60)
    logger.info("Job Application Agent Scheduler Started")
    logger.info("=" * 60)
    
    config = load_config()
    
    if not config['scheduler'].get('enabled', False):
        logger.info("Scheduler is disabled in configuration")
        sys.exit(0)
    
    interval = config['scheduler'].get('interval_hours', 6)
    logger.info(f"Scheduling agent to run every {interval} hour(s)")
    schedule.every(interval).hours.do(run_agent)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()