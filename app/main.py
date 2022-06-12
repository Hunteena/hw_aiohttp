from aiohttp import web

from db import orm_context
from views import AdvView


def main():
    app = web.Application()
    app.router.add_routes([
        web.post('/advs/', AdvView),
        web.get('/advs/{adv_id:\d+}/', AdvView),
        web.patch('/advs/{adv_id:\d+}/', AdvView),
        web.delete('/advs/{adv_id:\d+}/', AdvView),
    ])

    app.cleanup_ctx.append(orm_context)
    web.run_app(app)


if __name__ == '__main__':
    main()
