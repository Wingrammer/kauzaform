from .engine import engine

connection = engine.connect()
connection.close()