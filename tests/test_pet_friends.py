from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


# тест-кейс 1
def test_add_new_pet_without_photo_with_valid_data(name='Боба', animal_type='пупур',
                                     age='5'):
    """Проверяем что можно добавить питомца с корректными данными и без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# тест-кейс 2
def test_successful_add_pet_photo(pet_photo='images/Boba.jpg'):
    """Проверяем возможность добавления фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и фото питомца существует
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#тест-кейс 3
def test_add_new_pet_with_incorrect_age(name='Пупа', animal_type='Гусеница',
                                     age='-1000000000000', pet_photo='images/Pupa.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Данные некорректны, значит статус код должен быть 400
    assert status == 400


#тест-кейс 4
def test_add_new_pet_with_incorrect_name(name='', animal_type='бука',
                                     age='1', pet_photo='images/Pupa.jpg'):
    """Проверяем что нельзя добавить питомца с пустым полем Name"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Данные некорректны, значит статус код должен быть 400
    assert status == 400

#тест-кейс 5
def test_add_new_pet_with_incorrect_data(name='', animal_type='',
                                     age=''):
    """Проверяем что нельзя добавить питомца с пустыми полями и без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом. Данные некорректны, значит статус код должен быть 400
    assert status == 400


#тест-кейс 6
def test_second_add_new_pet_with_incorrect_age(name='Лупа', animal_type='Гусеница',
                                     age='Буковки', pet_photo='images/Pupa.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным возрастом, состоящим из буквенных симоволов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Данные некорректны, значит статус код должен быть 400
    assert status == 400


# тест-кейс 7
def test_successful_delete_first_pet():
    """Проверяем возможность удаления первого добавленного питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Biba.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого добавленного питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][len(my_pets['pets'])-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# тест-кейс 8
def test_update_incorrect_pet_info(name='Биба', animal_type='"№;%:?*"', age=5):
    """Проверяем невозможность обновления некорректной (недопустимые символы) информации о породе питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'],name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
        assert result['animal_type'] == animal_type
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# тест-кейс 9
def test_add_new_pet_with_incorrect_age_2(name='Пупа', animal_type='Гусеница',
                                     age='вот тут не должно быть так', pet_photo='images/Pupa.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом. Данные некорректны, значит статус код должен быть 400
    assert status == 400

# тест-кейс 10
def test_get_api_key_for_invalid_user(email = 'valid_email', password = ''):
    '''Проверяем, что запрос API возвращает статус 403 и в резулультате не содержится key, т.к. данные недействительны'''

    # Отправка запроса и присвоение ответа с статусом в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    print('РЕЗУЛЬТАТ', result)

    # Сверяем с ожидаемым результатом
    assert status == 403
    assert 'key' not in result