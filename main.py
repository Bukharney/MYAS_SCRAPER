from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import logging
import json
import os


load_dotenv(".env")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

with sync_playwright() as p:
    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=logging.INFO,
        datefmt="%d-%m-%y %H:%M:%S",
    )
    logging.info("Logging in...")
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(
        "https://login1.leb2.org/login?app_id=1&redirect_uri=https%3A%2F%2Fapp.leb2.org%2Flogin"
    )
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("load")
    soup = BeautifulSoup(page.inner_html("#classListMain"), "html.parser")

    logging.info("Getting classes...")
    class_list = []
    for div in soup.findAll("div", {"class": "class-card"}):
        class_list.append(div.attrs["name"][5:])

    logging.info("Getting assignments...")
    assignments_list = []
    for class_id in class_list:
        page.goto(f"https://app.leb2.org/class/{class_id}/activity")
        page.wait_for_load_state("load")
        class_name = (
            page.inner_text("p[name=code]") + " : " + page.inner_text("p[name=name_ln]")
        )
        soup = BeautifulSoup(page.inner_html("#table"), "html.parser")

        assignments = {
            "class_name": class_name,
            "assignments": [],
        }

        # find all the rows in the table
        for tr in soup.findAll("tr"):
            assignment = {}
            if tr.find("a"):
                assignment["name"] = tr.find(
                    "a", {"class": "assessment__title-link"}
                ).text
            if tr.find("td"):
                assignment["submission"] = tr.find(
                    "td", {"data-label": "Submissions"}
                ).text
                assignment["due_date"] = (
                    tr.find("td", {"data-label": "Due Date"})
                    .find("span")
                    .attrs["title"]
                )

            if assignment:
                assignments["assignments"].append(assignment)

        assignments_list.append(assignments)

    logging.info("Writing to file...")
    with open("assignments.json", "w") as f:
        f.write(json.dumps(assignments_list, indent=4, ensure_ascii=False))

    browser.close()

    logging.info("Done!")
