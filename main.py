from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# get env variable
from dotenv import load_dotenv
import os

load_dotenv(".env")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "https://login1.leb2.org/login?app_id=1&redirect_uri=https%3A%2F%2Fapp.leb2.org%2Flogin"
    )
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("load")
    soup = BeautifulSoup(page.inner_html("#classListMain"), "html.parser")

    class_list = []
    # get name arrtibute in div tag
    for div in soup.findAll("div", {"class": "class-card"}):
        # card-511287 cut card- and get the number
        class_list.append(div.attrs["name"][5:])

    assignments_list = []
    for class_id in class_list:
        page.goto(f"https://app.leb2.org/class/{class_id}/activity")
        page.wait_for_load_state("load")
        # get text in p tag arrtibute name=code
        class_name = page.inner_text("p[name=code]")
        soup = BeautifulSoup(page.inner_html("#table"), "html.parser")
        # get span tag in td tag with attribute data-label=Submissions

        assignments = {
            "class_name": class_name,
            "assignments": [],
        }

        for tr in soup.findAll("tr"):
            assignment = {}
            if tr.find("a", {"class": "assessment__title-link"}):
                name = tr.find("a", {"class": "assessment__title-link"}).text
                assignment["name"] = name
            if tr.find("td", {"data-label": "Submissions"}):
                assignment["submission"] = tr.find(
                    "td", {"data-label": "Submissions"}
                ).text
            if tr.find("td", {"data-label": "Due Date"}):
                # get text in td tag
                td = tr.find("td", {"data-label": "Due Date"})
                span = td.find("span")
                assignment["due_date"] = span.attrs["title"]
            if assignment:
                assignments["assignments"].append(assignment)

        assignments_list.append(assignments)

    print(assignments_list)

    # write to json file
    import json

    with open("assignments.json", "w") as f:
        # make it pretty
        # uft-8 for thai language
        f.write(json.dumps(assignments_list, indent=4, ensure_ascii=False))

    browser.close()
