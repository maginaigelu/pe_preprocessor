from pydantic import BaseModel


class BaseConfig(BaseModel):

    def as_options(self, **options):
        result = self.dict(by_alias=True)
        result.update(options)
        return result
