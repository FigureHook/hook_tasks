from celery.utils.log import get_task_logger
from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)

logger = get_task_logger(__name__)


@app.task
def create_release_ticket_for_purpose(purpose: str) -> str:
    ticket_repo = ReleaseTicketRepository(hook_api_client)
    last_time = ticket_repo.get_last_ticket_created_time_with_purpose(purpose)
    ticket = ticket_repo.create_release_ticket_info_by_time_with_purpose(
        time=last_time, purpose=purpose
    )
    return ticket.id
