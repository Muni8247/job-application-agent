#!/usr/bin/env python3
"""
Job scraper for Naukri, LinkedIn, and Indeed
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

class JobScraper:
    """Scrapes job listings from multiple platforms"""
    
    def __init__(self, config):
        self.config = config
        self.ua = UserAgent()
        self.jobs = []
    
    def get_chrome_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"user-agent={self.ua.random}")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            return None
    
    def scrape_naukri(self):
        """Scrape jobs from Naukri.com"""
        logger.info("Scraping Naukri...")
        jobs = []
        
        try:
            driver = self.get_chrome_driver()
            if not driver:
                return jobs
            
            user_profile = self.config['user_profile']
            skills_query = ','.join(user_profile['skills'][:3])
            location_query = user_profile['locations'][0]
            
            url = f"https://www.naukri.com/search?k={skills_query}&l={location_query}"
            
            logger.info(f"Fetching: {url}")
            driver.get(url)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "jobTuple"))
                )
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('article', class_='jobTuple')
                logger.info(f"Found {len(job_cards)} job cards on Naukri")
            except:
                logger.warning("Could not load Naukri jobs")
            
            driver.quit()
        
        except Exception as e:
            logger.error(f"Error scraping Naukri: {str(e)}")
        
        return jobs
    
    def scrape_linkedin(self):
        """Scrape jobs from LinkedIn"""
        logger.info("Scraping LinkedIn...")
        jobs = []
        
        try:
            driver = self.get_chrome_driver()
            if not driver:
                return jobs
            
            logger.warning("LinkedIn requires authentication. Skipping.")
            driver.quit()
        
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {str(e)}")
        
        return jobs
    
    def scrape_indeed(self):
        """Scrape jobs from Indeed.com"""
        logger.info("Scraping Indeed...")
        jobs = []
        
        try:
            driver = self.get_chrome_driver()
            if not driver:
                return jobs
            
            user_profile = self.config['user_profile']
            skills_query = '+'.join(user_profile['skills'][:2])
            location_query = user_profile['locations'][0].replace(' ', '+')
            
            url = f"https://www.indeed.com/jobs?q={skills_query}&l={location_query}"
            
            logger.info(f"Fetching: {url}")
            driver.get(url)
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            logger.info("Indeed scraping completed")
            
            driver.quit()
        
        except Exception as e:
            logger.error(f"Error scraping Indeed: {str(e)}")
        
        return jobs