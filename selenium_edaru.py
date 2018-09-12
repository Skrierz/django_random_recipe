from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pprint import pprint
import json


class CategoryParser():
    def __init__(self, pages, url_base, browser, name):
        self.pages = pages
        self.url_base = url_base
        self.browser = browser
        self.name = name
        self.dishes = []

    def page_parser(self):
        for page in range(1, self.pages+1):
            page_url = self.url_base.format(page)
            dishes_on_page = recipes_parser(self.browser, page_url)
            for dish in dishes_on_page:
                self.dishes.append(dish)
            print('page {} of {} in {}'.format(page, self.pages, self.name))
        return self.dishes


def recipe_parser(recipe_page_source, url):
    title = portions = ''
    ingredients = {}
    instruction = []

    try:
        soup = BeautifulSoup(recipe_page_source, features='html.parser')
    except MemoryError as err:
        print(err)
        return None

    dish = {}

    title_soup = soup.find(class_='fn s-recipe-name')
    if title_soup is not None:
        title = title_soup.contents[0]
        title = title.replace('\xa0', ' ')

    portions_soup = soup.find(class_='selectBox-label')
    if portions_soup is not None:
        portions = portions_soup.contents[0].strip()

    ingredients_tab = soup.find(class_='b-ingredients-list').find('tbody')
    ingredients_soup = ingredients_tab.find_all(class_='ingredient')
    if ingredients_soup is not None:
        for ingredient in ingredients_soup:
            try:
                ingredient_name = ingredient.find('a').contents[0]
            except AttributeError as err:
                ingredient_name = ingredient.find('span').contents[0]
            ingredient_amount = ingredient.find(class_='amount').contents[0]
            ingredients[ingredient_name] = ingredient_amount

    recipe_tab = soup.find(class_='b-directions').find(class_='instructions')
    instruction_soup = recipe_tab.find_all(class_='text')
    if instruction_soup is not None:
        for action in instruction_soup:
            try:
                instruction.append(action.contents[2].strip())
            except IndexError as err:
                print(title)
                print(err)
                instruction.append(action.contents[0].strip())

    try:
        dish['url'] = url
        dish['title'] = title
        dish['portions'] = portions
        dish['ingredients'] = ingredients
        dish['instruction'] = instruction
    except UnboundLocalError as err:
        print(err)
        pprint(title_soup)
        pprint(portions_soup)
        pprint(ingredients_soup)
        pprint(instruction_soup)
    return dish


def recipes_parser(browser, recipes_page):
    browser.get(recipes_page)
    browser_recipes_page = browser.page_source
    soup = BeautifulSoup(browser_recipes_page, features='html.parser')
    class_name = 'b-recipe-widget__name-wrap'
    recipes_soup = soup.find_all(class_=class_name)
    urls_on_page = []
    dishes = []
    for recipe in recipes_soup:
        url = recipe.find('a')['href']
        urls_on_page.append(url)
    main_window = browser.current_window_handle
    for url in urls_on_page:
        full_url = 'https://eda.ru' + url
        browser.execute_script('window.open(arguments[0])', full_url)
        new_tab = browser.window_handles[1]
        browser.switch_to_window(new_tab)
        dish = recipe_parser(browser.page_source, browser.current_url)
        dishes.append(dish)
        browser.close()
        browser.switch_to_window(main_window)
    return dishes


def write_to_file(dishes, name):
    with open('{}.json'.format(name), 'w', encoding='utf8') as fp:
        json.dump(dishes, fp, ensure_ascii=False)
    print(name, ' done')


def main():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)

    url = 'https://eda.ru'

    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.get(url)

    old_site_button = browser.find_element_by_class_name('js-back-to-old')
    old_site_button.click()

    vypechka_url = 'https://eda.ru/recepty/vypechka-deserty/page{}'
    #     pages = 570
    vypechka = CategoryParser(570, vypechka_url, browser, 'vypechka')
    dishes_in_vypechka = vypechka.page_parser()
    write_to_file(dishes_in_vypechka, 'vypechka')

    osnovnie_bluda_url = 'https://eda.ru/recepty/osnovnye-blyuda/page{}'
    #     pages = 534
    osnovnie_bluda = CategoryParser(534, osnovnie_bluda_url, browser,
                                    'osnovnie_bluda')
    dishes_in_osnovnie_bluda = osnovnie_bluda.page_parser()
    write_to_file(dishes_in_osnovnie_bluda, 'osnovnie_bluda')

    pasta_pizza_url = 'https://eda.ru/recepty/pasta-picca/page{}'
    #     pages = 88
    pasta_pizza = CategoryParser(88, pasta_pizza_url, browser, 'pasta_pizza')
    dishes_in_pasta_pizza = pasta_pizza.page_parser()
    write_to_file(dishes_in_pasta_pizza, 'pasta_pizza')

    sendvichi_url = 'https://eda.ru/recepty/sendvichi/page{}'
    #     pages = 28
    sendvichi = CategoryParser(28, sendvichi_url, browser, 'sendvichi')
    dishes_in_sendvichi = sendvichi.page_parser()
    write_to_file(dishes_in_sendvichi, 'sendvichi')


if __name__ == '__main__':
    main()
