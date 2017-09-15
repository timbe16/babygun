"""empty message

Revision ID: 339a32884dc6
Revises: 
Create Date: 2017-09-12 22:51:43.002708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '339a32884dc6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'email',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('mail_from', sa.String(255), nullable=False),
        sa.Column('mail_to', sa.String(255), nullable=False),
        sa.Column('mail_cc', sa.String(255), nullable=True),
        sa.Column('mail_bcc', sa.String(255), nullable=True),
        sa.Column('mail_subj', sa.String(255), nullable=True),
        sa.Column('body', sa.Text, nullable=True),
        sa.Column('last_sent_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('status', sa.Boolean),
        sa.Column('counter', sa.Integer(), nullable=False),
    )
    op.create_table(
        'email_status',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email_id', sa.Integer(), nullable=False),
        sa.Column('sent_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('status', sa.Text, nullable=True),
        sa.Column('delivered', sa.Boolean)
    )


def downgrade():
    pass
