from surrealdb import Surreal

db = Surreal()


class SurrealDB:
    async def __init__(self):
        await self.connect()

    async def connect():
        try:
            await db.connect("ws://localhost:8080/rpc")
            await db.signin({"user": "root", "pass": "root"})
            await db.use("test", "test")
            print("SurrealDB conectado com sucesso!")
        except Exception as error:
            print(f"CONNECTION ERROR: {error}")

    async def select(table: str):
        await db.select(table)
    
    async def create(table: str, data: dict):
        await db.create(thing=table, data=data)
    
    async def query(sql: str):
        await db.query(sql)
