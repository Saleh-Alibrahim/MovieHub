import psycopg2

# Connect to db
conn = psycopg2.connect(host="localhost", database="moviehub",
                        user="postgres", password="postgres")
