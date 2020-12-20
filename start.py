from pprint import pprint
import requests
import os
import re
from lxml.html import fromstring

GITHUB_PAT = os.environ.get("GITHUB_PAT")
PRODUCTION = False

if PRODUCTION:
    owner = "wmcadigital"
else:
    owner = "keelanfh"

for category in ("user-research", "patterns", "styles", "components"):
    category_sing = category.rstrip("s")
    for thing in os.listdir(f"../wmn-design-system/src/www/pages/{category}"):
        if thing not in ("index.njk", "header-demo"):
            title = fromstring(requests.get(
                f"https://designsystem.wmnetwork.co.uk/{category}/{thing}/").content).findtext(".//title").split(" - ")[0]

            if category in ("patterns", "components"):
                if thing not in ("links", "table", "content-tiles", "buttons"):
                    with open(os.path.join(f"../wmn-design-system/src/www/pages/{category}/{thing}/index.njk")) as f:
                        try:
                            description = re.search(
                                "<li>\s*(.*)\s*<\/li>", f.read()).group(1)
                        except AttributeError:
                            description = ""
                source_code = f"\n\n[View the source code for this {category_sing}](https://github.com/wmcadigital/wmn-design-system/tree/master/src/wmnds/{category}/{thing})"
            else:
                source_code = ""

            issue_text = f"""## Description

{description}

Use this issue to discuss the [{title.lower()}](https://designsystem.wmnetwork.co.uk/{category}/{thing}/) {category_sing}.

## Source code

[View the source code for the description of this {category_sing}](https://github.com/wmcadigital/wmn-design-system/tree/master/src/www/pages/{category}/{thing}){source_code}
"""

            issue = {"body": issue_text,
                     "title": f"{title} {category_sing}"}

            print(requests.post(f"https://api.github.com/repos/{owner}/wmn-design-system/issues",
                                headers={"Accept": "application/vnd.github.v3+json",
                                         "Authorization": f"token {GITHUB_PAT}"},
                                json=issue))
