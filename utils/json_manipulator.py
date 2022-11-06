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

from json import dump, load
from os.path import exists


class JSONManipulator:
    """Manipulator with JSON data."""

    content: dict | list = any
    """File content."""

    LATEST_FILE_PATH = ""
    """Latest file path that has been used when loading file."""

    @classmethod
    def load(cls, file_path: str) -> None:
        """Load JSON file and convert into Python dictionary."""

        cls.LATEST_FILE_PATH = file_path
        if exists(file_path):
            with open(file_path, "r") as file:
                cls.content = load(file)
                file.close()
        else:
            cls.content = {}

    @classmethod
    def save(cls, file_path: str) -> bool:
        """Save the Python dictionary to JSON file."""

        with open(file_path, "w") as file:
            dump(cls.content, file, indent=2)
            file.close()

        return True

