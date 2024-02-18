from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, Director, Admins
import buttons
from staff_config import staff


# =======================================================================================================================

class FSM_order(StatesGroup):
    size = State()
    quantity = State()
    number = State()
    fullname = State()
    submit = State()


async def fsm_start(call: types.CallbackQuery, state: FSMContext):
    if call.message.from_user.id in staff or \
       call.message.from_user.id in Director or \
       call.message.from_user.id in Admins:

        await call.message.answer('Вы сотдруник или админ, вы не можете оформить заказ!')

    else:
        async with state.proxy() as data:
            buyer_id = int(call.data.replace("to_order", "").strip())
            text = call.message.text
            lines = text.split("\n")
            for line in lines:
                if line.startswith("Байер:"):
                    buyer_name = line.split("Байер: ")[1].strip()
                elif line.startswith("Артикул:"):
                    article = line.split("Артикул: ")[1].strip()
                    break

            data['company_name'] = buyer_name
            data['article'] = article
            data['buyer_id'] = buyer_id

            await FSM_order.size.set()
            await call.message.reply(f"Байер: {data['company_name']}\n"
                                     f"Артикул: {data['article']}\n\n"
                                     f"Ваш размер? (xxl, l и т.д)", reply_markup=buttons.cancel_for_client)


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSM_order.next()
    await message.answer('Количество товара?')


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await FSM_order.next()
    await message.answer("Ваш номер телефона или то через что мы сможем с вами связаться!\n\n"
                         "(Instagram, Telegram, WhatsAppи или телефон номер!)")


async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await FSM_order.next()
    await message.answer("Ваше ФИО?\n")


async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text

    await message.answer(text=f"Данные: ⬇️\n\n"
                              f"Байер: {data['company_name']}\n"
                              f"Артикул: {data['article']}\n"
                              f"Размер: {data['size']}\n"
                              f"Количество товара: {data['quantity']}\n"
                              f"Телефон номер или соц.сеть: {data['number']}\n"
                              f"ФИО: {data['fullname']}", reply_markup=buttons.submit_markup)
    await FSM_order.next()
    await message.answer('Верно?!')


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == "да":
        await message.answer('Отправлено менеджерам!', reply_markup=buttons.StartClient)
        async with state.proxy() as data:
            photo = open('media/for_order.png', 'rb')

# ====================================Отправка заказа своему байеру=====================================================

            await bot.send_photo(photo=photo, chat_id=data['buyer_id'], caption=f"Новый заказ!\n\n"
                                                                     f"Артикул: {data['article']}\n"
                                                                     f"Размер: {data['size']}\n"
                                                                     f"Количество товара: {data['quantity']}\n"
                                                                     f"Телефон номер или соц.сеть: {data['number']}\n"
                                                                     f"ФИО: {data['fullname']}")
        # Запись в базу данных
# ======================================================================================================================

        await state.finish()

    elif message.text.lower() == "нет":
        await message.answer('Отменено!', reply_markup=buttons.StartClient)
        await state.finish()

    else:
        await message.answer("Пожалуйста, выберите Да или Нет.")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartClient)


# =======================================================================================================================
def register_order_for_client(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена!", ignore_case=True), state="*")
    dp.register_callback_query_handler(fsm_start,
                                       lambda call: call.data and call.data.startswith("to_order"))

    dp.register_message_handler(load_size, state=FSM_order.size)
    dp.register_message_handler(load_quantity, state=FSM_order.quantity)
    dp.register_message_handler(load_number, state=FSM_order.number)
    dp.register_message_handler(load_fullname, state=FSM_order.fullname)
    dp.register_message_handler(load_submit, state=FSM_order.submit)
