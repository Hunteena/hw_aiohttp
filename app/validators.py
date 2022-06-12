import typing

import pydantic

import config


class CreateAdvValidator(pydantic.BaseModel):
    title: pydantic.constr(min_length=config.MIN_TITLE_LEN,
                           max_length=config.MAX_TITLE_LEN)
    desc: pydantic.constr(min_length=config.MIN_DESCRIPTION_LEN,
                          max_length=config.MAX_DESCRIPTION_LEN)
    owner: pydantic.constr(min_length=config.MIN_OWNER_NAME_LEN,
                           max_length=config.MAX_OWNER_NAME_LEN)


class UpdateAdvValidator(pydantic.BaseModel):
    title: typing.Optional[
        pydantic.constr(min_length=config.MIN_TITLE_LEN,
                        max_length=config.MAX_TITLE_LEN)
    ]
    desc: typing.Optional[
        pydantic.constr(min_length=config.MIN_DESCRIPTION_LEN,
                        max_length=config.MAX_DESCRIPTION_LEN)
    ]
    owner: typing.Optional[
        pydantic.constr(min_length=config.MIN_OWNER_NAME_LEN,
                        max_length=config.MAX_OWNER_NAME_LEN)
    ]

    @pydantic.root_validator
    def any(cls, values):
        values = {key: value for key, value in values.items()
                  if value is not None}
        if not values:
            raise ValueError("At least one field must be defined")
        return values
