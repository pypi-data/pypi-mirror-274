import os

from .ArchFlow import ArchFlow


def main(roots_path_json=None):
    roots_path_json.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "db.json")))
    arch = ArchFlow()
    args = arch.handle_args()
    arch.handler_functions_flow(args, roots_path_json)

