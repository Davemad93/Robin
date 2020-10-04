# Robin

A Simple Robinhood Python Trading Bot using RSI (buy <=20 and sell >=70 RSI) and with support and resistance.

Requirements

- Python >=3.5

# Setup/Installation

1. Fork/Clone the repository `git clone https://github.com/Davemad93/Robin.git`
2. pip install -r requirements.txt
3. Create a 'config.py' and add the environment variables below. 

```
# Example ENV

# Robinhood
USERNAME = "email"
PASSWORD = "password"
MFA = "Auth token"
GUSER = "email"
GPASS = "password"
EMAILS = "email_to_send_to"

# Poll data every 5 minutes
POLL_INTERVAL = "300"
```
4. Test run your project locally with `python robin.py`

# Integrations
- Yahoo Finance
- Robinhood Unofficial API (pyrh)
  · https://github.com/robinhood-unofficial/pyrh

# PIP Modules
View the [requirements.txt]https://github.com/Davemad93/Robin/blob/master/requirements.txt)