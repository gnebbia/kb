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
import json

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
        record = "{"
        if self.id:
            record =  record + '"id":' + str(self.id)  + '"'
        if self.title:
            record = record + ',"title":"' + self.title  + '"'
        if self.category:
            record = record + ',"category":"' + self.category  + '"'
        if self.path:
            record = record + ',"path":"' + self.path  + '"'
        if self.tags:
            record = record + ',"tags":"' + self.tags  + '"'
        if  self.status:
            record = record + ',"status":"' + self.status  + '"'
        if self.author:
            record = record + ',"author":"' + self.author  + '"'
        if  self.template:
            record = record + ',"template":"' + self.template  + '"'

        record = record + "}"
        return record
