#external imports

import click, json, os, unittest
from flask.cli import FlaskGroup
# internal imports
from core.extensions import db
from core import masakhane
from core.models.language import Language


cli = FlaskGroup(masakhane)


@cli.command("create_db")
def create_db():
    """User defined Flask CLI command
    ---
    This command will create and commit the available database tables"""
    db.create_all()
    db.session.commit()


@cli.command("clean")
def clean():
    """User defined Flask CLI command
    ---
    This command will DELETE & re-create the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("all_languages")
def all_languages():
    """User defined Flask CLI command
    ---
    This command will list the translation model info in the database"""
    for lan in Language.query.all():
        print(lan.to_json())


@cli.command("add_language")
@click.argument('name_tag')
def add_language(name_tag):
    """User defined Flask CLI command
    ---
    This command will add a language into the database\n
    The parameter is of the form `src-trg-domain`, ie. `en-sw-JW300` || `en-tiv-`
    """
    with open(os.environ.get('JSON',
                             "./languages.json"), 'r') as f:
        distros_dict = json.load(f)

    languages_short_to_full = {}
    languages_full_to_short = {}

    for distro in distros_dict:
        languages_short_to_full[distro['language_short'].lower(
        )] = distro['language_en'].lower()
        languages_full_to_short[distro['language_en'].lower(
        )] = distro['language_short'].lower()

    source, target, domain = name_tag.split('-')
    language = Language(src_tgt_dmn=name_tag,
                        source_target_domain=f"{languages_short_to_full[source]}-{languages_short_to_full[target]}-{domain}")

    db.session.merge(language)
    db.session.commit()


@cli.command("remove_language")
@click.argument('name_tag')
def remove_language(name_tag):
    """User defined Flask CLI command
    ---
    This command will remove a language from the database\n
    The parameter is of the form `src-trg-domain`, ie. `en-sw-JW300` || `en-tiv-`
    """
    try:
        language = Language.query.filter_by(
            src_tgt_dmn=name_tag).first_or_404()

        print(language)
        db.session.delete(language)
        db.session.commit()
    except Exception as e:
        pass


@cli.command("tests")
def tests():
    """User defined Flask CLI command
    --- 
    Runs the tests without code coverage """

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    for test_module in loader.discover('core/tests', pattern='test*.py'):
        suite.addTest(test_module)

    result = unittest.TextTestRunner(verbosity=1).run(suite)

    if result.wasSuccessful():
        return 0
    return 1
    # return tests


if __name__ == "__main__":
    cli()
