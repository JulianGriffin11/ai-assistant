import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/app")
import logging

import nest_asyncio
from utils.event_loader import EventLoader
from workflows.email_workflow import EmailWorkflow

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)


# --------------------------------------------------------------
# Load event (update with your event uuid)
# --------------------------------------------------------------

message_event = EventLoader.load_event(
    "1da88f56-71bd-11f1-b97f-1c36bb12f2ba"
)  # update with your event uuid
spam_event = EventLoader.load_event(
    "0eafbc4a-71bd-11f1-b97f-1c36bb12f2ba"
)  # update with your event uuid
invoice_event = EventLoader.load_event(
    "875a4818-71bd-11f1-b97f-1c36bb12f2ba"
)  # update with your event uuid


# --------------------------------------------------------------
# Run workflow
# --------------------------------------------------------------

workflow = EmailWorkflow()
result = workflow.run(message_event)  # you can change this to message_event or spam_event to test different scenarios

print(result.nodes["ClassificationNode"]["result"].output.category)
print(result.model_dump_json(indent=4))