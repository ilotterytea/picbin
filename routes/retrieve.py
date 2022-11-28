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

@blueprint.get("/<id>")
async def retrieve(id: str):
    """GET route for retrieving the file"""

    # Return 404 if ID not exists
    if not exists(f"uploads/{id}"):
        return {
            "file": None,
            "status": 404,
            "message": "Image with ID {} has never existed or its lifetime has expired!".format(id)
        }, 404

    return send_file(f"uploads/{id}")
