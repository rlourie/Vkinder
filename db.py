from pprint import pprint
import sqlalchemy

db = 'postgresql://azvezdin:12345@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

sel = connection.execute(''' 
''').fetchall()
print(sel)
