"""fix_users_role_authority_check_case_insensitivity

Revision ID: 1925b630e83a
Revises: 66f98182a0b2
Create Date: 2026-09-15 02:06:20.571444+00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1925b630e83a'
down_revision: Union[str, None] = '66f98182a0b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('users_role_authority_check', 'users', type_='check')
    op.create_check_constraint(
        'users_role_authority_check',
        'users',
        '''
        (UPPER(role::text) IN ('CITIZEN', 'ADMIN') AND authority_id IS NULL)
        OR (UPPER(role::text) IN ('AUTHORITY', 'FIELD_WORKER') AND authority_id IS NOT NULL)
        '''
    )


def downgrade() -> None:
    op.drop_constraint('users_role_authority_check', 'users', type_='check')
    op.create_check_constraint(
        'users_role_authority_check',
        'users',
        '''
        (role IN ('CITIZEN', 'ADMIN') AND authority_id IS NULL)
        OR (role = 'AUTHORITY' AND authority_id IS NOT NULL)
        '''
    )

