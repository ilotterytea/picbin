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

from .filegentype import FileGenType
from secrets import token_hex


def FileIdGen(
        length: int,
        type: FileGenType
) -> str:
    """
    Generate an ID for file.

    :param length: Length of final ID.
    :param type: Type of file ID generation
    :return: ID
    """
    id = ""

    match type:
        case FileGenType.RANDOM_HEX:
            id = token_hex(length)[:-length]

    return id