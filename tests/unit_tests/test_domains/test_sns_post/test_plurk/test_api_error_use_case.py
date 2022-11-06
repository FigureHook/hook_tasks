from hook_tasks.domains.sns_post.plurk.errors import (
    EmptyContent,
    InValidData,
    NoCommentPermission,
    PlurkApiError,
    SameContent,
    SpamDomain,
    TooManyNew,
)
from hook_tasks.domains.sns_post.plurk.use_cases.get_plurk_api_error_use_case import (
    GetPlurkApiErrorUserCase,
)


def test_add_plurk_error():
    get_error = GetPlurkApiErrorUserCase.get_add_plurk_error
    assert isinstance(get_error({"error_text": "Invalid data"}), InValidData)
    assert isinstance(get_error({"error_text": "Content is empty"}), EmptyContent)
    assert isinstance(
        get_error({"error_text": "no-permission-to-comment"}), NoCommentPermission
    )
    assert isinstance(get_error({"error_text": "anti-flood-same-content"}), SameContent)
    assert isinstance(get_error({"error_text": "anti-flood-spam-domain"}), SpamDomain)
    assert isinstance(get_error({"error_text": "anti-flood-too-many-new"}), TooManyNew)
    assert isinstance(get_error({}), PlurkApiError)
