from flask.cli import FlaskGroup
from app import app, db, migrate

cli = FlaskGroup(app)

@cli.command('db_create')
def db_create():
    db.create_all()

@cli.command('db_migrate')
def db_migrate():
    migrate.init_app(app,db)
    migrate.migrate()

@cli.command('db_upgrade')
def db_upgrade():
    migrate.init_app(app,db)
    migrate.upgrade()

if __name__ == '__main__':
    cli()