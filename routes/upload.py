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

from flask import request
from datacls import FileData
from mimetypes import guess_extension
from datetime import datetime
from os import rename
from secrets import token_hex

from .RoutesBlueprint import blueprint
from utils.files import FileIdGen, FileGenType, get_file_hash
from utils import Configuration, JSONManipulator


@blueprint.post("/upload")
def upload():
    """
    POST route for uploading file.
    """

    # Return 400 if no file provided:
    if "file" not in request.files:
        return {
            "file": 400,
            "message": "No file provided."
        }, 400
    
    # File from form:
    FILE = request.files["file"]
    keep_alive_ms = Configuration.content.get("SERVER", "DEFAULT_KEEPALIVE_MS")

    # Reject request with status 400 if MIME type of file is forbidden by config:
    if FILE.mimetype in Configuration.content.get("SERVER", "DECLINE_MIMETYPES").split(';'):
        return {
            "status": 400,
            "message": "MIME type of your file is forbidden in this file hosting settings."
        }, 400

    # File ID:
    file_id = FileIdGen(int(Configuration.content.get("FILES", "NAME_LENGTH")), FileGenType.RANDOM_HEX)

    # Secret key for DELETE requests:
    SECRET_KEY = token_hex(16)

    # Convert MIME type (e.g. image/png) to extension (e.g. .png):
    EXT = guess_extension(FILE.mimetype)

    # Re-generate file ID if ID is already exists:
    while file_id in JSONManipulator.content:
        file_id = FileIdGen(int(Configuration.content.get("FILES", "NAME_LENGTH")), FileGenType.RANDOM_HEX)

    # Path for future file:
    PATH = "{}/{}{}".format(Configuration.content.get("SERVER", "LOCAL_FOLDER"), file_id, EXT)

    # Save local file:
    FILE.save(PATH)

    # Hash summary of file:
    hash_file = None

    # Get hash of file if "GENERATE_LINKED_FILES" is 1 in configuration:
    if bool(int(Configuration.content.get("FILES", "GENERATE_LINKED_FILES"))):
        hash_file = get_file_hash(PATH)

        # Move file to clone by hash (for optimizing the storage?):
        rename(
            PATH,
            "{}/{}{}".format(Configuration.content.get("SERVER", "LOCAL_FOLDER"), hash_file, EXT)
        )

    FILE_DATA = FileData(
        file_id,
        EXT,
        FILE.mimetype,
        hash_file,
        SECRET_KEY,
        str(datetime.now()),
        keep_alive_ms
    )

    # Final JSON file data:
    data = {
        "file": {
            "data": FILE_DATA.__dict__,
            "get": "{}{}{}".format(request.host_url, file_id, EXT),
            "delete": "{}{}{}?key={}".format(request.host_url, file_id, EXT, SECRET_KEY)
        },
        "status": 200,
        "message": "Success!"
    }

    JSONManipulator.content[file_id] = data["file"]["data"]
    JSONManipulator.save(JSONManipulator.LATEST_FILE_PATH)

    return data, 200
