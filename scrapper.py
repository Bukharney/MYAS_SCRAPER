from playwright.async_api import async_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup


async def scrape_assignments(username: str, password: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(
            "https://login1.leb2.org/login?app_id=1&redirect_uri=https%3A%2F%2Fapp.leb2.org%2Flogin"
        )
        await page.fill('input[name="username"]', username)
        await page.fill('input[name="password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("load")
        soup = BeautifulSoup(await page.inner_html("#classListMain"), "html.parser")

        class_list = []
        for div in soup.findAll("div", {"class": "class-card"}):
            class_list.append(div.attrs["name"][5:])
        assignments_list = []

        for class_id in class_list:
            await page.goto(f"https://app.leb2.org/class/{class_id}/activity")
            await page.wait_for_load_state("load")
            class_name = (
                await page.inner_text("p[name=code]")
                + " : "
                + await page.inner_text("p[name=name_ln]")
            )
            soup = BeautifulSoup(await page.inner_html("#table"), "html.parser")

            assignments = {
                "class_name": class_name,
                "assignments": [],
            }

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

        await browser.close()

    return assignments_list
