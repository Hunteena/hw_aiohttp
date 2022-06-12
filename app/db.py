import asyncio
import errno

from gino import Gino
import config

db = Gino()


class AdvModel(db.Model):
    __tablename__ = 'advs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(config.MAX_TITLE_LEN), nullable=False)
    desc = db.Column(db.String(config.MAX_DESCRIPTION_LEN), nullable=False)
    creation_date = db.Column(db.Date, server_default=db.func.current_date())
    owner = db.Column(db.String(config.MAX_OWNER_NAME_LEN), nullable=False)

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.desc,
                'creation_date': str(self.creation_date),
                'owner': self.owner}


async def orm_context(app):
    connected = False
    for i in range(1, config.DB_CONN_RETRIES + 1):
        print(f"Connecting to database: attempt {i}")
        try:
            connected = await db.set_bind(config.PG_DSN)
            break
        except OSError:
            await asyncio.sleep(config.DB_CONN_INTERVAL)

    if not connected:
        raise ConnectionRefusedError(
            errno.ECONNREFUSED,
            f"Connection fails after {config.DB_CONN_RETRIES} retries. "
            f"Try to increase DB_CONN_RETRIES or DB_CONN_INTERVAL in config.py"
        )
    print('Database connected')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('Database disconnected')

