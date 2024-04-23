from flask.cli import FlaskGroup
from app import app, db, migrate
from flask_migrate import upgrade, init

cli = FlaskGroup(app)

@cli.command('db_create')
def db_create():
    db.create_all()

@cli.command('db_migrate')
def db_migrate():
    migrate.init_app(app,db)

@cli.command('db_upgrade')
def db_upgrade():
    migrate.init_app(app,db)
    upgrade()

@cli.command('db_init')
def db_init():
    init()

if __name__ == '__main__':
    cli()