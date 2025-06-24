# Run  python migrate.py

from database.database import connection
# from migration.status import status_table
from migration.gender import gender_table
from migration.roles import roles_table
from migration.permission import permission_table
from migration.roles_permission import roles_permission_table
from migration.users import users_table
from migration.brand import brand_table

if connection:
    # status_table(connection)
    gender_table(connection)
    roles_table(connection)
    permission_table(connection)
    roles_permission_table(connection)
    users_table(connection)
    brand_table(connection)



