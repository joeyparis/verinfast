import json
import os
from pathlib import Path
from typing import List

from curses.ascii import isdigit

from dependencies.walkers.classes import Walker, Entry
from typing import TextIO

class NodeWalker(Walker):
    def initialize(self, root_path: str="./"):
        self.install_points:List[Path] = []
        for p in Path(root_path).rglob('**/*.*'):
            if p.name in self.manifest_files:
                self.install_points.append(p)
        for p in self.install_points:    
            target_dir = Path(p).parent
            os.chdir(target_dir)
            os.system("npm install")
            self.walk(path=str(target_dir))       

    def parse(self, path:TextIO):
        entry = {}
        try:
            d=json.load(path)
            key=d["name"] + "@" + d["version"]
            entry["source"] = "npm"
            entry["name"] = d["name"]
            entry["specifier"] = "==" + d["version"]
            if type(d["license"]) == type({}):
                license[key]=d["license"]["type"]
            else:
                license[key]=d["license"]
            entry["license"] = license[key]
            entry["requires"] = []
            for key in d["dependencies"].keys():
                k = key
                value = d["dependencies"]
                if isdigit(value[0]):
                    value="=="+value
                entry["requires"].append(k+value)

            entry["required_by"] = []
            entry["summary"] = d["description"]
            e = Entry(
                name=entry["name"],
                specifier=entry["specifier"],
                source=entry["source"],
                license=entry["license"],
                summary=entry["summary"]
            )
            self.entries.append(e)
        except:
            pass

nodeWalker = NodeWalker(manifest_type='json', manifest_files=["package.json"])
