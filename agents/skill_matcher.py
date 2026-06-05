#!/usr/bin/env python3
"""
AI-powered skill matcher for job profiles
"""

import logging

logger = logging.getLogger(__name__)

class SkillMatcher:
    """Matches job requirements with user skills"""
    
    def __init__(self, config):
        self.config = config
        self.user_skills = set(s.lower() for s in config['user_profile']['skills'])
        self.min_match = config['matching']['min_skill_match_percentage']
    
    def calculate_match_score(self, job):
        """Calculate match score between job and user profile"""
        
        # Skill matching (40% weight)
        skill_score = self._match_skills(job) * 40
        
        # Location matching (25% weight)
        location_score = self._match_location(job) * 25
        
        # Experience matching (20% weight)
        experience_score = self._match_experience(job) * 20
        
        # Job title matching (15% weight)
        title_score = self._match_job_title(job) * 15
        
        total_score = skill_score + location_score + experience_score + title_score
        
        return max(0, min(100, total_score))
    
    def _match_skills(self, job):
        """Match job required skills with user skills"""
        
        job_description = f"{job.get('title', '')} {job.get('description', '')}".lower()
        
        if not job_description or job_description == " ":
            return 0.5
        
        matched_skills = 0
        
        for user_skill in self.user_skills:
            if user_skill in job_description:
                matched_skills += 1
        
        skill_match_percentage = (matched_skills / len(self.user_skills)) * 100 if self.user_skills else 0
        
        return min(100, skill_match_percentage) / 100
    
    def _match_location(self, job):
        """Match job location with user location preferences"""
        
        job_location = job.get('location', '').lower()
        user_locations = [loc.lower() for loc in self.config['user_profile']['locations']]
        
        if 'remote' in job_location:
            if 'remote' in user_locations or 'work from home' in user_locations:
                return 1.0
        
        for user_loc in user_locations:
            if user_loc in job_location or job_location in user_loc:
                return 1.0
        
        if any(part in job_location for loc in user_locations for part in loc.split()):
            return 0.5
        
        return 0.3
    
    def _match_experience(self, job):
        """Match job experience requirement with user experience"""
        
        user_exp = self.config['user_profile']['experience_years']
        tolerance = self.config['matching'].get('experience_tolerance_years', 1)
        
        exp_text = job.get('experience', '').lower()
        
        if not exp_text or 'n/a' in exp_text:
            return 1.0
        
        try:
            import re
            numbers = re.findall(r'\d+', exp_text)
            
            if numbers:
                required_exp = int(numbers[0])
                diff = abs(user_exp - required_exp)
                
                if diff == 0:
                    return 1.0
                elif diff <= tolerance:
                    return 0.8
                elif diff <= tolerance * 2:
                    return 0.5
                else:
                    return 0.2
        except Exception as e:
            logger.debug(f"Could not parse experience: {str(e)}")
        
        return 0.7
    
    def _match_job_title(self, job):
        """Match job title with user preferred job titles"""
        
        job_title = job.get('title', '').lower()
        preferred_titles = [title.lower() for title in self.config['user_profile']['job_titles']]
        
        for title in preferred_titles:
            if title in job_title or job_title in title:
                return 1.0
        
        title_words = job_title.split()
        preferred_words = set()
        for title in preferred_titles:
            preferred_words.update(title.split())
        
        matched_words = len(set(title_words) & preferred_words)
        total_words = len(set(title_words) | preferred_words)
        
        if total_words > 0:
            similarity = matched_words / total_words
            return min(1.0, similarity + 0.3)
        
        return 0.5