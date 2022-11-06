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

from dataclasses import dataclass, asdict
from json import dumps


@dataclass
class FileData:
    """
    Dataclass for file data.
    """

    internal_id: str
    """Internal ID that generated while processing the POST / request.
    It can be random hex chars (e.g. 123ab6), random words (e.g. BeautifulSillyImage).
    """

    extension: str
    """Extension of file (e.g. .png, .mp4, .json)"""

    mime_type: str
    """MIME type of file (e.g. image/png, video/mp4, application/json)"""

    hash_file: str
    """Hash summary of file.
    Used to combine files with identical hash summary for storage optimization.
    Can be disabled in your configuration file, set GENERATE_LINKED_FILES to 0
    """
    
    secret_key: str
    """Secret key for some interaction with file, like for premature deletion."""

    timestamp: str
    """Timestamp when the file was uploaded."""

    keep_alive: int
    """Keep alive (ms) the file until it's deletion."""

    @property
    def __dict__(self):
        return asdict(self)
    
    @property
    def json(self):
        return dumps(self.__dict__)
