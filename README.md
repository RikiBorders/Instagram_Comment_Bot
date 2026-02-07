# README

# Overview:

An autonomous Instagram comment bot that leverages selenium's headless browser and automation features to scrape Instagram, leaving comments on posts using a variety of techniques to maximize traffic flow to user accounts. I formally distributed this software as the 'RKAB Comment Bot' to over 100 unique users, providing live customer support and incremental feature improvement based on user feedback. The tech stack leverages Python for general webscraping abiltiies, while using the tkinter library to power the UI/UX. MySQL is used under the hood to store HWID-based customer license keys which are used to authorize access to the software. The database used to be hosted on-premises, but is no longer active.

This software was developed for Windows, but can be run on Mac by generating an exe file using Wine.

While not captured in this repository, I developed various tools to support the business, including accounting and license management dashboards.

# USAGE:

To run this software, clone this repository and run interface.py. Don't run installer.py as it's unneccessary and was originally used to authenticate customer license keys.

# Files:

**installer.py**
Handles bot installation and license authentication by verifying users against the license database.

**database_functions.py**
Utility functions for connecting to and interacting with the user database.

**interface.py**
User-facing interface that manages bot configuration, account details, and behavioral controls.

**shared.py:**
Shared state and constants used to coordinate data between the GUI and bot logic.

**source.py:**
Core bot implementation, including Instagram navigation, commenting logic, and the primary bot class.

**accounts.txt:**
List of Instagram accounts provided by the user for automated commenting.

**commented_posts.txt:**
Records posts that have already been processed and commented on to prevent duplicates.

**comments.txt:**
Pool of comments randomly selected by the bot when posting.

**config.txt:**
Configuration file defining user-customizable bot settings and behavior.

**hashtags.txt:**
Hashtags used by the bot when operating in hashtag mode.

**sources.txt:**
Stored source links or identifiers collected when commenting outside of feed mode.

**target_accounts.txt:**
Target Instagram accounts whose posts are commented on in account mode.

# Dependency Notes:

This software requires the latest version of [Chromedriver](https://chromedriver.chromium.org/downloads) to be installed in the bot's root directory for the bot to successfully run. Google Chrome must also be installed on the user's machine, and the version of Chrome should match the version of Chromedriver in the bot directory. Alternative drivers (e.g geckodriver) can also be used if preferred.
