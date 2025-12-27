from pydantic import BaseModel, Field
from typing import Optional
import re

E164_REGEX = re.compile(r"^\+\d+$")

class WebhookMessage(BaseModel):
    message_id: str = Field(min_length=1)
    from_: str = Field(alias="from")
    to: str
    ts: str
    text: Optional[str] = Field(default=None, max_length=4096)

    @staticmethod
    def validate_e164(value: str):
        if not E164_REGEX.match(value):
            raise ValueError("Invalid E.164 format")
        return value

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_e164(self.from_)
        self.validate_e164(self.to)
