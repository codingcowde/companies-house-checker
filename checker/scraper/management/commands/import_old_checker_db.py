from lib2to3.pytree import Base
from django.core.management.base import BaseCommand
from scraper.models import Subscription
import sqlite3 as db
from sqlite3 import DatabaseError

class Command(BaseCommand):  
    def add_arguments(self, parser):
        parser.add_argument('db_file_path', nargs='+', type=str)
       
        
    def handle(self, *args, **options):
        """ 
            imports from a legacy database
            needas a filename as parameter"""
        for db_file in options['db_file_path']:        
            
            connection = None
            try:
                connection = db.connect(db_file)
                print(f"Database ready. SQLite {db.version}")
                print("Checking data ...")
                cursor= connection.cursor()
                response = cursor.execute("SELECT * FROM user")            
                for data in response:
                    name = data[0]
                    email = data[1]
                    flag = data[2]
                   # if sub:= Subscription.objects.filter(name=name, email=email)[:1][0]:
                    #    return
                    sub = Subscription.objects.create(name=name, email=email, flag=flag)
                    sub.save()
                print('All users migrated.')

            except DatabaseError as e:
                if f"{e}" == "no such table: user":
                    print("No data found.")                
                else:
                    print(f"Error: {e}")
            finally:
                if connection:                
                    connection.close()
                    print("Connection closed.")
        
        
                
            
        