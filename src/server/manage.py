from flask.cli import FlaskGroup

from core.extensions import db
from core import masakhane, load_model

from flask import current_app
from core.models.language import Language

import click, json, os


cli = FlaskGroup(masakhane)


@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()
        

@cli.command("init_models")
def init_models():
    print(current_app.models)
    print(masakhane.models)

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
    with open(os.environ.get('JSON', 
    "./languages.json"), 'r') as f:
            distros_dict = json.load(f)

    languages_short_to_full = {}
    languages_full_to_short = {}

    for distro in distros_dict:
        languages_short_to_full[distro['language_short'].lower()] = distro['language_en'].lower()
        languages_full_to_short[distro['language_en'].lower()] = distro['language_short'].lower()

    source, target, domain = name_tag.split('-')
    language = Language(src_tgt_dmn=name_tag, 
                        source_target_domain = f"{languages_short_to_full[source]}-{languages_short_to_full[target]}-{domain}")
    db.session.add(language)
    db.session.commit()
    

@cli.command("remove_language")
@click.argument('name_tag')
def remove_language(name_tag):
    source, target, domain = name_tag.split('-')
    # Be carefull 
    language = Language.query.filter_by(src_tgt_dmn=name_tag).first_or_404()

    print(language)
    db.session.delete(language)
    db.session.commit()


if __name__ == "__main__":
    cli()