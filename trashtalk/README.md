Trashtalk
=========

Trashtalk.com will essentially act as a liaison between: Oakland's Department of Public Works and the Oakland Adopt-A Volunteer Program...fueled by community leaders starting cleanups within their community (or defined areas/location of interest)

## Developers

To run:
- Fork the repository.
- Clone your fork of the repo.
- Run: `pip install -r requirements.txt`

Then you can configure the project. Open `dev.cfg` to customize the
settings to your local configuration. An example is provided in `dev.cfg.example` of what you may need to change.

Finally: `python run.py`

For debug mode, set the `FLASK_APP` environment variable and use `flask run` instead.

### Updating Your App

You'll also need to update `alembic.ini` with the URI to your database in
order to run migrations:
`sqlalchemy.url = postgresql://postgres@localhost/trashtalk`