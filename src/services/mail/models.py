import datetime

from pydantic import Field, BaseModel, field_validator


class Mailbox(BaseModel):
    login: str
    domain: str

    @property
    def mail(self) -> str:
        return f"{self.login}@{self.domain}"

    @classmethod
    @field_validator("domain")
    def validate_domain(cls, value: str) -> str:
        if not value.endswith((".com", ".net", ".org")):
            raise ValueError("Domain must ends with one of these .com, .net, .org")
        return value


class Attachment(BaseModel):
    filename: str
    content_type: str = Field(alias="contentType")
    size: int


class Message(BaseModel):
    id: int
    from_: str = Field(alias="from")
    subject: str
    date: datetime.datetime
    attachments: list[Attachment]
    body: str
    text_body: str = Field(alias="textBody")
    html_body: str = Field(alias="htmlBody")
