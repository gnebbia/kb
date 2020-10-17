# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb view API module 

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""
import sys
sys.path.append('kb')

from flask import make_response
from pathlib import Path
from typing import Dict
import kb.filesystem as fs
from kb.db import get_artifact_by_id, get_artifacts_by_filter
import base64

def view_by_id(conn,id,DEFAULT_CONFIG):
    """
    Retrieve an artifact by ID

    Arguments:
    conn:           - an opoen DB connection
    args:           - ID        }
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """

    # Default response is an error
    response = (make_response(({'Error': 'No artifacts were found'}), 404))
 
    if id:
        artifact = get_artifact_by_id(conn, id)
        if artifact is None:
            return (make_response(({'Error': 'There is no artifacts with the ID of ' + id}), 404))

        category_path = Path(str(DEFAULT_CONFIG["PATH_KB_DATA"]), str(artifact.category))
        artifact_file = Path(str(category_path), str(artifact.title))

        with open(artifact_file, "rb") as artifact_file:
            encoded_string = base64.b64encode(artifact_file.read())
        record = "{" + toJson(artifact)  + "{" + "Content:" + str(encoded_string) + "}"
        response = (make_response((record), 200))

    
    return(response)

def view_by_title(conn,title,DEFAULT_CONFIG):
    """
    Retrieve an artifact by title

    Arguments:
    conn:           - an opoen DB connection
    title:          - title of the artifact to view
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """

    artifact = get_artifacts_by_filter(conn, title=title, is_strict=True)
    
    # Set default response - nothing found
    response = (make_response(({'Error': 'There are no artifacts with the title of ' + title}), 404))

    if len(artifact) > 1:
        response =  make_response(({'Error': 'There is more than one artifact with the title of ' + title}), 301)
    
    if len(artifact) == 0:
        response = (make_response(({'Error': 'There are no artifacts with the title of ' + title}), 404))
    
    if len(artifact) == 1:
        category_path = Path(str(DEFAULT_CONFIG["PATH_KB_DATA"]), artifact[0].category)
        artifact_file = Path(str(category_path), str(artifact[0].title))
        with open(artifact_file, "rb") as artifact_file:
            encoded_string = base64.b64encode(artifact_file.read())
        record = "{" + toJson(artifact[0])  + "{" + "content:" + str(encoded_string) + "}"
        response = (make_response((record), 200))
   
    return (response)



def view_by_name(conn,title,category,DEFAULT_CONFIG):
    """
    Retrieve an artifact by name

    Arguments:
    conn:           - an opoen DB connection
    title:          - title of the artifact to view
    category:       - category of the artifact to view
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """
    artifact = db.get_artifacts_by_filter(conn, title=title, category=category, is_strict=True)
    
    # Set default response - nothing found
    response = (make_response(({'Error': 'There are no artifacts with the name of ' + category + "/" + title}), 404))

    if len(artifact) > 1:
        response =  make_response(({'Error': 'There is more than one artifact with the name of ' + category + "/" + title}), 301)
    
    if len(artifact) == 0:
        response = (make_response(({'Error': 'There are no artifacts with the name of ' + category + "/" + title}), 404))
    
    if len(artifact) == 1:
        category_path = Path(str(DEFAULT_CONFIG["PATH_KB_DATA"]), artifact[0].category)
        artifact_file = Path(str(category_path), str(artifact[0].title))
        with open(artifact_file, "rb") as artifact_file:
            encoded_string = base64.b64encode(artifact_file.read())
        record = "{" + toJson(artifact[0])  + "{" + "content:" + str(encoded_string) + "}"
        response = (make_response((record), 200))

    return (response)
   
"""
    This function converts an Artifact object to a Json document

    Arguments:
    self   - Artifact object

    Returns:
    A Json document
"""

def toJson(self):
    record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s""status":"%s""author":"%s","template":"%s"}' % (self.id,self.title,self.category,self.path,self.tags,self.status, self.author,self.template)
    
    return record

