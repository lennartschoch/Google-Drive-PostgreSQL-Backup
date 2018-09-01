# Google Drive PostgreSQL Backup

I build this script to find a simple and cost-efficient way of storing PostgreSQL database dumps on a regular basis. I set up a cronjob, which executes the script every 24 hours.

## Prerequisites

1. Create a new project on the Google Cloud console and activate the Google Drive API. Download the credentials and save save as token.json.
2. Run auth.py to authenticate to Google Drive
3. Rename .env.example to .env
4. Set the environment variables (the ID of your Google Drive folder is the last part of its URL)

