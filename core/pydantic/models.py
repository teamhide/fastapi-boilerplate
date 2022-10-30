import inspect

from fastapi import Query, Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseConfig, BaseModel, ValidationError

from core.utils.case_converter import snake2camel


class QueryBaseModel(BaseModel):
    """
    fastapi query param validated through PydanticModel

    - Query Param raise RequestValidationError instead of ValidationError
    - support openapi schema

    e.g.
    from core.pydantic import QueryBaseModel

    class SomeQueryParam(QueryBaseModel):
        query1: str
        query2: str
        query3: str


    @router.get(
        "/path",
        ...
    )
    def search_some(query_param:g SomeQueryParam = Depends(SomeQueryParam.as_query))
        qs1 = query_param.query1
        qs2 = query_param.query2
        qs3 = query_param.query3
        ...
        return ...

    """

    def __init_subclass__(cls, *args, **kwargs):
        field_default = Query(...)
        new_params = []
        for field in cls.__fields__.values():
            default = Query(field.default) if not field.required else field_default
            annotation = inspect.Parameter.empty

            new_params.append(
                inspect.Parameter(
                    field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=default,
                    annotation=annotation,
                )
            )

        async def _as_query(**data):
            try:
                return cls(**data)
            except ValidationError as e:
                raise RequestValidationError(e.raw_errors)

        sig = inspect.signature(_as_query)
        sig = sig.replace(parameters=new_params)
        _as_query.__signature__ = sig  # type: ignore
        setattr(cls, "as_query", _as_query)

    @staticmethod
    async def as_query(parameters: list) -> "QueryBaseModel":
        raise NotImplementedError

    class Config(BaseConfig):
        alias_generator = snake2camel


class FormBaseModel(BaseModel):
    """
    fastapi Form param validated through PydanticModel

    - Query Form raise RequestValidationError instead of ValidationError
    - support openapi schema

    e.g.
    from core.pydantic import FormBaseModel

    class SomeFormParam(FormBaseModel):
        form1: str
        form2: str
        form3: str


    @router.post(
        "/path",
        ...
    )
    def search_some(form_param:g SomeFormParam = Depends(SomeFormParam.as_form))
        form1 = form_param.form1
        form2 = form_param.form2
        form3 = form_param.form3
        ...
        return ...

    """

    def __init_subclass__(cls, *args, **kwargs):
        field_default = Form(...)
        new_params = []
        for field in cls.__fields__.values():
            default = Form(field.default) if not field.required else field_default
            annotation = inspect.Parameter.empty

            new_params.append(
                inspect.Parameter(
                    field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=default,
                    annotation=annotation,
                )
            )

        async def _as_form(**data):
            try:
                return cls(**data)
            except ValidationError as e:
                raise RequestValidationError(e.raw_errors)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig  # type: ignore
        setattr(cls, "as_form", _as_form)

    @staticmethod
    async def as_form(parameters: list) -> "FormBaseModel":
        raise NotImplementedError

    class Config(BaseConfig):
        alias_generator = snake2camel