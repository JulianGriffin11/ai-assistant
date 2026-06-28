from pydantic import BaseModel, Field

class Sender(BaseModel):
    email: str
    name: str

class EmailObject(BaseModel):
    attachments: list = []
    bcc: list = []
    body: str
    cc: list = []
    date: int
    folders: list = []
    from_: Sender = Field(..., alias="from")
    grant_id: str
    id: str
    object: str
    reply_to: list = []
    snippet: str
    starred: bool
    subject: str
    thread_id: str
    to: list
    unread: bool
