from flask.cli import FlaskGroup

from core.extensions import db
from core import masakhane, load_model

from flask import current_app
from core.models.language import Language, language_list

import click


cli = FlaskGroup(masakhane)


@cli.command("create_db")
def create_db():
    # db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("clean")
def clean():
    # Carefull this will delete the content of the databases
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("all_language")
def all_language():
    for lan in Language.query.all():
        print(lan.to_json() )

@cli.command("add_language")
@click.argument('name_tag')
def add_language(name_tag):
    language = Language(src_tgt=name_tag)
    db.session.add(language)
    db.session.commit()
    source, target = name_tag.split('-')

@cli.command("remove_language")
@click.argument('name_tag')
def remove_language(name_tag):
    # Be carefull 
    language = Language.query.filter_by(src_tgt=name_tag).first_or_404()
    print(language)
    db.session.delete(language)
    db.session.commit()


if __name__ == "__main__":
    cli()