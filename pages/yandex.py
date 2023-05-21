import os

from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or 'https://ya.ru/'

        super().__init__(web_driver, url)

    search = WebElement(css_selector= 'input[class*=search3__input]')

    search_suggestions= ManyWebElements(css_selector= 'li[class*=mini-suggest__item]')

    search_run_button = WebElement(css_selector='button[class*=search3__button]')

    search_links = ManyWebElements(css_selector='a[class*=OrganicTitle-Link ]')

    search_item_more= WebElement(css_selector='a[class*=services-suggest__item-more ]')

    images=WebElement(xpath='//a[@aria-label="Картинки"]')

class ImagesPage(MainPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("Images_URL") or 'https://yandex.ru/images/'
        super().__init__(web_driver, url)

    catalog = ManyWebElements(css_selector='div[class*= PopularRequestList-SearchText]')

    search = WebElement(css_selector='input[class*= input__control ]')

    imgs= ManyWebElements(css_selector='img[class*= serp-item__thumb]')

    opened_img= WebElement(css_selector='img[class*= MMImage-Preview]')

    next_button= WebElement(css_selector='div[class*= CircleButton_type_next ]')

    previous_button=WebElement(css_selector='div[class*= CircleButton_type_prev ]')

    advertisment=WebElement(css_selector='div[class*= yac492ba1  ]')