from pydantic import BaseModel

from fiddler.utils.response_handler import APIResponseHandler


class BaseDataSchema(BaseModel):
    '''
    Schema must be taken from api spec documentation
    '''

    @classmethod
    def deserialize(cls, response: APIResponseHandler):  # type: ignore
        data = response.get_data()

        return cls.parse_obj(data)
