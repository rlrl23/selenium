#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time

import allure
from termcolor import colored

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageChops
from utils import compare_pixels


class WebElement(object):

    _locator = ('', '')
    _web_driver = None
    _page = None
    _timeout = 10
    _wait_after_click = False

    def __init__(self, timeout=10, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click

        for attr in kwargs:
            self._locator = (str(attr).replace('_', ' '), str(kwargs.get(attr)))

    def find(self, timeout=10):
        """ Find element on the page. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
               EC.presence_of_element_located(self._locator)
            )
        except:
            print(colored('Element not found on the page!', 'red'))

        return element

    def wait_to_be_clickable(self, timeout=10, check_visibility=True):
        """ Wait until the element will be ready for click. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.element_to_be_clickable(self._locator)
            )
        except:
            print(colored('Element not clickable!', 'red'))

        if check_visibility:
            self.wait_until_not_visible()

        return element

    def is_clickable(self):
        """ Check is element ready for click or not. """

        element = self.wait_to_be_clickable(timeout=0.1)
        return element is not None

    def is_presented(self):
        """ Check that element is presented on the page. """

        element = self.find(timeout=0.1)
        return element is not None

    def is_visible(self):
        """ Check is the element visible or not. """

        element = self.find(timeout=0.1)

        if element:
            return element.is_displayed()

        return False

    def wait_until_not_visible(self, timeout=10):
        """ Wait until the element will be visible """
        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.visibility_of_element_located(self._locator)
            )
        except:
            print(colored('Element not visible!', 'red'))

        if element:
            js = ('return (!(arguments[0].offsetParent === null) && '
                  '!(window.getComputedStyle(arguments[0]) === "none") &&'
                  'arguments[0].offsetWidth > 0 && arguments[0].offsetHeight > 0'
                  ');')
            visibility = self._web_driver.execute_script(js, element)
            iteration = 0

            while not visibility and iteration < 10:
                time.sleep(0.5)

                iteration += 1

                visibility = self._web_driver.execute_script(js, element)
                print('Element {0} visibility: {1}'.format(self._locator, visibility))

        return element

    def press_enter(self):
        """ Press enter. """
        element = self.find()

        if element:
            element.send_keys(Keys.ENTER)
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def send_keys(self, keys, wait=2):
        """ Send keys to the element. """

        keys = keys.replace('\n', '\ue007')

        element = self.find()

        if element:
            element.click()
            element.clear()
            element.send_keys(keys)
            time.sleep(wait)
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def get_text(self):
        """ Get text of the element. """

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as e:
            print('Error: {0}'.format(e))

        return text

    def get_attribute(self, attr_name):
        """ Get attribute of the element. """

        element = self.find()

        if element:
            return element.get_attribute(attr_name)

    def _set_value(self, web_driver, value, clear=True):
        """ Set value to the input element. """

        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def navigate_to_elem(self, hold_seconds=0, x_offset=1, y_offset=1):
        """ Navigate cursor to the element. """

        element=self.find()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds)
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def click(self, hold_seconds=0, x_offset=1, y_offset=1):
        """ Wait and click the element. """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset).\
                pause(hold_seconds).click(on_element=element).perform()
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

        if self._wait_after_click:
            self._page.wait_page_loaded()

    def right_mouse_click(self, x_offset=0, y_offset=0, hold_seconds=0):
        """ Click right mouse button on the element. """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).context_click(on_element=element).perform()
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight element and make the screen-shot of all page. """

        element = self.find()

        # Scroll page to the element:
        self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Add red border to the style:
        self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Make screen-shot of the page:
        self._web_driver.save_screenshot(file_name)

    def scroll_to_element(self):
        """ Scroll page to the element. """

        element = self.find()

        # Scroll page to the element:
        # Option #1 to scroll to element:
        # self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Option #2 to scroll to element:
        try:
            element.send_keys(Keys.DOWN)
        except Exception as e:
            pass  # Just ignore the error if we can't send the keys to the element

    def delete(self):
        """ Deletes element from the page. """

        element = self.find()

        # Delete element:
        self._web_driver.execute_script("arguments[0].remove();", element)

    def element_screenshot(self, file_name='element.jpg'):
        """ Make screenshot of element """

        # Make screen-shot of the page:
        self._page.wait_page_loaded()
        self._web_driver.save_screenshot(file_name)

        # Создаем экземпляр Image для работы с изображением
        img= Image.open(file_name).convert('RGB')
        element_img=img.crop((129, 25, 545, 650))
        #Cохраняем локально
        element_img.save(file_name)
        # Cохраняем в report
        allure.attach(self._web_driver.get_screenshot_as_png(),
                      name=file_name,
                      attachment_type=allure.attachment_type.PNG)

    def compare_with(self, file_name):
        """ Compare two images """

        new_file='tests/screenshots/new.jpg'
        self.element_screenshot(new_file)
        image_1 = Image.open(file_name)
        image_2 = Image.open(new_file)
        return compare_pixels(image_1, image_2)

        # # Работает некорректно
        # difference = ImageChops.difference(image_1, image_2).getbbox()
        # if difference == None:
        #     return True
        # else:
        #     return False


class ManyWebElements(WebElement):

    def __getitem__(self, item):
        """ Get list of elements and try to return required element. """

        elements = self.find()
        return elements[item]

    def find(self, timeout=10):
        """ Find elements on the page. """

        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
               EC.presence_of_all_elements_located(self._locator)
            )
        except:
            print(colored('Elements not found on the page!', 'red'))

        return elements

    def _set_value(self, web_driver, value):
        """ Note: this action is not applicable for the list of elements. """

        raise NotImplemented('This action is not applicable for the list of elements')

    def click_first(self, hold_seconds=0, x_offset=0, y_offset=0):
        """ Note: this action is applicable for the first element. """

        elements = self.find()
        if elements:
            for element in elements:
                element = self.wait_to_be_clickable()
                action = ActionChains(self._web_driver)
                action.move_to_element_with_offset(element, x_offset, y_offset). \
                    pause(hold_seconds).click(on_element=element).perform()
                break
        else:
            msg = 'Elements with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

            if self._wait_after_click:
                self._page.wait_page_loaded()

    def is_visible(self):
        """ Check is the element visible or not. """

        elements = self.find()
        result=True

        if elements:
            for element in elements:
                result*= element.is_displayed()

        return result

    def count(self):
        """ Get count of elements. """

        elements = self.find()
        return len(elements)

    def get_text(self):
        """ Get text of elements. """

        elements = self.find()
        result = []

        for element in elements:
            text = ''

            try:
                text = str(element.text)
            except Exception as e:
                print('Error: {0}'.format(e))

            result.append(text)

        return result

    def get_text_first_element(self):
        """ Get text of first element. """

        elements = self.find()

        for element in elements:
            try:
                text = str(element.text)
                return text
            except Exception as e:
                print('Error: {0}'.format(e))

    def get_attribute(self, attr_name):
        """ Get attribute of all elements. """

        results = []
        elements = self.find()

        for element in elements:
            results.append(element.get_attribute(attr_name))

        return results

    def get_attribute_first(self, attr_name):
        """ Get attribute of all elements. """

        elements = self.find()

        for element in elements:
            # element=self.wait_until_not_visible()
            return element.get_attribute(attr_name)

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight elements and make the screen-shot of all page. """

        elements = self.find()

        for element in elements:
            # Scroll page to the element:
            self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

            # Add red border to the style:
            self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Make screen-shot of the page:
        self._web_driver.save_screenshot(file_name)
