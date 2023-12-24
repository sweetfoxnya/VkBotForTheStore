from threading import Thread
import requests
import vk_api

import phonenumbers
import os.path
from vk_api.keyboard import VkKeyboard

from DBHelper import DBHelper, convertToBinaryData, writeTofile, checkUser
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date

from keyboards import get_start, get_anketa, get_home, get_basket, get_katalog, get_order, get_back_anketa, get_pay, \
    get_making, get_chat, get_list, get_product, get_name, get_start_for_admin, get_list_search, get_name_for_search, \
    get_name_vkid, get_name_change, get_name_list_basket, get_list_order, get_order_all, get_order_all_list, home

vk_session = vk_api.VkApi(
    token="vk1.a.UtRaqh6hUBK2pHpcErYc-W4DVIzSrpquWdel63eSOl6lhhZlFyz2xOq2-9CZHG_FPu1h0TQxf5YdaJ0Gf8ZS90LKtV-ofDmXyGrVlsDY-W2uDEOAhrjnIRmTl-qDFkAxti3xLiYhkkPauRHqUPl5ZZ11m1IgcagujPAzDxZUgsa1KCWpYxOwbCnjUjhUqQt9cDrPAeh7ujFPMwmeos3OHw")

longpool = VkLongPoll(vk_session)
vk = vk_session.get_api()
helper = DBHelper()
commands_for_start = ['Каталог 🗂', 'Корзина 🛒', 'Заказы 📋', 'Акции 💯', 'Анкета 📝', 'Помощь 🙏', 'О нас 🏪']
commands_for_anketa = ['Имя 👩👨', 'Телефон 📞', 'Город 🏤', 'Адрес 🏨']
commands_for_making = ['Самовывоз 🚹', 'Доставка 🚕']
commands_for_pay = ['Наличными при получении 💵', 'Переводом на карту 💳']
commands_for_change = ['Удалить товар 💥', 'Добавить товар 👍']

user_template = [[], "", 0]

users = {}

def send_keyboard(userid, some_text, keyboard):
    vk_session.method("messages.send", {"user_id": userid, "message": some_text, "random_id": get_random_id(),
                                        'keyboard': keyboard.get_keyboard()})


def send_message(userid, some_text):
    vk_session.method("messages.send", {"user_id": userid, "message": some_text, "random_id": get_random_id()})


def handle_message_start(userid, message):
    if message == commands_for_start[0]:
        send_message(userid, "Каталог:")
        user = users.get(userid)
        user[2] = 0
        users.update({userid: user})
        key = get_list(user[2])
        write_card(userid, user[2])
        send_keyboard(userid, "Выберите товар для добавления в корзину", key)
    elif message == commands_for_start[1]:
        key = get_basket(userid)
        send_message(userid, "Ваша текущая корзина:")
        write_card_basket(userid)
        send_keyboard(userid, "Выберите что делать", key)
    elif message == commands_for_start[2]:
        key = get_order(userid)
        send_message(userid, "Ваши заказы:")
        write_card_order(userid)
        send_keyboard(userid, "Нажмите чтобы детально просмотреть заказ", key)
    elif message == commands_for_start[3]:
        key = get_start()
        send_message(userid, get_sale())
        send_keyboard(userid, "Действующая акция:", key)
    elif message == commands_for_start[4]:
        key = get_anketa()
        send_keyboard(userid, "Ваша анкета:", key)
    elif message == commands_for_start[5]:
        key = get_chat()
        send_keyboard(userid, "Данные для связи с менеджером", key)
        send_message(userid, "Номер телефона:89995833622 \n\tViber: 89995833622 \n\tTelegram: 89995833622 \n\tПочта: "
                             "xamidullina.vika@mail.ru \n\tСтраница в вк: https://vk.com/sellstolen\n\t Если хотите "
                             "дождаться оператора, нажмите 'оператор', если у вас срочный вопрос, можете перейти в "
                             "чат с"
                             " менеджером и написать напрямую")
    elif message == commands_for_start[6]:
        key = get_home()
        send_keyboard(userid, "Информация о магазине", key)
        send_message(userid, "Адрес: Южноуральск, ул. Пирогова 75\n\tРуководитель и менеджер: Хамидуллина Виктория "
                             "Эдуардовна\n\tДата открытия: 15.08.2022\n\tКак найти: Большой гаражный бокс с желтой "
                             "вывеской 'Активный отдых'.\n\tОписание: Только качественные и проверенные товары для "
                             "готовки на огне🔥"
                             "Отправляем ✈ по России \n\tВ нашем магазине вы найдете:\n\t ✅ Чугунные казаны из "
                             "Узбекистана"
                             "и печи к ним, треноги.\n\t ✅ Афганские казаны Рашко Баба.\n\t ✅ Качественные мангалы и "
                             "печи.\n\t ✅"
                             "Узбекские пчаки.\n\t ✅ Керамическую посуду, саджи (чугунные и стальные), подставки к "
                             "ним.\n\t ✅"
                             "Шампуры поштучно и в подарочных наборах.\n\t ✅ Аксессуары для готовки дома и на природе: "
                             "шумовки, половники, щипцы, камни для выпечки, вилки - ножи")


