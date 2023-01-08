from discord.app_commands import (
    CommandTree,
    Group,
    Command
)
from os import PathLike
from os.path import exists
import json

__all__ = ["CommandTreeCacher"]

class CommandTreeCacher(object):

    tree : CommandTree



    def __init__(self, current_tree : CommandTree):
        self.tree = current_tree



    def recursive_group_search(self, group : Group) -> dict:
        return {
            "name" : group.name,
            "commands" : [c.name if isinstance(c, Command) else self.recursive_group_search(c) for c in group.commands]
        }



    def generate_json_tree(self):

        generated_json_tree = []
        
        for command in self.tree.walk_commands():
            
            if isinstance(command, Group):
                generated_json_tree.append(
                    self.recursive_group_search(command)
                )
            
            elif isinstance(command, Command) and command.parent is None:
                generated_json_tree.append({"name" : command.name})

        return generated_json_tree



    def dump_new_tree(self, fp : PathLike, tree_json : dict) -> None:
        
        with open(fp, "w+") as f:
            json.dump(tree_json, f, indent=4)



    def tree_has_changes(self, fp : PathLike, update_if_changed : bool = False) -> bool:
        """Returns true if the tree has changed at all"""
        my_generated_tree = self.generate_json_tree()

        if not exists(fp):
            self.dump_new_tree(fp, my_generated_tree)
            return True

        with open(fp, "r") as cached_tree_json:
            json_unpacked = json.load(cached_tree_json)

        verdict = json_unpacked != my_generated_tree

        if verdict and update_if_changed: 
            self.dump_new_tree(fp, my_generated_tree)

        return verdict