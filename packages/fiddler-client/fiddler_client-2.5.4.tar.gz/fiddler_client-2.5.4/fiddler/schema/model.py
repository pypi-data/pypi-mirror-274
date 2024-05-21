from typing import Optional
from uuid import UUID

from fiddler.schema.base import BaseDataSchema


class Model(BaseDataSchema):
    id: Optional[int] = None
    name: str
    project_name: Optional[str]
    organization_name: Optional[str]
    # @TODO: OAS says info is optional. Check it.
    info: Optional[dict] = None
    file_list: Optional[list] = None
    model_type: Optional[str] = None
    framework: Optional[str] = None
    requirements: Optional[str] = None
    job_uuid: Optional[UUID]
