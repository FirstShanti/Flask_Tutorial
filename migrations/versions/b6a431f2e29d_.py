"""empty message

Revision ID: b6a431f2e29d
Revises: 5f1207aaa403
Create Date: 2020-01-07 22:54:52.135205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6a431f2e29d'
down_revision = '5f1207aaa403'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('knot_posts',
    sa.Column('knot_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['knot_id'], ['knot.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], )
    )
    op.add_column('knot', sa.Column('slug', sa.String(length=140), nullable=True))
    op.create_unique_constraint(None, 'knot', ['slug'])
    op.create_unique_constraint(None, 'tag', ['name'])
    op.create_unique_constraint(None, 'tag', ['slug'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='unique')
    op.drop_constraint(None, 'tag', type_='unique')
    op.drop_constraint(None, 'knot', type_='unique')
    op.drop_column('knot', 'slug')
    op.drop_table('knot_posts')
    # ### end Alembic commands ###