    # Developer's Guide to Contributing

#### -------------- **PYTHON 3 REQUIRED** --------------
**Contents:**
- [Team Contact](#teamcontact)
- [Code Guidelines](#codeguidelines)
- [Submitting Pull Requests](#pullrequests)
- [Setting up locally](#settings)

This guide attempts to make no assumptions about the skill level of the developer. Contributions are welcome, regardless of skill level! Post any questions on the issue tracker (use appropriate labels to get the right help).

<a name="teamcontact"></a>
## Team Contact
- [Slack](https://openoakland.slack.com)
- [Project Board](https://github.com/openoakland/TrashTalk/projects)
- [Issue Tracker](https://github.com/openoakland/TrashTalk/issues)

As an open source, collaborative, and public project, developers come and go in seasons. This guide to makes it possible for each participant to effectively contribute. Communication is the key to an optimal experience! Ask questions and work with others to create a fluid development process.

<a name="codeguidelines"></a>
## Code Guidelines

- Upload code changes to a branch within a personal repository and then submit a pull request to the Master repository.
   - **Never push directly to the Master repository**
- Allow another contributer to review and commit the changes to the master repository. 
   - **Never commit your own code to the Master repository**
- [Test](https://docs.djangoproject.com/en/2.0/topics/testing/) code changes programmtically before committing them
- [Lint](https://pylint.readthedocs.io/en/latest/index.html) files to make sure they follow PEP8. Aim for a pylint score of at least 7 in each edited file (C level messages are acceptable usually).
- Securely store password and keys.
    - **Never place sensitive information in a repository**
- Update the [requirements files](https://github.com/openoakland/TrashTalk/tree/master/requirements) with any newly added modules

<a name="pullrequests"></a>
#### Submitting Pull Requests (PRs)
When submitting pull requests, please follow these conventions:

__Commit message format__
*ISSUE NUMBER ISSUE TYPE -- Description of the work done*</br>
    -If there's no issue associated with the code changes, create one and describe the desired changes. Give as much detail as possible!

__Pull Request Format__
- Title: Same as commit message above.
- Description: Add some details about the code changes. 
 Include links or references that will help other developers review the code!
- Checklist: Make sure to hit all the marks! 
- Code Failures: [Travis](https://docs.travis-ci.com/user/getting-started/) will automatically test the PR. If there are any test failures, review the code and fix the errors. If it's unclear what's wrong, leave a comment on the PR and other developers will help.
- Linting: Read about [Lint Messaging](https://pylint.readthedocs.io/en/latest/user_guide/output.html#source-code-analysis-section) and improve the readability of the code

**More Documentation**
- [Django Docs](https://docs.djangoproject.com/en/dev/)
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [Google Apps](https://cloud.google.com/docs/)
- [Pylint](https://pylint.readthedocs.io/en/latest/user_guide/)
- [PostgreSQL](https://www.postgresql.org/docs/)

<a name="settings"></a>
## Setting Up Local
Follow the links at each step for appropriate instructions
## Overview
1. Create local copy of project: [New Developer Guide](https://github.com/openoakland/TrashTalk/wiki/New-Developer-Guide)
2. [Install python requirements](#requirements) to a virtual environment named `venv`. This is important for dependency version control
3. [Install postgreSQL](https://www.postgresql.org/)
4. [Configure local settings](#localsettings) 
6. Create code changes locally: [New Developer Guide](https://github.com/openoakland/TrashTalk/wiki/New-Developer-Guide) 
7. [Manage model](#modeling) changes
8. [Locally Review](#localreview) code changes
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

<a name="localsettings"></a>
#### Step 4: Configure Local Settings

Always develop on a new branch. Never work on the master branch.

Make your own copy of dev.py.example and rename to dev.py
```
cp trashtalk/settings/dev.py.example trashtalk/settings/dev.py
```
Open dev.py and update it with:
   </br>a. postgresql username and password
   </br>b. [API Key](https://developers.google.com/maps/documentation/embed/guide) to view Google Maps
        - Each new IP address will need to gain permission to use the API Key
   
Create and migrate the database:
```
createdb trashtalk
python manage.py migrate
```
Create an admin user for the Trashtalk app and follow the prompts
```
python manage.py createsuperuser
```
Seed test data
```
python manage.py seed config/locations.csv
```
Run the server and open in your browser at localhost:8000
```
python manage.py runserver
```
*NOTE: `dev.py` is private and is best used for storing custom credentials and settings. Beware: these settings are NOT shared by anyone; Keep it Simple.*

Verify all the files that have changed
```
git status
```

<a name="modeling"></a>
## Step 6: Make Model Changes

Django includes database management. Be extremely thoughtful when making changes to models. Ensure to migrate any model changes and commit them to git.

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


<a name="localreview"></a>
## Step 7: Local Code Review
a. [Lint](https://pylint.readthedocs.io/en/latest/user_guide/run.html) and update accordingly: 
    ```venv/bin/pylint --rcfile=./.pylintrc ./```
    or
    ```pylint [filename].py```
    
b. [Test](https://docs.djangoproject.com/en/2.0/topics/testing/): 
    `python manage.py test`
