# Copyright 2019 Simone Rubino - Agile Business Group
# Distributed under the MIT License (http://opensource.org/licenses/MIT).
import pytest

from oca_github_bot.tasks.label_modified_addons import label_modified_addons


@pytest.mark.vcr()
def test_label_modified_addons(mocker):
    label_modified_addons("OCA", "mis-builder", "610", dry_run=False)
