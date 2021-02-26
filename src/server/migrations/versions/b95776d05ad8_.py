"""empty message

Revision ID: b95776d05ad8
Revises: 9691767e83b7
Create Date: 2021-02-08 23:57:40.451373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b95776d05ad8'
down_revision = '9691767e83b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('masakhane_src_lang_key', 'masakhane', type_='unique')
    op.drop_constraint('masakhane_token_key', 'masakhane', type_='unique')
    op.create_unique_constraint(None, 'masakhane', ['stars'])
    op.create_unique_constraint(None, 'masakhane', ['review'])
    op.create_unique_constraint(None, 'masakhane', ['input'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'masakhane', type_='unique')
    op.drop_constraint(None, 'masakhane', type_='unique')
    op.drop_constraint(None, 'masakhane', type_='unique')
    op.create_unique_constraint('masakhane_token_key', 'masakhane', ['token'])
    op.create_unique_constraint('masakhane_src_lang_key', 'masakhane', ['src_lang'])
    # ### end Alembic commands ###