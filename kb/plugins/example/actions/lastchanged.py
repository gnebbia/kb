# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""Acttion for last_changed function

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

def last_changed(args: Dict[str, str], config: Dict[str, str]): 
    from pathlib import Path
    import arrow
    from kb.db import get_artifact_by_id, create_connection
    from kb.entities.artifact import Artifact
    from kb.filesystem import get_last_modified_time
    from kb.plugin import get_modules, get_plugin_status, get_plugin_info

    
    # This is the happy path - need to check for error conditions
    conn = create_connection(config["PATH_KB_DB"])
    artifact = get_artifact_by_id(conn,args['id'])
    document=str(Path(config['PATH_KB_DATA'],artifact.path))

    last_updated = get_last_modified_time(document)

    results = {}

    results['artifact'] = artifact
    results['document'] = document
    results['last_updated'] = last_updated
    return results