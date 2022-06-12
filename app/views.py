import json

import pydantic
from aiohttp import web

from db import AdvModel
from validators import CreateAdvValidator, UpdateAdvValidator


class AdvView(web.View):
    async def post(self):
        adv_data = await self.request.json()
        try:
            validated_data = CreateAdvValidator(**adv_data).dict()
        except pydantic.ValidationError as er:
            raise web.HTTPBadRequest(text=er.json(),
                                     content_type='application/json')
        new_adv = await AdvModel.create(**validated_data)
        return web.json_response(new_adv.to_dict())

    async def _get_adv_object(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await AdvModel.get(adv_id)
        if not adv:
            error_text = json.dumps({'404': 'adv does not exist'})
            raise web.HTTPNotFound(text=error_text,
                                   content_type='application/json')
        return adv

    async def get(self):
        adv = await self._get_adv_object()
        return web.json_response(adv.to_dict())

    async def delete(self):
        adv = await self._get_adv_object()
        await adv.delete()
        return web.json_response({'200': f'Adv {adv.id} deleted'})

    async def patch(self):
        adv_data = await self.request.json()
        try:
            validated_data = UpdateAdvValidator(**adv_data).dict()
        except pydantic.ValidationError as er:
            raise web.HTTPBadRequest(text=er.json(),
                                     content_type='application/json')
        adv = await self._get_adv_object()
        await adv.update(**validated_data).apply()
        return web.json_response(adv.to_dict())
