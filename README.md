# IG_CommentBot
-----DESCRIPTION:

Instagram Comment bot formerly sold as the 'RKAB Comment bot'. This bot is a web-scraping based comment bot that utilizes parallel programming with several key modes that allow users to automate commenting on the social media platform.

This bot uses Python, and is connected to a MySQL database that holds client information, including their license keys which are used to run the bot. The databse tracks the bot's host computer's unique ID in order to identify if the machine can be given permission to run the software. If the databse ID does not match the computer's, then the software will not fully load the interface, thus preventing the bot from being properly run (assuming the bot is being run through as an exe). If an invalid license key is used, or a license key is not provided, the bot will not run. For security reasons, aspects of the licensing system have been omitted from this repository in order to keep sensitive data hidden. 
NOTE: License checking has been disabled (commented out) so the bot can actually be run without the user being locked out for having an invalid license.

The comment bot itself uses selenium as its way of accessing and parsing the html of the Instagram website. The general tags used for the bot should have a low chance of becoming obsolete, unless some sort of Instagram html update drastically changes the site layout. The tags used to navigate the site have been in use for a little over a year since I have added this project to Github. The frontend of the bot uses the tkinter library, which has the perfect level of functionality and speed for the comment bot program. The layout is simple, with status text that updates/changes in real-time in response to button clicks. The front-end also has functional scroll bars, and auxiliary windows that open panels to view accounts, bot status, and much more. 



-----FILES:

installer.py - Installer used to authenticate bot copies by connecting to and verifying licenses in the user database

database_functions.py - Contains some functions used to connect to the user database

interface.py - Interface displayed to the user. Contains functionalities that support customization of bot behavior, account information, and many other functionalities.

shared.py - small collection of variables and data to faciliate communication of data shared between the GUI and bot

source.py - Source code containing the functions used to navigate and comment on the instagram website, as well as a bot class containing the majority of the bot functionalities.

accounts.txt - Accounts the user has inputted for the bot to use for commenting purposes

commented_posts.txt - Posts the bot has located in the feed, and already commented on.

comments.txt - Contains a collection of comments the bot will pull from at random when commenting on a post.

config.txt - Settings allowing for the user to customize bot behavior.

hashtags.txt - collection of hashtags the bot will use in conjunction with 'hashtag' mode

sources.txt - Collection of unique source tags/links the bot has saved after commenting on posts using modes that are not 'feed' mode

target_accounts.txt - Accounts whos posts the bot will comment on when using 'account' mode

-----DEPENDENCIES:

Several python libraries are used, which can be found at the top of each python file. Software-wise, the bot requires the appropriate
version of [Chromedriver](https://chromedriver.chromium.org/downloads) in the bot's root directory in order to run the bot. The appropriate version of Chrome driver can be found by downloading and using the version of Chromedriver that matches the user's downloaded version of Google Chrome (This can be checked by opening chrome, and navigating to Help->About Google Chrome). Alternatively, another webdriver can theoretically be used if the user has the alternative webdriver in the bot directory, and matching internet browser installed. Alternatives to Google chrome have not been tested.

In order to be run on Mac, an exe can be made on a Mac operating system, or virtual machine running MACOS. Note that python must still be installed on the machine. When creating exe files for distribution, pyinstaller is my preffered method of creating an exe for the program. All dependencies are converted, and all files can be included in a single command. Command prompt can also be hidden from the user.
