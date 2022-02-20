from pydantic import BaseModel


class DTO(BaseModel):
    class Meta:
        orm_mode = True
