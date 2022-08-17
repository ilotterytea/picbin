// Copyright 2022 NotDankEnough (ilotterytea)
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { Command } from "commander";

/**
 * Silly Command-Line Interface.
 * @returns options.
 */
function CLI(): Record<string, string | boolean> {
    const Program = new Command();

    Program.option("--init", "Generate the neccessary files.", false);
    Program.option("--no-ssl", "Run application in debug mode. Port for HTTP connection is \"8080\" instead of standard \"80\".", false);

    Program.parse(process.argv);
    return Program.opts();
}

export default CLI;