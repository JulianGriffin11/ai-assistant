import logging
from core.nodes.base import Node
from core.task import TaskContext
from schemas.nylas_email_schema import EmailObject
from services.nylas_service import NylasService


class ProcessInvoiceNode(Node):
    def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Processing invoice")

        email_object = EmailObject(**task_context.event.data["object"])

        nylas_service = NylasService()
        file_content = nylas_service.download_attachment(
            email=email_object, download=True
        )

        logging.info(f"File content: {file_content}")

        return task_context