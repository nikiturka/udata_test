import re
from bs4 import BeautifulSoup
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import session_factory
from src.db.models import Item
from playwright.async_api import async_playwright


class ScraperService:
    DOMAIN = "https://www.mcdonalds.com"
    BASE_URL = "https://www.mcdonalds.com/ua/uk-ua"

    @staticmethod
    async def setup_playwright():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        return playwright, browser

    @staticmethod
    async def get_product_links(menu_url: str) -> List[str]:
        playwright, browser = await ScraperService.setup_playwright()
        page = await browser.new_page()
        await page.goto(menu_url)

        await page.wait_for_selector('li.cmp-category__item')

        product_items = await page.query_selector_all('li.cmp-category__item')
        product_links = []

        for item in product_items:
            link_tag = await item.query_selector('a.cmp-category__item-link')
            if link_tag:
                href = await link_tag.get_attribute('href')
                if href:
                    if not href.startswith('http'):
                        href = ScraperService.DOMAIN + href
                    product_links.append(href)

        await browser.close()
        await playwright.stop()
        return product_links

    @staticmethod
    async def get_product_details(product_url: str) -> Dict[str, str]:
        playwright, browser = await ScraperService.setup_playwright()
        page = await browser.new_page()
        await page.goto(product_url)

        # Wait until element opens
        try:
            await page.click('#accordion-29309a7a60-item-9ea8a10642-button')
            await page.wait_for_selector('#accordion-29309a7a60-item-9ea8a10642-panel', state='visible')
        except Exception as e:
            print(f"Error opening content: {e}")

        page_source = await page.content()
        soup = BeautifulSoup(page_source, 'html.parser')

        # Get product name
        name_tag = soup.find('span', class_='cmp-product-details-main__heading-title')
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"

        # ИGet product description
        description_tag = soup.find('div', class_='cmp-product-details-main__description')
        description = description_tag.get_text(strip=True) if description_tag else "No description available"

        # Product dict
        nutrition_info = {}

        # Main metrics
        primary_nutrition_items = soup.select('.cmp-nutrition-summary__heading-primary-item')
        for item in primary_nutrition_items:
            metric = item.select_one('.metric')
            value = item.select_one('.value')

            if metric and value:
                metric_text = metric.get_text(strip=True)
                value_text = value.get_text(strip=True)
                nutrition_info[metric_text] = value_text

        # Secondary metrics
        secondary_nutrition_items = soup.select('.cmp-nutrition-summary__details-column-view-mobile .label-item')
        for item in secondary_nutrition_items:
            metric = item.select_one('.metric')
            value = item.select_one('.value')

            if metric and value:
                metric_text = metric.get_text(strip=True)
                value_text = value.get_text(strip=True)
                nutrition_info[metric_text] = value_text

        await browser.close()
        await playwright.stop()

        return {
            'name': name,
            'description': description,
            'url': product_url,
            'nutrition': nutrition_info
        }

    @staticmethod
    def refactor_nutrition(nutrition):
        pattern = re.compile(r'(\d+)\s?(ккал|г|kcal|g)')

        refactored_nutrition = {}

        for key, value in nutrition.items():
            match = pattern.search(value)
            if match:
                number = match.group(1)
                refactored_nutrition[key.split('\n')[0].strip()] = f"{number} {match.group(2)}"

        return refactored_nutrition

    @staticmethod
    async def save_item_to_db(item_dict: dict):
        try:
            with session_factory() as session:
                existing_item = session.query(Item).filter(Item.name == item_dict['name']).first()

                if existing_item:
                    print(f"Item already exists: {existing_item.name}, skipping.")
                    return

                item = Item(
                    name=item_dict['name'],
                    description=item_dict['description'],
                    calories=item_dict['nutrition'].get('Калорійність', '0 ккал'),
                    fats=item_dict['nutrition'].get('Жири', '0 г'),
                    carbs=item_dict['nutrition'].get('Вуглеводи', '0 г'),
                    proteins=item_dict['nutrition'].get('Білки', '0 г'),
                    unsaturated_fats=item_dict['nutrition'].get('НЖК:', '0 г'),
                    sugar=item_dict['nutrition'].get('Цукор:', '0 г'),
                    salt=item_dict['nutrition'].get('Сіль:', '0 г'),
                    portion=item_dict['nutrition'].get('Порція:', '0 г')
                )

                session.add(item)
                session.commit()

            print(f"Item saved: {item}")

        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    async def main():
        menu_url = f"{ScraperService.BASE_URL}/eat/fullmenu.html"
        product_links = await ScraperService.get_product_links(menu_url)

        for link in product_links:
            product_details = await ScraperService.get_product_details(link)
            product_details['nutrition'] = ScraperService.refactor_nutrition(product_details['nutrition'])

            await ScraperService.save_item_to_db(product_details)
