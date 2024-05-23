"""2024.1.0b1 Revision merge

Revision ID: d4d4be3b65a6
Revises: ('e032a4187413', 'f57584a7076f')
Create Date: 2024-05-09 12:41:34.979640

"""

# revision identifiers, used by Alembic.
revision = "d4d4be3b65a6"
down_revision = ("e032a4187413", "f57584a7076f")

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass


def migrate_datas():
    from alembic.context import get_bind
    from zope.sqlalchemy import mark_changed
    from caerp_base.models.base import DBSESSION

    session = DBSESSION()
    conn = get_bind()

    mark_changed(session)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
