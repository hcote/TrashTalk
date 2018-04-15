    # Developer's Guide to Contributing

#### -------------- **PYTHON 3 REQUIRED** --------------
**Contents:**
- [Team Contact](#teamcontact)
- [Code Guidelines](#codeguidelines)
- [Submitting Pull Requests](#pullrequests)
- [Setting up locally](#settings)
- [Integrations](#integrations)
- [Deployment](#deployment)

This guide attempts to make no assumptions about the skill level of the developer. Your
contributions are welcome no matter your skill level. If you have questions, you can post
them on the issue tracker (use the appropriate labels so you can get the attention you
need!).
<a name="teamcontact"></a>
## Team Contact
- [Slack](https://openoakland.slack.com)
- [Project Board](https://github.com/openoakland/TrashTalk/projects)
- [Issue Tracker](https://github.com/TangoYankee/TrashTalk/issues)

As an open source, collaborative, public project developers come and go with the seasons. The goal of this guide is to make it possible for each participant to make contributions with as little pain as possible.

That said, communication is still the key to the optimal experience! Asking questions and working with others will be very helpful during development.

<a name="codeguidelines"></a>
## Code Guidelines

- Upload code changes to a branch within a personal repository and then submit a pull request to the Master repository.
   - **Never push directly to the Master repository**
- Allow another contributer to review and commit the changes to the master repository. 
   - **Never commit your own code to the Master repository**
- [Test](https://docs.djangoproject.com/en/2.0/topics/testing/) code changes programmtically
- [Lint](https://pylint.readthedocs.io/en/latest/index.html) files to make sure they follow PEP8. Aim for a pylint score of at least 7 per file edited file (C level messages are acceptable usually).
- Securely store password and keys.
    - **Never place sensitive information in a repository**
- Update the [requirements files](https://github.com/openoakland/TrashTalk/tree/master/requirements) with any newly added modules

<a name="pullrequests"></a>
#### Submitting Pull Requests
When submitting pull requests, try to follow these conventions:

__Commit message format__
*ISSUE NUMBER ISSUE TYPE -- Description of the work done*</br>
    -If there's no issue for the changes you want to make, create one and describe the changes you want to submit. Give as much detail as you're able!

__Pull Request Format__
- Title: Same as commit message above.
- Description: Add some details about the code changes. 
 Include links or references to any information that will be helpful to other developers who have to review your code!
- Checklist: Make sure you've hit all the marks! 
- Code Failures: The code will be automatically tested by Travis once you create the PR. If you see any test failures, re-review your code and fix the errors. If you're not sure what's wrong, leave a comment on your PR for other devs to help you out.
- Linting: Read about [Lint Messaging](https://pylint.readthedocs.io/en/latest/user_guide/output.html#source-code-analysis-section) in order to improve the readability of the code

**More Documentation**
- [Django Docs](https://docs.djangoproject.com/en/dev/)
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [Google Apps](https://cloud.google.com/docs/)
- [Pylint](https://pylint.readthedocs.io/en/latest/user_guide/)

<a name="settings"></a>
## Setting Up Local
Follow the links at each step for appropriate instructions
## Overview
1. Create local copy of project: [New Developer Guide](https://github.com/openoakland/TrashTalk/wiki/New-Developer-Guide)
2. [Install python requirements to a virtual environment named `venv`.](#requirements) This is important to control versions of dependencies
3. Install [postgreSQL](https://www.postgresql.org/)
4. Update and configure local settings
5. Seed Test Data
6. Create code changes locally: [New Developer Guide](https://github.com/openoakland/TrashTalk/wiki/New-Developer-Guide) 
7. Lint and update accordingly: `venv/bin/pylint --rcfile=./.pylintrc ./`
8. Test: `python manage.py test`
9. Share Code Changes: [New Developer Guide](https://github.com/openoakland/TrashTalk/wiki/New-Developer-Guide)

<a name="requirements"></a>
#### Step 2: Requirements and Virtual Environment
create a virtual environment and install project requirements:
```bash
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements/dev.txt
```

#### Step : Update and Configure Local Settings

Always work on a new branch when developing new changes to the code. Never work on the
master branch.

```
# Update to the latest the code
git pull upstream master

# Make your own copy of dev.py.example and rename to dev.py
cp trashtalk/settings/dev.py.example trashtalk/settings/dev.py

# Open dev.py and update it with your database settings
# Next, create and migrate the database:
createdb trashtalk
python manage.py migrate

# Create an admin user for the Trashtalk app and follow the prompts
python manage.py createsuperuser

# Run the server and open in your browser at localhost:8000
python manage.py runserver

*NOTE: `dev.py` is yours and is best used for storing your credentials and custom log settings. Beware that these settings are NOT shared by anyone else so keep it simple.*

```
# Verify all the files that have changed
git status

# If you're satisfied, stage all your file changes and additions
git add .

git commit -m "#99 Type a good message here about the changes."
git push origin YOUR_BRANCH_NAME
```


<a name="modeling"></a>
## Making Model Changes

Django manages the database for us. Be extremely thoughtful about making changes to models.
If you change models, make sure you create the migrations and commit them to git.

```
# First edit the models you wish to change/add/remove
# Create the migation files:
python manage.py makemigrations

# Apply the migrations:
python manage.py migrate
```

Please refer to the official Django Documentation and learn more:
- [Model Documentation](https://docs.djangoproject.com/en/dev/topics/db/)
- [Migrtions Documentation](https://docs.djangoproject.com/en/dev/topics/migrations/)

