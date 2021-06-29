import mysql.connector

database = mysql.connector.connect(host="redacted",
                                   user="redacted",
                                   passwd="redacted",
                                   database="redacted")

data_cursor = database.cursor()

#You need to set the increments when using mysql.connector.
#If you don't do this, the increment values are corrupted for unknown reasons.
data_cursor.execute("ALTER TABLE client AUTO_INCREMENT=1")
data_cursor.execute("SET @@auto_increment_increment=1")



database.commit()
data_cursor.close()
database.close()
