# Copyright 2022 NotDankEnough (iLotterytea)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from difflib import SequenceMatcher
from flask import request
from os import remove
from os.path import exists

from .RoutesBlueprint import blueprint
from utils import Configuration, JSONManipulator, parse_query


@blueprint.delete("/<id>")
def burn(id: str):
    """
    DELETE route for deleting a file.
    """

    # Return 405 if premature deletion is disabled in configuration:
    if not bool(int(Configuration.content.get("SERVER", "ENABLE_DELETION_BY_LINK"))):
        return {
            "file": None,
            "status": 405,
            "message": "Deletion file by link is disabled in this file hosting's settings."
        }, 405

    # Return 404 if ID not found:
    if id not in JSONManipulator.content:
        return {
            "file": None,
            "status": 404,
            "message": "Image with ID {} has never existed or its lifetime has expired!".format(id)
        }, 404

    # Local file data:
    DATA = JSONManipulator.content[id]

    # Parsed query:
    QUERY = parse_query(str(request.query_string)[2:-1])

    # Return 401 if key is not provided or provided key and file key is not match:
    if "key" not in QUERY or SequenceMatcher(a=QUERY["key"], b=DATA["secret_key"]).ratio() < 1:
        return {
            "file": None,
            "status": 401,
            "message": "Original hash key not match with yours."
        }, 401

    # Erase all records with same hash summary if GENERATE_LINKED_FILES is 1:
    if bool(int(Configuration.content.get("FILES", "GENERATE_LINKED_FILES"))):
        remove("{}/{}{}".format(Configuration.content.get("SERVER", "LOCAL_FOLDER"), DATA["hash"], DATA["ext"]))

        on_deletion_ids = []

        for mfid in JSONManipulator.content:
            if SequenceMatcher(a=DATA["hash"], b=JSONManipulator.content[mfid]["hash"]).ratio() == 1:
                on_deletion_ids.append(mfid)

        for mfid in on_deletion_ids:
            del JSONManipulator.content[mfid]

    else:
        remove("{}/{}{}".format(Configuration.content.get("SERVER", "LOCAL_FOLDER"), DATA["internal_id"], DATA["extension"]))

    # Save to JSON:
    JSONManipulator.save(JSONManipulator.LATEST_FILE_PATH)

    return {
        "file": {
            "data": DATA,
            "get": None,
            "delete": None
        },
        "status": 200,
        "message": "Successfully deleted the image from server!"
    }, 200
