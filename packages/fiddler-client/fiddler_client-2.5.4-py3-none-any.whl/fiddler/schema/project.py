from fiddler.schema.base import BaseDataSchema


class Project(BaseDataSchema):
    name: str
    organization_name: str
