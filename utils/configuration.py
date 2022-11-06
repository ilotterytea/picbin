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

from configparser import ConfigParser
from os.path import exists


class Configuration:
    content = ConfigParser()

    @classmethod
    def load(cls, file_path: str) -> None:
        should_be_rewritten = False

        if exists(file_path) is True:
            cls.content.read(file_path)

        if cls.content.has_section("SERVER") is False: cls.content.add_section("SERVER"); should_be_rewritten = True;
        if cls.content.has_option("SERVER", "LOCAL_FOLDER") is False: cls.content.set("SERVER", "LOCAL_FOLDER", "./uploads"); should_be_rewritten = True;
        if cls.content.has_option("SERVER", "DEFAULT_KEEPALIVE_MS") is False: cls.content.set("SERVER", "DEFAULT_KEEPALIVE_MS", "7200000"); should_be_rewritten = True;
        if cls.content.has_option("SERVER", "MAX_KEEPALIVE_MS") is False: cls.content.set("SERVER", "MAX_KEEPALIVE_MS", "1209600000"); should_be_rewritten = True;
        if cls.content.has_option("SERVER", "DECLINE_MIMETYPES") is False: cls.content.set("SERVER", "DECLINE_MIMETYPES", "image/jpeg"); should_be_rewritten = True;
        if cls.content.has_option("SERVER", "ENABLE_DELETION_BY_LINK") is False: cls.content.set("SERVER", "ENABLE_DELETION_BY_LINK", "True"); should_be_rewritten = True;

        if cls.content.has_section("FILES") is False: cls.content.add_section("FILES"); should_be_rewritten = True;
        if cls.content.has_option("FILES", "NAME_LENGTH") is False: cls.content.set("FILES", "NAME_LENGTH", "6"); should_be_rewritten = True;
        if cls.content.has_option("FILES", "FILE_GEN_TYPE") is False: cls.content.set("FILES", "FILE_GEN_TYPE", "0"); should_be_rewritten = True;
        if cls.content.has_option("FILES", "GENERATE_LINKED_FILES") is False: cls.content.set("FILES", "GENERATE_LINKED_FILES", "True"); should_be_rewritten = True;

        if should_be_rewritten is True:
            cls.save(file_path)

    @classmethod
    def save(cls, file_path: str) -> bool:
        with open(file_path, "w") as file:
            cls.content.write(file)

        return True
