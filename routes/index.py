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

from .RoutesBlueprint import blueprint
from flask import render_template, send_from_directory, send_file
from os.path import join


@blueprint.get("/")
def index():
    """GET route for index page."""
    return render_template("index.html")

@blueprint.get("/favicon.ico")
def favicon():
    return send_file(f"static/favicon.ico")
