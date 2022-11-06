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


def parse_query(raw_query: str) -> dict[str, str]:
    """ Parse raw query string (e.g. "abc=123&xd=456") to dictionary."""
    q = raw_query.split('&')
    d = {}

    for var in q:
        k = var.split('=')[0]
        val = '='.join(var.split('=')[1:])

        d[k] = val

    return d
