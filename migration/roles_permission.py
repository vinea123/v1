def roles_permission_table(connection):
    # check table
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'roles_permission'")
    result = cursor.fetchone()
    
    if result:
        # if have table is alert already
        print("Table 'roles_permission' already exists.")
    else:
        # data for table
        query = """
            CREATE TABLE roles_permission (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roles_id INT,
                permission_id INT,
                create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                modify_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (roles_id) REFERENCES roles(id) ON DELETE CASCADE,
                FOREIGN KEY (permission_id) REFERENCES permission(id) ON DELETE CASCADE
            );
        """
        cursor.execute(query)
        connection.commit()
        # if don't have table is alert created
        print("Table 'roles_permission' created successfully.")
    
    cursor.close()
