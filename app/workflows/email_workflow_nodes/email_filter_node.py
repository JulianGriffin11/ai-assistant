from core.nodes.base import Node
from core.task import TaskContext
from schemas.nylas_email_schema import EmailObject, Sender
from dotenv import load_dotenv
import os
import logging

load_dotenv()


class EmailFilterNode(Node):
    def process(self, task_context: TaskContext) -> TaskContext:
        # 1. Grab the raw dictionary out of the context
        raw_email_data = task_context.event.data["object"]

        # 2. Extract the single dictionary from the list BEFORE Pydantic sees it
        if isinstance(raw_email_data.get("from"), list) and len(raw_email_data["from"]) > 0:
            raw_email_data["from"] = raw_email_data["from"][0]

        # 3. Now pass the cleaned data to Pydantic. It will validate perfectly!
        email_object = EmailObject(**raw_email_data)

        EMAIL = os.getenv("EMAIL")

        # 4. 'email_object.from_' is now a single Sender object. No [0] needed anymore!
        sender: Sender = email_object.from_
        
        if sender.email == EMAIL:
            logging.info(f"Processing email from {sender.email}")
            return task_context
        else:
            task_context.stop_workflow(
                reason=f"Email from {sender.email} is not from {EMAIL}"
            )
            logging.info(f"Skipping email from {sender.email}")
            return task_context