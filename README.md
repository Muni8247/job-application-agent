# AI Job Application Agent

An intelligent automation agent that applies to jobs on Naukri, LinkedIn, and Indeed based on your skill set, experience, location preferences, and sends email notifications for each application.

## Features

- 🤖 **AI-Powered Matching**: Uses NLP to match job requirements with your skills
- 🔍 **Multi-Platform Support**: Scrapes jobs from Naukri, LinkedIn, and Indeed
- 📧 **Email Notifications**: Get instant updates on applications sent
- ⚙️ **Customizable Filters**: Filter by location, experience, salary, skills
- 🔐 **Secure Credentials**: Environment-based configuration
- 📊 **Application Tracking**: Logs all applications for reference

## Tech Stack

- **Python 3.9+**
- **Selenium**: Web automation and scraping
- **LangChain**: AI-powered skill matching
- **OpenAI**: NLP for job matching
- **SMTP**: Email notifications
- **SQLite**: Application tracking database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Muni8247/job-application-agent.git
cd job-application-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Install ChromeDriver for Selenium:
```bash
# Download from: https://chromedriver.chromium.org/
# Or use: pip install webdriver-manager
```

## Configuration

Edit `config.json` with your preferences:

```json
{
  "user_profile": {
    "skills": ["Python", "Machine Learning", "Data Science"],
    "experience_years": 3,
    "locations": ["Bangalore", "Hyderabad", "Remote"],
    "salary_min": 500000,
    "job_titles": ["Data Scientist", "ML Engineer", "AI Developer"]
  },
  "platforms": {
    "naukri": true,
    "linkedin": true,
    "indeed": true
  },
  "notification": {
    "email_enabled": true,
    "send_daily_summary": true
  }
}
```

## Environment Variables

Create a `.env` file:

```
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# OpenAI API (for skill matching)
OPENAI_API_KEY=sk-xxx

# Job Platforms (optional)
NAUKRI_EMAIL=your-naukri-email@gmail.com
NAUKRI_PASSWORD=your-naukri-password
LINKEDIN_EMAIL=your-linkedin-email@gmail.com
LINKEDIN_PASSWORD=your-linkedin-password
INDEED_EMAIL=your-indeed-email@gmail.com
INDEED_PASSWORD=your-indeed-password

# Notification Email
NOTIFICATION_EMAIL=your-email@gmail.com
```

## Usage

Run the agent:

```bash
python main.py
```

For scheduling (runs every 6 hours):

```bash
python scheduler.py
```

## Project Structure

```
job-application-agent/
├── main.py                 # Main entry point
├── scheduler.py           # Scheduled execution
├── config.json            # User configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── agents/
│   ├── __init__.py
│   ├── job_scraper.py    # Web scraping logic
│   ├── skill_matcher.py  # AI skill matching
│   └── applier.py        # Application automation
├── platforms/
│   ├── __init__.py
│   ├── naukri.py         # Naukri platform handler
│   ├── linkedin.py       # LinkedIn platform handler
│   └── indeed.py         # Indeed platform handler
├── services/
│   ├── __init__.py
│   ├── email_service.py  # Email notifications
│   ├── database.py       # SQLite operations
│   └── logger.py         # Logging setup
└── tests/
    ├── __init__.py
    └── test_matcher.py   # Unit tests
```

## Security Notes

⚠️ **Important**: 
- Never commit `.env` file to repository
- Use app-specific passwords for Gmail
- Keep API keys secure
- Consider using GitHub Secrets for CI/CD

## Troubleshooting

- **ChromeDriver issues**: Use `webdriver-manager` for automatic driver management
- **Email not sending**: Check Gmail app password and enable "Less secure app access"
- **LinkedIn blocking**: Add delays between requests and use rotating user agents
- **Job matching too loose/strict**: Adjust similarity threshold in `skill_matcher.py`

## Contributing

Feel free to open issues and submit PRs for improvements!

## License

MIT License

## Disclaimer

This tool is for educational purposes. Ensure you comply with each platform's Terms of Service before automation.
