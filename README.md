# OSINT Duniya

A Python-based osint duniya tool that uses the OSINT Industries API to search for usernames, emails, and phone numbers. This tool generates a unique virtual user ID and device ID for each user and supports session cookies and user-agent headers for API requests.

## Features
- Search for user details using a username, email, or phone number.
- Automatically generates a virtual user ID and device ID for each user.
- Supports session cookies and user-agent headers.
- Fetches and displays images related to the search results, if available.

## Prerequisites
- Python 3.x
- OSINT Industries API Key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sinchop100/osintduniya.git
cd osintduniya
pip install -r requirements.txt
python osint_search.py
