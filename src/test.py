import sys 
import psycopg2

args = sys.argv 
print(args)

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="example"

)
