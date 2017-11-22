# Developer's Guide to Contributing

#### -------------- **PYTHON 3 REQUIRED** --------------

This guide attempts to make no assumptions about the skill level of the developer. Your
contributions are welcome no matter your skill level. If you have questions, you can post
them on the issue tracker (use the appropriate labels so you can get the attention you
need!).

**Communication:**
- [Slack](https://openoakland.slack.com)
- [Project Board](https://github.com/openoakland/TrashTalk/projects)
- [Issue Tracker](https://github.com/TangoYankee/TrashTalk/issues)

**Development:**
- [Setting up locally](#setting)
- [Code Guidelines](#codeguidelines)
- [Integrations](#integrations)
- [Deployment](#deployment)

## Code Guidelines

- Do not merge your own code. It should be reviewed by your fellow devs and merged by them.
- Test your changes, always, before submitting them.
- Lint your files before submitting them to make sure they follow PEP8
- Never store API keys or passwords in your code! Sensitive data should be stored securely, never in the repository.
- Be sure to add any new modules you install to the requirements file.

**Other Documentation**
- [Django Docs](https://docs.djangoproject.com/en/dev/)
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [Google Apps](https://cloud.google.com/docs/)

## Setting Up Local

The steps laid out will be further detailed below, step by step.

1. Fork the main repository
2. Pull the code onto your local machine
3. Set-up your git remotes
4. Install the requirements to a folder named `venv`. This is important.
5. Create a new branch
6. Commit your changes to the code.
7. Lint and update accordingly: `venv/bin/pylint --rcfile=./pylint.cfg ./`
8. Test: `python manage.py test`
9. Push the branch to your fork
0. Create a Pull Request

Let's get started!

#### Step 1: Install

At the top right of the main repository github page, click the Fork button and save it wherever you like. It should default to your personal account.

Then open your terminal (command line):

```
git clone https://github.com/YOUR_ACCOUNT_HERE/TrashTalk
cd TrashTalk
git remote add upstream https://github.com/openoakland/TrashTalk
```

Now you have forked your own copy of the repo, downloaded the files and set-up your remotes.

Next, install project requirements to a virtual environment:
```bash
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements/dev.txt
```

You're ready to start coding.

#### Step 2: Develop

Always work on a new branch when developing new changes to the code. Never work on the
master branch.

```
# Update to the latest the code
git pull upstream master

# Open settings/dev.py and configure your local database settings.
# Create and update your database:
createdb trashtalk
python manage.py migrate

# Create a super user for using the app during development
python manage.py createsuperuser

# Create a new branch to work on and then start the app
git checkout -b YOUR_BRANCH_NAME
python manage.py runserver
```

Update your configuration settings in the following files:
* settings/dev.py: Verify database URI and user settings

Your app should now be running locally. Open your browser to http://localhost:8000 to view it.

You can begin making your changes to the code at this point. Remember to test your changes when you're done to make sure they work.

#### Step 3: Commit and Push

You're done making changes. Now it's time to share your updates.

```
# Verify all the files that have changed
git status

# If you're satisfied, stage all your file changes and additions
git add .

git commit -m "Type a good message here about the changes."
git push origin YOUR_BRANCH_NAME
```

Now go to your fork on Github. You may see a notification about the recent push you just made. Click the "New Pull Request" button next to it.

If you don't see a notification, select YOUR_BRANCH_NAME from the branch drop down menu on the top left of the repository. Then click the "New pull request" button next to it.

Leave a descriptive title and message on your PR. Include links or references to any information that will be helpful to other developers who have to review your code!

The code will be automatically tested by Travis once you create the PR. If you see any test failures, re-review your code and fix the errors. If you're not sure what's wrong, leave a comment on your PR for other devs to help you out.

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