def handle_message_anketa(userid, message):
    if message == commands_for_anketa[0]:
        key = get_back_anketa()
        send_keyboard(userid, "Введите ваше имя:", key)

        new_msg = New_message(userid)

        handle_name(userid, new_msg)

    elif message == commands_for_anketa[1]:
        key = get_back_anketa()
        send_keyboard(userid, "Введите ваш телефон:", key)

        phone = New_message(userid)

        handle_phone(userid, phone)

    elif message == commands_for_anketa[2]:
        key = get_back_anketa()
        send_keyboard(userid, "Введите ваш город'", key)

        city = New_message(userid)

        handle_city(userid, city)
    elif message == commands_for_anketa[3]:
        key = get_back_anketa()
        send_keyboard(userid, "Введите ваш адрес:", key)

        address = New_message(userid)

        handle_address(userid, address)


def handle_name(userid, name):
    helper.update('user', 'id', user_id, 'name', name)
    key = get_anketa()
    send_keyboard(userid, f"Ваше имя '{name}' сохранено!", key)


def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "RU")
        is_valid = phonenumbers.is_valid_number(parsed_number)
        return is_valid
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def handle_phone(userid, phone):
    if phone == 'Назад ⬅':
        handle_message_back(userid, phone)
    elif validate_phone_number(phone):
        helper.update('user', 'id', user_id, 'phone', phone)
        key = get_anketa()
        send_keyboard(userid, f"Ваш телефон '{phone}' сохранен!", key)
        # Сохранение имени в базу данных
        # save_name(userid, phone)
    else:
        key = get_anketa()
        send_keyboard(userid, "Некорректный номер телефона. Пожалуйста, введите номер в правильном формате. 😕", key)


