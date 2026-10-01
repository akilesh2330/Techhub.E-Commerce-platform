# config.py
# Stores configuration settings for our Flask app, including database credentials.
# Keeping this separate from route files means we only update credentials in ONE place.

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Techhub@123'  # Replace with YOUR actual MySQL password
    MYSQL_DB = 'techhub_db'
    