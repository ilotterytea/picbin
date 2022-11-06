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

from os.path import exists
from flask import send_file

from .RoutesBlueprint import blueprint
from utils.configuration import Configuration
from utils.json_manipulator import JSONManipulator


@blueprint.get("/<id>")
def retrieve(id: str):
    """GET route for retrieving the file"""

    # Return 404 if ID not exists
    if id not in JSONManipulator.content:
        return {
            "file": None,
            "status": 404,
            "message": "Image with ID {} has never existed or its lifetime has expired!".format(id)
        }, 404


    # Local file data:
    DATA = JSONManipulator.content[id]

    # Path based on hash:
    HASH_BASED_PATH = "{}/{}{}".format(
                Configuration.content.get("SERVER", "LOCAL_FOLDER"),
                DATA["hash"],
                DATA["ext"]
    )

    # Path based on random hex:
    HEX_BASED_PATH = "{}/{}{}".format(
                Configuration.content.get("SERVER", "LOCAL_FOLDER"),
                DATA["id"],
                DATA["ext"]
    )

    if exists(HASH_BASED_PATH):
        return send_file(HASH_BASED_PATH)
    elif exists(HEX_BASED_PATH):
        return send_file(HEX_BASED_PATH)
    else:
        return {
            "file": None,
            "status": 404,
            "message": "Image with ID {} has never existed or its lifetime has expired!".format(id)
         }, 404
