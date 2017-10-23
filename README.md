Trashtalk
=========

Trashtalk.com will essentially act as a liaison between: Oakland's Department of Public Works and the Oakland Adopt-A Volunteer Program...fueled by community leaders starting cleanups within their community (or defined areas/location of interest)

## Developers
Please read CONTRIBUTE.md for full information and instructions.

Before you can do anything, you must do the following:

To run:
- Fork the repository.
- Clone your fork of the repo.
- Run: `pip install -r requirements.txt`
- Run: `alembic upgrade head`

Then you can configure the project. Open `dev.cfg` to customize the
settings to your local configuration. An example is provided in `dev.cfg.example` of what you may need to change. **Remember to uncomment the config line in the main app script (run.py) if you do this.**

Finally: `python run.py`

For debug mode, set the `FLASK_APP` environment variable and use `flask run` instead.

To locally test the app on Google Cloud, please check the wiki for full instructions:
https://github.com/openoakland/TrashTalk/wiki/Deployment

### Updating Your App

You'll also need to update `alembic.ini` with the URI to your database in
order to run migrations:
`sqlalchemy.url = postgresql://postgres@localhost/trashtalk`

