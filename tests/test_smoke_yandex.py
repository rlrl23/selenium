import pytest
from pages.yandex import MainPage, ImagesPage
from selenium import webdriver

def test_check_main_search(web_browser):
    """ Make sure main search works fine. """

    page = MainPage(web_browser)

    # Проверить наличие поля поиска
    assert page.search.is_presented()

    page.search = 'Тензор'

    # Проверить, что появилась таблица с подсказками (suggest)
    assert page.search_suggestions.is_visible()

    page.search.press_enter()

    # Проверить, что появилась страница результатов поиска
    assert page.search_links.is_visible()

    first_link= page.search_links.get_attribute_first('href')

    # Проверить 1 ссылка ведет на сайт tensor.ru
    assert first_link == 'https://tensor.ru/'

    page.tear_down()

def test_check_images(web_browser):
    """ Make sure that images works fine. """

    page = MainPage(web_browser)

    # Проверить, что кнопка меню присутствует на странице
    assert page.images.is_presented()

    page.search.click()
    page.search_item_more.click()
    new_page=ImagesPage(web_driver=webdriver.Chrome(), url=page.images.get_attribute('href'))

    # Проверить, что перешли на url https://yandex.ru/images/
    assert new_page.get_current_url()=='https://yandex.ru/images/'

    page.tear_down()

    new_page.catalog.click_first()

    # Проверить, что название категории отображается в поле поиска
    assert new_page.search.get_attribute('value')==new_page.catalog.get_text_first_element()

    new_page.imgs.click_first()

    # Проверить, что картинка открылась
    assert new_page.opened_img.is_visible()

    first_img_screen='tests/screenshots/image.jpg'
    new_page.opened_img.element_screenshot(first_img_screen)

    # Убрать всплывающую рекламу
    # new_page.advertisment.delete()

    new_page.next_button.click()

    # Проверить, что картинка сменилась
    assert not new_page.opened_img.compare_with(first_img_screen)

    new_page.previous_button.click()

    # Проверить, что картинка осталась из шага 8
    assert new_page.opened_img.compare_with(first_img_screen)

    new_page.tear_down()