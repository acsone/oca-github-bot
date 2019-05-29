# Copyright (c) initOS GmbH 2019
# Distributed under the MIT License (http://opensource.org/licenses/MIT).

import pytest
from .common import EventMock
from oca_github_bot.version_branch import make_merge_bot_branch
from oca_github_bot.webhooks import on_issue_comment


def create_test_data(pr, user, body):
    return {
        "repository": {
            "full_name": "OCA/some-repo"
        },
        "issue": {
            "number": pr if pr else None,
            "pull_request": bool(pr),
        },
        "comment": {
            "body": body,
            "user": {"login": user},
        },
    }


@pytest.mark.asyncio
async def test_on_issue_comment_no_pr(mocker):
    mocker.patch(
        "oca_github_bot.webhooks.on_issue_comment.parse_commands"
    )

    data = create_test_data(False, 'test-user', '/ocabot merge')
    event = EventMock(data)
    await on_issue_comment.on_issue_comment(event, None)
    on_issue_comment.parse_commands.assert_not_called()


@pytest.mark.asyncio
async def test_on_issue_comment_valid_pr(mocker):
    cmd_mock = mocker.Mock()
    mocker.patch(
        "oca_github_bot.webhooks.on_issue_comment.parse_commands"
    ).return_value = [cmd_mock]

    body = "test_message"

    # Completed
    data = create_test_data(42, "test-user", body)
    event = EventMock(data)
    await on_issue_comment.on_issue_comment(event, None)
    on_issue_comment.parse_commands.assert_called_once_with(body)
    cmd_mock.delay.assert_called_once_with(
        "OCA", "some-repo", 42, "test-user"
    )
