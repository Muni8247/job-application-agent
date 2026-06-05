#!/usr/bin/env python3
"""
Database service for tracking applications
"""

import sqlite3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Database:
    """SQLite database for application tracking"""
    
    def __init__(self, db_path='applications.db'):
        self.db_path = db_path
        self.connection = None
        self._connect()
    
    def _connect(self):
        """Connect to database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database error: {str(e)}")
    
    def create_tables(self):
        """Create necessary tables"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT,
                    company TEXT,
                    platform TEXT,
                    job_url TEXT UNIQUE,
                    match_score REAL,
                    applied_date REAL,
                    status TEXT DEFAULT 'Applied',
                    notes TEXT
                )
            ''')
            
            self.connection.commit()
            logger.info("Database tables created")
        
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {str(e)}")
    
    def add_application(self, job_title, company, platform, job_url, match_score, applied_date):
        """Add new application record"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO applications 
                (job_title, company, platform, job_url, match_score, applied_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (job_title, company, platform, job_url, match_score, applied_date, 'Applied'))
            
            self.connection.commit()
            logger.info(f"Application recorded: {job_title}")
            return True
        
        except sqlite3.IntegrityError:
            logger.warning(f"Application already exists")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error: {str(e)}")
            return False
    
    def has_applied(self, job_url):
        """Check if already applied"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id FROM applications WHERE job_url = ?', (job_url,))
            return cursor.fetchone() is not None
        except sqlite3.Error:
            return False
    
    def close(self):
        """Close database"""
        try:
            if self.connection:
                self.connection.close()
        except sqlite3.Error:
            pass