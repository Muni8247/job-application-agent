#!/usr/bin/env python3
"""
Main entry point for the AI Job Application Agent
"""

import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.job_scraper import JobScraper
from agents.skill_matcher import SkillMatcher
from agents.applier import JobApplier
from services.email_service import EmailService
from services.logger import setup_logger
from services.database import Database
import json

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.error("config.json not found. Please create it from config.json.example")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in config.json")
        sys.exit(1)

def main():
    """Main execution flow"""
    logger.info("=" * 60)
    logger.info("Starting AI Job Application Agent")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize services
        database = Database()
        database.create_tables()
        
        email_service = EmailService()
        skill_matcher = SkillMatcher(config)
        
        # Initialize job scraper and applier
        job_scraper = JobScraper(config)
        job_applier = JobApplier(config, skill_matcher, email_service, database)
        
        # Scrape jobs from enabled platforms
        all_jobs = []
        
        if config['platforms'].get('naukri', {}).get('enabled', False):
            logger.info("Scraping Naukri...")
            try:
                naukri_jobs = job_scraper.scrape_naukri()
                all_jobs.extend(naukri_jobs)
                logger.info(f"Found {len(naukri_jobs)} jobs on Naukri")
            except Exception as e:
                logger.error(f"Error scraping Naukri: {str(e)}")
        
        if config['platforms'].get('linkedin', {}).get('enabled', False):
            logger.info("Scraping LinkedIn...")
            try:
                linkedin_jobs = job_scraper.scrape_linkedin()
                all_jobs.extend(linkedin_jobs)
                logger.info(f"Found {len(linkedin_jobs)} jobs on LinkedIn")
            except Exception as e:
                logger.error(f"Error scraping LinkedIn: {str(e)}")
        
        if config['platforms'].get('indeed', {}).get('enabled', False):
            logger.info("Scraping Indeed...")
            try:
                indeed_jobs = job_scraper.scrape_indeed()
                all_jobs.extend(indeed_jobs)
                logger.info(f"Found {len(indeed_jobs)} jobs on Indeed")
            except Exception as e:
                logger.error(f"Error scraping Indeed: {str(e)}")
        
        logger.info(f"Total jobs found: {len(all_jobs)}")
        
        if not all_jobs:
            logger.warning("No jobs found. Exiting.")
            return
        
        # Filter and match jobs
        logger.info("Matching jobs with your profile...")
        matched_jobs = []
        
        for job in all_jobs:
            match_score = skill_matcher.calculate_match_score(job)
            if match_score >= config['matching']['min_skill_match_percentage']:
                job['match_score'] = match_score
                matched_jobs.append(job)
        
        logger.info(f"Matched {len(matched_jobs)} jobs")
        
        if not matched_jobs:
            logger.info("No matching jobs found.")
            return
        
        # Apply to matched jobs
        logger.info("Applying to matched jobs...")
        applications = job_applier.apply_to_jobs(matched_jobs)
        
        logger.info("=" * 60)
        logger.info(f"Agent execution completed. Applied to {len(applications)} jobs.")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("Agent interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()