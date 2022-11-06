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

from flask import Flask
from os.path import exists
from os import mkdir
from routes.RoutesBlueprint import blueprint
from utils import Configuration, JSONManipulator

import logging


logging.basicConfig(
        format="%(message)s"
)

Configuration.load("config.ini")
JSONManipulator.load("uploaded.json")

if not exists(Configuration.content.get("SERVER", "LOCAL_FOLDER")):
    mkdir(Configuration.content.get("SERVER", "LOCAL_FOLDER"))


app = Flask(__name__, template_folder="templates", static_folder="static")
app.register_blueprint(blueprint)
