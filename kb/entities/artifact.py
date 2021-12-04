# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb artifact frozen dataclass

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

# from typing import List, Set, Optional
from typing import Optional

import attr


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Artifact:
    id: Optional[int]
    title: str
    category: str
    path: Optional[str] = None
    tags: Optional[str] = None
    status: Optional[str] = None
    author: Optional[str] = None
    template: Optional[str] = None
