def brand_table(connection):
    # check table
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'brand'")
    result = cursor.fetchone()
    
    if result:
        # if have table is alert already
        print("Table 'brand' already exists.")
    else:
        # data for table
        query = """
            CREATE TABLE brand (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                status ENUM('active', 'inactive') DEFAULT 'active',
                create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                modify_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        """
        cursor.execute(query)
        connection.commit()
        # if don't have table is alert created
        print("Table 'brand' created successfully.")
    
    cursor.close()
