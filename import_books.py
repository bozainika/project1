import pandas
from sqlalchemy import create_engine
import os
from pandas.io import sql
import pymysql

if not os.getenv('DATABASE_URL'):
	raise RuntimeError('DATABASE_URL not set')

engine=create_engine(os.getenv('DATABASE_URL'))
#db=engine.connect()
df=pandas.read_csv('books.csv')
df.to_sql(name='books',con=engine,schema='project1',
				if_exists='replace')
result=engine.execute('select author from books');
for row in result:
	print("\n Author:", row['author'])
