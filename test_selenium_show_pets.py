import pytest
import time
from selenium import webdriver
from settings import valid_email, valid_password
from selenium.webdriver.common.by import By  # подключение библиотеки
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


# 1. Присутствуют все мои питомцы.
# Явные ожидания
def test_have_all_mypets(driver):
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)

    wait.until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице сайта.
    # Ожидаем в течение 10с, что на странице есть тег h1 с текстом "PetFriends"
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    print(f"\nВсего питомцев: {pets_number}")

    wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    assert int(pets_number) == len(pets_count)


# 2. Хотя бы у половины питомцев есть фото.
def test_mypets_have_photo(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # Сохраняем в переменную pets_number данные из статистики и получаем количество своих питомцев
    pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    print(f"\nВсего питомцев: {pets}")

    pets_number = int(pets)
    # Находим половину от количества питомцев
    half = pets_number // 2
    print(f'\nКоличество половины питомцев: {half}')

    # Сохраняем в переменную images_pet элементы с атрибутом img
    images_pet = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover img')

    number_photos = 0
    # Находим количество питомцев с фотографией
    for i in range(len(images_pet)):
        if images_pet[i].get_attribute('src') != '':
            number_photos += 1

    print(f'\nФото: {number_photos}')
    assert number_photos >= half


# 3. У всех питомцев есть имя, возраст и порода.
# НЕЯвные ожидания
def test_mypets_have_name_age_type(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # Сохраняем в переменные элементы с данными о питомцах
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(10)
    names = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover tbody tr td')
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(10)
    age = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover tbody tr td')
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(10)
    type_of_pet = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover tbody tr td')

    # Перебираем данные и сравниваем их с ожидаемым результатом
    for i in range(len(names)):
        assert names[i].text != ''
        assert age[i].text != ''
        assert type_of_pet[i].text != ''


# 4. У всех питомцев разные имена.
def test_mypets_different_name(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # Сохраняем в переменные элементы с данными о питомцах
    pet_data = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover tbody tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.Выбераем имена и добавляем их в список pets_name.
    names_my_pets = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        names_my_pets.append(split_data_pet[0])

    # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
    # Проверяем, если r == 0 то повторяющихся имен нет.
    r = 0
    for i in range(len(names_my_pets)):
        if names_my_pets.count(names_my_pets[i]) > 1:
            r += 1
    assert r == 0
    print(f'\nr: ')
    print(f'\nnames_my_pets: ')


# 5. В списке нет повторяющихся питомцев. (Сложное задание).
def test_mypets_not_repeat(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # Сохраняем в переменные элементы с данными о питомцах
    pet_data = driver.find_elements(By.CSS_SELECTOR, '.table.table.table-hover tbody tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0
