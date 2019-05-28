# Copyright (c) initOS GmbH 2019
# Distributed under the MIT License (http://opensource.org/licenses/MIT).

from ..router import router
from ..tasks.merge_bot import merge_bot


@router.register("pull_request_review_comment")
async def on_pr_review_comment(event, gh, *args, **kwargs):
    """On pull request review, tag if approved or ready to merge."""
    org, repo = event.data["repository"]["full_name"].split("/")
    pr = event.data["pull_request"]["number"]
    target_branch = event.data["pull_request"]["base"]["ref"]
    user = event.data["comment"]["user"]

    with github.repository(org, repo) as gh_repo:
        if git_user_can_push(gh_repo, username):
            merge_bot_start(org, repo, pr, target_branch)
