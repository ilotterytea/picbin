# Copyright 2022 NotDankEnough (ilotterytea)
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

from utils import Configuration
from .RoutesBlueprint import blueprint


@blueprint.get("/api/get_config")
def get_config_data():
    """GET route for getting the server configuration.
    """

    return {
        "DEFAULT_KEEPALIVE_MS": Configuration.content.get("SERVER", "DEFAULT_KEEPALIVE_MS"),
        "MAX_KEEPALIVE_MS": Configuration.content.get("SERVER", "MAX_KEEPALIVE_MS"),
        "REJECT_MIMETYPES": Configuration.content.get("SERVER", "DECLINE_MIMETYPES").split(';'),
        "DELETION_BY_KEY": bool(int(Configuration.content.get("SERVER", "ENABLE_DELETION_BY_LINK"))),
        "LINKED_FILES": bool(int(Configuration.content.get("FILES", "GENERATE_LINKED_FILES")))
    }, 200