def check_city(city):
    api_key = "0c4d541d-3452-4b46-b30a-63c4aaeda180"
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={city}"

    response = requests.get(url)
    data = response.json()

    try:
        # Получить статус ответа
        response_code = int(
            data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"])

        # Если найдено хотя бы одно совпадение, город существует
        if response_code > 0:
            return True
        else:
            return False
    except KeyError:
        # Если произошла ошибка при обработке ответа, считаем ввод некорректным
        return False


def handle_city(userid, city):
    if city == 'Назад ⬅':
        handle_message_back(userid, city)
    elif check_city(city):
        helper.update('user', 'id', user_id, 'town', city)
        # Сохранение имени в базу данных
        # save_name(userid, city)
        key = get_anketa()
        send_keyboard(userid, f"Ваш город'{city}' сохранен!", key)
    else:
        key = get_anketa()
        send_keyboard(userid, "Город не найден или не принадлежит России.", key)


def check_address(address):
    # Замените "your_api_key" на ваш ключ API геокодирования Яндекса
    api_key = "ec8e7d47-3fe3-42a4-a1de-c4f01f6f8f08"
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={address}"

    response = requests.get(url)
    data = response.json()

    try:
        # Получить статус ответа и преобразовать в целое число
        response_code = int(
            data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"])

        # Если найдено хотя бы одно совпадение, адрес существует
        if response_code > 0:
            return True
        else:
            return False
    except KeyError:
        # Если произошла ошибка при обработке ответа, считаем ввод некорректным
        return False


def handle_address(userid, address):
    if address == 'Назад ⬅':
        handle_message_back(userid, address)
    elif check_address(address):
        # Сохранение имени в базу данных
        # save_name(userid, address)
        key = get_anketa()
        send_keyboard(userid, f"Ваш адрес'{address}' сохранен!", key)
    else:
        key = get_anketa()
        send_keyboard(userid, "Некорректный адрес!", key)


def handle_find(userid, message):
    if message == "Поиск 🔎":
        key = get_order()
        send_keyboard(userid, "Введите наименование товара для поиска", key)

        new_msg = New_message(userid)

        handle_product(userid, new_msg)


def get_sale():
    sales = helper.print_info('promotion')
    sale = sales[0][1]
    return sale

def handle_product(userid, product):
    product_names = helper.print_info('product')

    matching_products = [prod for prod in product_names if product.lower() in prod[1].lower()]
    matching_name = []
    index = 0

    key = VkKeyboard(one_time=True)
    if matching_products:
        key = get_list_search(product)
        for prod in matching_products:
            message, attachment = create_product_card(prod)
            vk.messages.send(
                random_id=vk_api.utils.get_random_id(),
                peer_id=userid,
                message=message,
                attachment=attachment
            )

        send_keyboard(userid, f"Результат поиска", key)
    else:
        key = get_order()
        send_keyboard(userid, "Товар не найден. Попробуйте ввести другое наименование или вернуться на главную.", key)
        new_msg = New_message(userid)
        handle_product(userid, new_msg)


def handle_products(userid, message):
    product_names = get_name_for_search()
    if message in product_names:
        basket = helper.get('basket', ['user_id'], [str(userid)])
        prod = helper.get('product', ['name'], [clean_message(message)])
        helper.insert('basket_products', ['basket_id', 'product_id', 'num'], [basket[0][0], prod[0][0], 1])

        key = get_product()
        send_keyboard(userid, f"Выбранный вами товар '{message}'. Он отправился в корзину", key)

def clean_message(mess):
    words = mess.split()
    words.pop(-1)
    word = " ".join(words)
    return word

def handle_change_basket(userid, message):
    product_names = get_name_list_basket(userid)
    if message in product_names:
        user = users.get(userid)
        user[1] = clean_message(message)
        users.update({userid: user})
        key = get_name_change()
        send_keyboard(userid, f"Выберите что делать с товаром", key)


def handle_change_basket_prod(userid, message):
    if message == commands_for_change[0]:
        user = users.get(userid)
        basket = helper.get('basket', ['user_id'], [str(userid)])
        prod_id = helper.get('product', ['name'], [user[1]])
        real = helper.get('basket_products', ['basket_id', 'product_id'], [str(basket[0][0]), str(prod_id[0][0])])
        helper.delete('basket_products', 'id', real[0][0])
        key = get_basket(userid)
        send_keyboard(userid, "Корзина изменена", key)
    elif message == commands_for_change[1]:
        user = users.get(userid)
        basket = helper.get('basket', ['user_id'], [str(userid)])
        prod_id = helper.get('product', ['name'], [user[1]])
        real = helper.get('basket_products', ['basket_id', 'product_id'], [str(basket[0][0]), str(prod_id[0][0])])
        num = real[0][3] + 1
        helper.update('basket_products', 'id', str(real[0][0]), 'num', num)
        key = get_basket(userid)
        send_keyboard(userid, "Корзина изменена", key)

def handle_message_making(userid, message):
    if message in commands_for_making:
        user = users.get(userid)
        user[0].clear()
        user[0].append(clean_message(message))
        users.update({userid: user})
        key = get_pay()
        send_keyboard(userid, "Выберите способ оплаты:", key)



def handle_message_operator(userid, message):
    if message == "Оператор 📞":
        key = get_home()
        send_keyboard(userid, "Оператор скоро подойдёт к вам", key)


def handle_message_back(userid, message):
    if message == "Назад ⬅":
        key = get_anketa()
        send_keyboard(userid, "Ваша анкета:", key)


def handle_message_order(userid, message):
    if message == "Оформить заказ 📦":
        key = get_making()
        send_keyboard(user_id, "Выбери способ доставки:", key)


def handle_message_pay(userid, message):
    if message in commands_for_pay:
        key = get_start()
        user = users.get(userid)
        user[0].append(clean_message(message))
        users.update({userid: user})
        basket = helper.get('basket', ['user_id'], [str(userid)])
        basket_prod = helper.get('basket_products', ['basket_id'], [str(basket[0][0])])
        products_ = []
        for prod_id in basket_prod:
            new_prod = helper.get('product', ['id'], [str(prod_id[2])])
            products_.append([new_prod[0], prod_id[3]])
        helper.delete('basket_products', 'basket_id', str(basket[0][0]))
        helper.insert('package', ['user_id', 'status', 'date', 'payment', 'delivery'], [userid, 'Ожидайте ответа', date.today(), user[0][1], user[0][0]])
        package = helper.get('package', ['user_id'], [str(userid)])
        for product in products_:
            helper.insert('package_products', ['package_id', 'product_id', 'num'], [str(package[-1][0]), str(product[0][0]), product[1]])
        send_keyboard(userid, "Ваш заказ оформлен, ожидайте сообщения/звонка от оператора", key)


def handle_for_admin(userid, message):
    if message == "код":
        key = get_start_for_admin()
        send_keyboard(userid, "Выберите команду:", key)


def handle_for_order(userid, message):
    orders_id = get_list_order(userid)
    if message in orders_id:
        package = helper.get('package_products', ['package_id'], [clean_message(message)])
        for prods in package:
            new_prod = helper.get('product', ['id'], [str(prods[2])])
            message, attachment = create_product_card(new_prod[0])
            send_message(userid, f"Количество: {prods[3]}")
            vk.messages.send(
                random_id=vk_api.utils.get_random_id(),
                peer_id=userid,
                message=message,
                attachment=attachment
            )
        key = get_start()
        send_keyboard(userid, "Товары в заказе", key)


def handle_for_order_admin(userid, message):
    orders_id = get_order_all_list()
    if message in orders_id:
        package = helper.get('package_products', ['package_id'], [clean_message(message)])
        for prods in package:
            new_prod = helper.get('product', ['id'], [str(prods[2])])
            message, attachment = create_product_card(new_prod[0])
            send_message(userid, f"Количество: {prods[3]}")
            vk.messages.send(
                random_id=vk_api.utils.get_random_id(),
                peer_id=userid,
                message=message,
                attachment=attachment
            )
        key = get_order_all()
        send_keyboard(userid, "Товары в заказе", key)



def handle_for_list_of_orders(userid, message):
    if message == "Список заказов 📖":
        send_message(userid, "Список заказов:")
        write_card_order_all(userid)
        key = get_order_all()
        send_keyboard(userid, "Выберите для полного просмотра", key)



def handle_for_status(userid, message):
    if message == "Изменить статус заказа 🔁":
        key = home()
        send_keyboard(userid, "Введите номер заказа", key)

        new_msg = New_message(userid)

        handle_new_code(userid, new_msg)

def handle_new_code(userid, order):
    key = home()
    send_keyboard(userid, "Введите статус для заказа", key)

    status = New_message(userid)

    handle_new_status(userid, status, order)


def handle_new_status(userid, new_status, order):
    helper.update('package', 'id', order, 'status', new_status)
    key = get_start_for_admin()
    send_keyboard(userid, f"Ваш статус заказа сохранён!", key)


def handle_for_sale(userid, message):
    if message == "Изменить акцию 💯":
        key = home()
        send_keyboard(userid, "Введите новую акцию:", key)

        new_msg = New_message(userid)

        handle_new_sale(userid, new_msg)


def handle_new_sale(userid, new_sale):
    helper.update('promotion', 'id', 1, 'description', new_sale)
    key = get_start_for_admin()
    send_keyboard(userid, f"Ваша новая акция сохранена!", key)


def write_card(userid, num):
    pos = num * 4
    end = pos + 4
    products_ = helper.print_info('product')
    if len(products_) < end:
        end = len(products_)
    for i in range(pos, end):
        message, attachment = create_product_card(products_[i])
        vk.messages.send(
            random_id=vk_api.utils.get_random_id(),
            peer_id=userid,
            message=message,
            attachment=attachment
        )


def handle_more(userid, message):
    if message == "Ещё 🚀":
        user = users.get(userid)
        user[2] += 1
        users.update({userid: user})
        key = get_list(user[2])
        write_card(userid, user[2])
        send_keyboard(userid, "Выберите товар для добавления в корзину", key)


def write_card_order(userid):
    orders = helper.get('package', ['user_id'], [str(userid)])
    for order in orders:
        mess = create_order_card(order)
        vk.messages.send(
            random_id=vk_api.utils.get_random_id(),
            peer_id=userid,
            message=mess
        )

def write_card_order_all(userid):
    orders = helper.print_info('package')
    for order in orders:
        user = helper.get('user', ['id'], [str(order[1])])
        mess = create_order_card_with_user(order, user[0])
        vk.messages.send(
            random_id=vk_api.utils.get_random_id(),
            peer_id=userid,
            message=mess
        )



def create_order_card(order):
    message = f"🔔 Номер заказа {order[0]}\n" \
        f"📄 Статус заказа: {order[2]} \n" \
        f"⏳ Дата заказа: {order[3]} \n" \
        f"💵 Способ оплаты: {order[4]}\n" \
        f"📦 Тип доставки: {order[5]} "

    return message


def create_order_card_with_user(order, user):
    message = f"Заказ\n" \
              f"🔔 Номер заказа {order[0]}\n" \
              f"📄 Статус заказа: {order[2]} \n" \
              f"⏳ Дата заказа: {order[3]} \n" \
              f"💵 Способ оплаты: {order[4]}\n" \
              f"📦 Тип доставки: {order[5]}\n" \
              f"Клиент \n" \
              f"⏳ Имя клиента: {user[1]} \n" \
              f"⏳ Телефон: {user[2]} \n" \
              f"💵 Город: {user[3]}\n" \
              f"📦 Адресс: {user[4]}"
    return message


def write_card_basket(userid):
    basket = helper.get('basket', ['user_id'], [str(userid)])
    basket_prod = helper.get('basket_products', ['basket_id'], [str(basket[0][0])])
    products_ = []
    for prod_id in basket_prod:
        new_prod = helper.get('product', ['id'], [str(prod_id[2])])
        products_.append([new_prod[0], prod_id[3]])
    for product in products_:
        send_message(userid, f"Количество: {product[1]}")
        message, attachment = create_product_card(product[0])
        vk.messages.send(
            random_id=vk_api.utils.get_random_id(),
            peer_id=userid,
            message=message,
            attachment=attachment
        )


def write_card_package(userid, packageid):
    package = helper.get('package', ['id', 'user_id'], [clean_message(packageid), str(userid)])  # TODO
    package_prod = helper.get('package_products', ['package_id'], [str(package[0][0])])
    products_ = []
    for prod_id in package_prod:
        new_prod = helper.get('product', ['id'], [str(prod_id[2])])
        products_.append([new_prod[0], prod_id[3]])
    for product in products_:
        send_message(userid, f"Количество: {product[1]}")
        message, attachment = create_product_card(product[0])
        vk.messages.send(
            random_id=vk_api.utils.get_random_id(),
            peer_id=userid,
            message=message,
            attachment=attachment
        )


def create_product_card(product):
    # Создаем клавиатуру для кнопки "Добавить в корзину"

    # Создаем сообщение с прикрепленной фотографией, описанием и стоимостью товара
    message = f"📦 {product[1]}\n" \
              f"💰 Цена: {product[3]}\n" \
              f"📝 Описание: {product[2]}"

    path = f"./in/{product[0]}.jpg"
    check_file = os.path.isfile(path)
    if not check_file:
        writeTofile(product[4], path)

    # Загружаем фотографию товара и получаем ее вложение
    upload = VkUpload(vk_session)
    photo = upload.photo_messages(photos=path)[0]

    # Прикрепляем фотографию к сообщению
    attachment = f"photo{photo['owner_id']}_{photo['id']}"

    return message, attachment


def New_message(id):
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == id:
            msg = event.text
            return msg

def addUser(user_id):
    if user_id in users:
        print("Good")
    else:
        users.update({user_id: user_template})

for event in longpool.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        msg = event.text
        mes = event.text.lower()
        user_id = event.user_id
        addUser(user_id)
        checkUser(user_id)
        handle_for_order(user_id, msg)
        handle_message_start(user_id, msg)
        handle_message_anketa(user_id, msg)
        handle_products(user_id, msg)
        handle_more(user_id, msg)
        handle_change_basket(user_id, msg)
        handle_change_basket_prod(user_id, msg)
        handle_message_making(user_id, msg)
        handle_message_operator(user_id, msg)
        handle_message_back(user_id, msg)
        handle_message_order(user_id, msg)
        handle_message_pay(user_id, msg)
        handle_find(user_id, msg)
        handle_for_order_admin(user_id, msg)
        handle_for_admin(user_id, mes)
        handle_for_list_of_orders(user_id, msg)
        handle_for_sale(user_id, msg)
        handle_for_status(user_id, msg)

        if (mes == "здравствуйте" or msg == "На главную 🏡" or mes == "на главную"
                or mes == "начало" or mes == "главная" or mes == "старт"
                or msg == "Режим пользователя👥"):
            key = get_start()
            send_keyboard(user_id, "Выберите команду:", key)

        Thread(target=handle_message_anketa, args=(event, id)).start()
        Thread(target=handle_for_sale, args=(event, id)).start()
        Thread(target=handle_for_status, args=(event, id)).start()
        Thread(target=handle_find, args=(event, id)).start()

