'''empty message

Revision ID: 7f7d4d6f29e1
Revises: 
Create Date: 2022-07-13 06:37:35.556125

'''
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f7d4d6f29e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('savings_goal', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=True),
    sa.Column('savings_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('month',
    sa.Column('month_id', sa.Integer(), nullable=False),
    sa.Column('month', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('month_id')
    )
    op.create_table('expense',
    sa.Column('expense_id', sa.Integer(), nullable=False),
    sa.Column('expense_type', sa.Text(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('month_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['month_id'], ['month.month_id'], ),
    sa.PrimaryKeyConstraint('expense_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    op.drop_table('month')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###