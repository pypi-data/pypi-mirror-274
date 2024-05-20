from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers
from os import listdir, path
from typing import List

from flet_easy_static.pagesy import AddPagesy


def automatic_routing(dir: str) -> List[AddPagesy]:
    """
    A function that automatically routes through a directory to find Python files, extract AddPagesy objects, and return a list of them.

    Parameters:
    - dir (str): The directory path to search for Python files.

    Returns:
    - List[AddPagesy]: A list of AddPagesy objects found in the specified directory.
    """

    print(f"Starting automatic routing in directory: {dir}")
    print(f"List of files in directory: {listdir(dir)}")


    pages = []
    for file in listdir(dir):
        if (file.endswith(".py") or file.endswith(".pyc")) and file != "__init__.py":
            spec = spec_from_file_location(path.splitext(file)[0], path.join(dir, file))
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            for _, object_page in getmembers(module):
                if isinstance(object_page, AddPagesy):
                    pages.append(object_page)
    if len(pages) == 0:
        print("No instances of AddPagesy found.")

        raise ValueError(
            "No instances of AddPagesy found. Check the assigned path of the 'path_views' parameter of the class (FletEasy)."
        )
    print(f"Finished automatic routing. Found {len(pages)} AddPagesy objects.")
    print(f"List of AddPagesy objects found: {pages}")
    return pages
