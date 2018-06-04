"""empty message

Revision ID: e57c8a3123fc
Revises: bea917440418
Create Date: 2018-05-22 12:32:28.415302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e57c8a3123fc'
down_revision = 'bea917440418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.DateTime(), nullable=True),
    sa.Column('user_email', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('author', sa.String(length=60), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('availability', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('book_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_revoked', sa.DateTime(), nullable=True),
    sa.Column('jti', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('user_password', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('borrowed_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('book_title', sa.String(length=60), nullable=False),
    sa.Column('book_author', sa.String(length=60), nullable=False),
    sa.Column('book_description', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_borrowed', sa.Date(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('returned', sa.Boolean(), nullable=True),
    sa.Column('returned_date', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrowed_books')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('revoked_tokens')
    op.drop_table('books')
    op.drop_table('active_tokens')
    # ### end Alembic commands ###
