from typing import Any, Dict

from ..errors import (
    EmptyContent,
    InValidData,
    NoCommentPermission,
    PlurkApiError,
    SameContent,
    SpamDomain,
    TooManyNew,
)


class GetPlurkApiErrorUserCase:
    @classmethod
    def get_add_plurk_error(cls, error_body: Dict[str, Any]) -> PlurkApiError:
        """
        HTTP 400 BAD REQUEST with {"error_text": "Invalid data"} as body
        HTTP 400 BAD REQUEST with {"error_text": "Content is empty"} as body
        HTTP 400 BAD REQUEST with {"error_text": "no-permission-to-comment"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-same-content"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-spam-domain"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-too-many-new"} as body
        """
        error_text = error_body.get("error_text")

        if error_text == "Invalid data":
            return InValidData(error_body)

        if error_text == "Content is empty":
            return EmptyContent(error_body)

        if error_text == "no-permission-to-comment":
            return NoCommentPermission(error_body)

        if error_text == "anti-flood-same-content":
            return SameContent(error_body)

        if error_text == "anti-flood-spam-domain":
            return SpamDomain(error_body)

        if error_text == "anti-flood-too-many-new":
            return TooManyNew(error_body)

        return PlurkApiError(error_body)
