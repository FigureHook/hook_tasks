from ..repositories.release_ticket_repository import ReleaseTicketRepositoryInterface
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)


class CreateReleaseTicketUseCase:
    ticket_repo: ReleaseTicketRepositoryInterface

    def __init__(self, ticket_repo: ReleaseTicketRepository) -> None:
        self.ticket_repo = ticket_repo

    def create_release_ticket_for_purpose(self, purpose: str) -> str:
        last_time = self.ticket_repo.get_last_ticket_created_time_with_purpose(purpose)
        ticket = self.ticket_repo.create_release_ticket_info_by_time_with_purpose(
            time=last_time, purpose=purpose
        )
        return ticket.id
