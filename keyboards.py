from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DBHelper import DBHelper

helper = DBHelper()
def get_start():
    key = VkKeyboard(one_time=True)
    key.add_button('Каталог 🗂', color=VkKeyboardColor.SECONDARY)
    key.add_button('Корзина 🛒', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Заказы 📋', color=VkKeyboardColor.SECONDARY)
    key.add_button('Акции 💯', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Анкета 📝', color=VkKeyboardColor.SECONDARY)
    key.add_button('Помощь 🙏', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('О нас 🏪', color=VkKeyboardColor.SECONDARY)
    return key


def get_start_for_admin():
    key = VkKeyboard(one_time=True)
    key.add_button('Список заказов 📖', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Изменить статус заказа 🔁', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Изменить акцию 💯', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Режим пользователя👥', color=VkKeyboardColor.SECONDARY)
    return key


def get_katalog():
    key = VkKeyboard(one_time=True)
    key.add_button('Корзина 🛒', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Поиск 🔎', color=VkKeyboardColor.SECONDARY)
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_anketa():
    key = VkKeyboard(one_time=True)
    key.add_button('Имя 👩👨', color=VkKeyboardColor.SECONDARY)
    key.add_button('Телефон 📞', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Адрес 🏨', color=VkKeyboardColor.SECONDARY)
    key.add_button('Город 🏤', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_back_anketa():
    key = VkKeyboard(one_time=True)
    key.add_button('Назад ⬅', color=VkKeyboardColor.SECONDARY)
    return key


def get_basket(vkid):
    product_names = get_name_vkid(vkid)
    keys = VkKeyboard(one_time=True)
    for i in range(len(product_names)):
        name = product_names[i]
        newName = name + " 📦"
        keys.add_button(newName, color=VkKeyboardColor.SECONDARY)
        keys.add_line()
    keys.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    keys.add_button('Оформить заказ 📦', color=VkKeyboardColor.SECONDARY)
    return keys


def home():
    key = VkKeyboard(one_time=True)
    key.add_button('Режим пользователя👥', color=VkKeyboardColor.SECONDARY)
    key.add_button('На главную 🏠', color=VkKeyboardColor.SECONDARY)
    return key

def get_order(userid):
    key = VkKeyboard(one_time=True)
    orders = helper.get('package', ['user_id'], [str(userid)])
    for order in orders:
        key.add_button(str(order[0]) + " 🔔", color=VkKeyboardColor.SECONDARY)
        key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_order_all():
    key = VkKeyboard(one_time=True)
    orders = helper.print_info('package')
    for order in orders:
        key.add_button(str(order[0]) + " ⚒", color=VkKeyboardColor.SECONDARY)
        key.add_line()
    key.add_button('На главную 🏠', color=VkKeyboardColor.SECONDARY)
    return key


def get_order_all_list():
    orders = helper.print_info('package')
    ord = []
    for order in orders:
        ord.append(str(order[0]) + " ⚒")
    return ord


def get_list_order(userid):
    orders = helper.get('package', ['user_id'], [str(userid)])
    list = []
    for orders in orders:
        list.append(str(orders[0]) + " 🔔")
    return list

def get_making():
    key = VkKeyboard(one_time=True)
    key.add_button('Самовывоз 🚹', color=VkKeyboardColor.SECONDARY)
    key.add_button('Доставка 🚕', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_pay():
    key = VkKeyboard(one_time=True)
    key.add_button('Наличными при получении 💵', color=VkKeyboardColor.SECONDARY)
    key.add_button('Переводом на карту 💳', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_chat():
    key = VkKeyboard(one_time=True)
    key.add_button('Оператор 📞', color=VkKeyboardColor.SECONDARY)
    key.add_openlink_button('Чат с менеджером 🗒', link="https://vk.com/sellstolen")
    key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_product():
    key = VkKeyboard(one_time=True)
    key.add_button('Корзина 🛒', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_home():
    key = VkKeyboard(one_time=True)
    key.add_button('На главную 🏡', color=VkKeyboardColor.SECONDARY)
    return key


def get_list(num):
    product_names = get_name()
    keys = VkKeyboard(one_time=True)
    pos = num * 4
    end = pos + 4
    if len(product_names) < end:
        end = len(product_names)
    for i in range(pos, end):
        name = product_names[i]
        keys.add_button(name + " ✅", color=VkKeyboardColor.SECONDARY)
        keys.add_line()
    keys.add_button("Ещё ⏩")
    keys.add_button("Поиск 🔎")
    keys.add_line()
    keys.add_button("На главную 🏡")
    return keys

def get_list_search(name):
    product_names = get_name_search(name)
    keys = VkKeyboard(one_time=True)

    for i in range(len(product_names)):
        name = product_names[i]
        newName = name + " ✅"
        keys.add_button(newName, color=VkKeyboardColor.SECONDARY)
        keys.add_line()
    keys.add_button('На главную 🏡')
    return keys


def get_name():
    products_ = helper.print_info('product')
    product_names = []
    index = 0
    for prod in products_:
        product_names.append(prod[1])
    return product_names


def get_name_for_search():
    products_ = helper.print_info('product')
    product_names = []
    index = 0
    for prod in products_:
        product_names.append(prod[1] + " ✅")
    return product_names


def get_name_search(name):
    products_ = helper.print_info('product')
    product_names = []
    index = 0
    for prod in products_:
        if name.lower() in prod[1].lower():
            product_names.append(prod[1])
    return product_names

def get_name_change():
    key = VkKeyboard(one_time=True)
    key.add_button('Удалить товар ❌', color=VkKeyboardColor.SECONDARY)
    key.add_line()
    key.add_button('Добавить товар ✔', color=VkKeyboardColor.SECONDARY)
    return key

def get_name_vkid(vkid):  # TODO
    basket = helper.get('basket', ['user_id'], [str(vkid)])
    basket_prod = helper.get('basket_products', ['basket_id'], [str(basket[0][0])])
    products_ = []
    for prod_id in basket_prod:
        new_prod = helper.get('product', ['id'], [str(prod_id[2])])
        products_.append(new_prod[0][1])
    return products_


def get_name_list_basket(vkid):
    prod = get_name_vkid(vkid)
    new = []
    for pr in prod:
        new.append(pr + " 📦")
    return new
