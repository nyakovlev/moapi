![Spontaneously Talos Education Presents:](https://nyakovlev.github.io/images/loadIcon.png "Encroaching upon a perfectly healthy and independent realm of learning since 2015")
<br>
Welcome, CV CyberPatriot teams! This repository is aimed at establishing a home for Ubuntu/Debian scripting.

Scripting is an extremely powerful method for accomplishing the various security tasks of a typical CyberPatriot round. Over the years, a number of students have developed nifty tools to help you knock out vulnerabilities, but documentation for such tools is often quite scarce, and as a result, many individuals shy away from the power of code. This repository is focused towards closing the coding gap between separate CyberPatriot seasons; however, this is a process, and it has yet to be completed. You must be daring and ready to complete tasks and follow instructions on your own. You must be prepared to copy and paste cryptic error messages into Google and experiment with doubtful but hopeful solutions. You must be willing to take independent initiative and decide how YOU want to own this season.

You can also ask Pauley for help - while an independent drive is vital, we're still here for guidance.

While scripting is a challenging skill to learn, anybody can excel in it with some perseverance, and it is well worth your time and effort.

# Installation Instructions
* Step 0: Make sure you have Ubuntu running somewhere.
* Step 1: Open a terminal and type `git clone https://github.com/nyakovlev/moapi.git`. If it says that the git command isn't recognized, you'll need to install it with `sudo apt-get install git`.
* Step 2: Enter the KeepMe directory: `cd moapi/KeepMe`.
* Step 3: Type `chmod 755 install.sh`, then type `sudo ./install.sh`. This ensures that various dependencies, like Python3.6, websockets, pygame, and Google Chrome are runing on the system.
* Step 4: You're ready to go! To verify functionality of the installation, type `sudo ./scoring_engine.py` or double-click the newly-created **Scoring Engine** icon on your desktop.

# Contribute
If you have been tasked with adding a vulnerability into this scoring engine, then this is the section for you!
To start out:
* Step 1: Create your own version (or branch) of the project and switch your local directory to that branch:
`git checkout -b <BRANCH_NAME>`
You may set BRANCH_NAME to whatever you wish.
* Step 2: Edit the necessary files for your vulnerability. Details on this process are described in the below section, titled **Editing a Vulnerability**.
* Step 3: Regularly save your progress to github:<br>
`git commit -m "CHANGE MESSAGE"`<br>
`git push origin <BRANCH_NAME>`
* Step 4: When you have finished crafting your vulnerability, and everything seems to work as intended, go ahead and create a pull request to the master branch:
  * Go to the Pull Requests tab at the top of the GitHub page and select "New Pull Request".
  * Select the branch that contains your newly-created work.
  * Go through the steps on the page, adding a name and description to the request as you see fit and eventually completing the process.

# Editing a Vulnerability
Data for each vulnerability in the Scoring engine is stored in **scoring/data**.
It is helpful to have a browser with the Scoring Engine open as you look through the data. Each folder corresponds to a section in the web interface. For example, "Basic Hardening Tasks" corresponds to the **basic_cfg** folder.
Work your way down the directory tree until you get to the folder of your vulnerability. Inside this folder, you'll find 3 critical files:
* **info**: Provides some general data about your vulnerability (including the location of the tutorial page)
* **script###.py**: Has the actual functionality of your vulnerability; you'll spend just about all of your time here.
* **tutorial.html**: A file that you can use for a tutorial page
The script.py file contains three Python functions:
* **check()**: This function runs every few seconds in the scoring engine. It must return **True** or **False** (True means that the vulnerability has been fixed).
* **fix()**: This function runs when the fix button for your function is clicked on the page.
* **reset()**: This function runs when the reset button for your function is clicked on the page.
Edit the file to give the vulnerability functionality. After saving the file, you'll need to restart the Scoring Engine to test your work.
Good luck! Contact Pauley if you run into any snags in this process.

Best wishes!

Nikita Ioukovlev<br>
*Former/lifelong member of **Talos**, its successor, **Spontaneously Talos**, and its team-agnostic philanthropy branch, **Spontaneously Talos Education***
