import os
import re

def test_page_links_manifest():
    """
    Don’t hit a Flask route (your test app may not have /home_page/).
    Instead, verify base.html contains the manifest link.
    """

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    base_html_path = os.path.join(project_root, "templates", "base.html")

    assert os.path.exists(base_html_path), f"base.html not found at: {base_html_path}"

    html = open(base_html_path, "r", encoding="utf-8").read()

    # Must contain rel="manifest"
    assert re.search(r'rel\s*=\s*["\']manifest["\']', html, re.IGNORECASE)

    # Accept href="manifest.json" OR href="/manifest.json" OR href="./manifest.json"
    assert re.search(
        r'href\s*=\s*["\'](\./)?/?manifest\.json["\']',
        html,
        re.IGNORECASE,
    )