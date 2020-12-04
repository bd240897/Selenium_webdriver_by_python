import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    wait = WebDriverWait(driver, 10)
    return wd


def test_basket(driver):
    # driver = webdriver.Chrome();
    # driver.get("http://localhost/litecart/admin/")
    # driver.find_element_by_name("username").send_keys("admin")
    # driver.find_element_by_name("password").send_keys("admin")
    # driver.find_element_by_name("login").click()

    for i in range(3) :
        # передйем на сайт магазина
        driver.get("https://litecart.stqa.ru/en/")

        # получим ссылку на счетчик
        numb_item = driver.find_element_by_css_selector("span.quantity")
        counter = numb_item.get_attribute("innerTex")
        print("sagalgjjasfahsfa", counter)

        # откроем первый продукт
        first_product = driver.find_element_by_css_selector("div#box-most-popular ul.listing-wrapper.products li:nth-child(1)")
        first_product.click()

        # смотрим названеи продукта
        w_title = driver.find_element_by_css_selector("h1")
        title = w_title.get_attribute("outerText")

        # // если он желтая утка
        if title == "Yellow Duck":
            yellow_duck = driver.find_element_by_css_selector("select")
            select = Select(yellow_duck)
            select.select_by_value("Small")
            # кликнем на кропку добавить
            add_to_cart = driver.find_element_by_css_selector("button[name=add_cart_product]")
            add_to_cart.click();
        else :
            # кликнем на кропку добавить
            add_to_cart = driver.find_element_by_css_selector("button[name=add_cart_product]")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=add_cart_product]")))
            add_to_cart.click();

        # дождемся обновление счетчика
        wait = WebDriverWait(driver, 10)
        wait.until(lambda s: s.find_element_by_css_selector("span.quantity").text == str(i+1))

    # передйем в корзину
    check_out = driver.find_element_by_css_selector("div#cart-wrapper a.link")
    href = check_out.get_attribute("href")
    driver.get(href)


    # длина карусели для удаления
    shortcuts  = driver.find_elements_by_css_selector("ul.shortcuts li a")
    print('asdasfas', shortcuts)
    # пробежимя по товарам и удалим их

    for i in range(len(shortcuts)) :

        # находим таблицу товаров
        wait = WebDriverWait(driver,10)
        # w_table = driver.find_element_by_css_selector("table.dataTable.rounded-corners")
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.dataTable.rounded-corners")))


        shortcuts_current = driver.find_elements_by_css_selector("li.shortcut")
        #  кликнем на маленькую иконку корусели
        if len(shortcuts_current) > 0 :
            shortcuts_current[0].click()


        # нажмем на кнопку удалить
        remove = driver.find_element_by_css_selector("button[name=remove_cart_item]")
        remove.click()

        # дождемся удаления
        wait.until(EC.staleness_of(table))




