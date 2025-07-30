__author__ = "akeshavan"
from jinja2 import Environment, FileSystemLoader
import os
import simplejson as json


def load_json(filename):
    """Load data from a json file
    Parameters
    ----------
    filename : str
        Filename to load data from.
    Returns
    -------
    data : dict
    """

    with open(filename, "r") as fp:
        data = json.load(fp)
    return data


files_to_generate = [
    {"filename": "index.html.j2", "location": "./_site"},
    {"filename": "css/stylish-portfolio.css.j2", "location": "./_site"},
]

env = Environment(loader=FileSystemLoader("./_site"))
info = load_json("data.json")

for f in files_to_generate:
    template = env.get_template(f["filename"])
    outfile = os.path.join(f["location"], f["filename"].replace(".j2", ""))
    print("writing", outfile)
    with open(outfile, "w") as q:
        q.write(template.render(**info))
