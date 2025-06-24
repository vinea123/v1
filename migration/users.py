def users_table(connection):
    # check table
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'users'")
    result = cursor.fetchone()
    
    if result:
        # if have table is alert already
        print("Table 'users' already exists.")
    else:
        # data for table
        query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                dob DATE,
                address TEXT,
                gender_id INT,
                roles_id INT,
                create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                modify_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (gender_id) REFERENCES gender(id) ON DELETE SET NULL,
                FOREIGN KEY (roles_id) REFERENCES roles(id) ON DELETE SET NULL
            );
        """
        cursor.execute(query)
        connection.commit()
        # if don't have table is alert created
        print("Table 'users' created successfully.")
    
    cursor.close()

    
