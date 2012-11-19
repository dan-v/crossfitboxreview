from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('affiliate_id', Integer),
    Column('ipaddress', String(length=20), nullable=False),
    Column('rating_overall', Integer, nullable=False),
    Column('rating_equipment', Integer, nullable=False, default=ColumnDefault(1)),
    Column('rating_instructor', Integer, nullable=False, default=ColumnDefault(1)),
    Column('comment', Text, nullable=False),
    Column('review_date', DateTime, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['review'].columns['rating_equipment'].create()
    post_meta.tables['review'].columns['rating_instructor'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['review'].columns['rating_equipment'].drop()
    post_meta.tables['review'].columns['rating_instructor'].drop()
