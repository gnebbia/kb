# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb artifact frozen dataclass

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import attr
from typing import List, Set, Optional

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

    def toJson(self):
        record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s""status":"%s""author":"%s","template":"%s"}' % (self.id,self.title,self.category,self.path,self.tags,self.status, self.author,self.template)
        return record
