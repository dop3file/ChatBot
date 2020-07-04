#импорт библиотек
import asyncio #асинхроность
import logging #логирование
import datetime
from datetime import timedelta  #работа со временем
import random


#aiogram и всё утилиты для коректной работы с Telegram API
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#конфиг с настройками
import config
#кастомные ответы
import custom_answer as cus_ans
#работа с базой данных
from database import dbworker
#работа с файлами
import os.path


#задаём логи
logging.basicConfig(level=logging.INFO)


#инициализируем бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())


#инициализируем базу данных
db = dbworker('database.db')



#хендлер команды /start
@dp.message_handler(commands=['start'],state='*')
async def start(message : types.Message):
	#кнопки для волшебного входа
	button_start = KeyboardButton('Зайти в волшебный мир Your Bunny врота🌀')

	magic_start = ReplyKeyboardMarkup(one_time_keyboard=True)

	magic_start.add(button_start)
	await message.answer('Привет👋\n\nЭто Your Bunny Wrote бот и я советую перечитать названия🤠\nА ещё я советую задержаться у нас подольше, у нас тут много интересного\n\nYour Bunny Wrote - место для знакомств : \n - скейтеров🛹\n - хипстеров🦹‍♀️ \n и инопланетян👽',reply_markup=magic_start)
	await message.answer_sticker('CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
	if(not db.user_exists(message.from_user.id)):
		#если юзера нет в базе добавляем его
		db.add_user(message.from_user.username,message.from_user.id,message.from_user.full_name)

#хендлер для команды Зайти в волшебный мир

@dp.message_handler(lambda message: message.text == 'Зайти в волшебный мир Your Bunny врота🌀',state='*')
async def magic_start(message : types.Message):
	#кнопки меню
	button_search = KeyboardButton('Найти человечка🔍')

	button_create_profile = KeyboardButton('Создать анкету📌')

	button_edit_profile = KeyboardButton('Редактировать анкету📝')

	button_remove_profile = KeyboardButton('Удалить🗑')

	button_rating_profile = KeyboardButton('Рейтинг анкет⭐️')

	menu = ReplyKeyboardMarkup()

	if(not db.profile_exists(message.from_user.id)):
			menu.add(button_search,button_create_profile,button_rating_profile)
	elif(db.profile_exists(message.from_user.id)) :
		menu.add(button_search,button_edit_profile,button_remove_profile,button_rating_profile)
		

	await message.answer('Привет-привет, это центральный компьютер чат бота🤖\n\nТут ты можешь управлять всеми этими штуками что внизу',reply_markup=menu)


#хендлер для создания анкеты


class CreateProfile(StatesGroup):
	name = State()
	description = State()
	city = State()
	photo = State()
	sex = State()
	age = State()
	social_link	 = State()
#хендлер старта для создания анкеты
@dp.message_handler(lambda message: message.text == 'Создать анкету📌',state='*')
async def create_profile(message : types.Message):
	#кнопки отмены
	button_exit = KeyboardButton('Назад❌')

	menu_exit = ReplyKeyboardMarkup()

	menu_exit.add(button_exit)

	if message.from_user.username != None:
		if(not db.profile_exists(message.from_user.id)):
			await message.answer("Для того что бы создать твою so style анкету нужно заполнить несколько пунктов\nДавайте начнём с твоего имя, как мне тебя называть?😉",reply_markup=menu_exit)
			await CreateProfile.name.set()
		elif(db.profile_exists(message.from_user.id)) :
			await message.answer('У тебя уже есть активная анкета\n\n')
	else:
		await message.answer('‼️У вас не заполнен username в телеграм!\n\nПожалуйста сделайте это для коректного функционирования бота\nДля этого зайдите в настройки -> Edit Profile(Изменить профиль) и жмякайте add username\n\nТам вводите желаемый никнейм и вуаля')
#хендлер для заполнения имя
@dp.message_handler(state=CreateProfile.name)
async def create_profile_name(message: types.Message, state: FSMContext):
	if str(message.text) == 'Назад❌':
		await state.finish()
		await magic_start(message)
		return
	if len(str(message.text)) < 35: 
		await state.update_data(profile_name=message.text.lower())
		await message.reply(message.text.title() + ' - п*здатое имя😉\nТеперь заполни описание своей личности что бы все поняли кто же ты : \n - инопланетянин👽\n - дурак🤡 \n - гигант мысли🧠 \n - отец русской демократии👪 \n\nбез этого никак прости :9')
		await CreateProfile.next()
	else:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return
#хендлер для заполнение описания
@dp.message_handler(state=CreateProfile.description)
async def create_profile_description(message: types.Message, state: FSMContext):
	if str(message.text) == 'Назад❌':
		await state.finish()
		await magic_start(message)
		return
	if len(message.text) < 35: 
		await state.update_data(profile_description=message.text)
		await message.answer('Неплохо,неплохо\n\nТеперь предлагаю заполнить город где вы собираетесь трепить🤪')
		await CreateProfile.next()
	else:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return
#хендлер для заполнения города 
@dp.message_handler(state=CreateProfile.city)
async def create_profile_description(message: types.Message, state: FSMContext):
	if str(message.text) == 'Назад❌':
		await state.finish()
		await magic_start(message)
		return
	if len(message.text) < 35: 
		await state.update_data(profile_city=message.text.lower())
		await message.answer('Прелестно, теперь добавим фотокарточку, что бы все знали какая ты красавица(хихи)🖼')
		await CreateProfile.next()
	else:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return
#хендлер для заполнения фотографии 
@dp.message_handler(state=CreateProfile.photo,content_types=['photo'])
async def create_profile_photo(message: types.Message, state: FSMContext):
	if str(message.text) == 'Назад❌':
		await state.finish()
		await magic_start(message)

	#кнопки выбора пола
	button_male = KeyboardButton('Мужчина')

	button_wooman = KeyboardButton('Женщина')

	button_potato = KeyboardButton('Картошка🥔')

	sex_input = ReplyKeyboardMarkup() 
	sex_input.add(button_male,button_wooman,button_potato)

	await message.photo[-1].download('photo_user/' + str(message.from_user.id) + '.jpg')
	await message.answer('Пипец ты соска)\n\nОсталось совсем немного,укажи свой пол(не тот который под тобой:)',reply_markup=sex_input)
	await CreateProfile.next()
#хендлер для заполнения пола 
@dp.message_handler(state=CreateProfile.sex)
async def create_profile_sex(message: types.Message, state: FSMContext):
	if str(message.text) == 'Назад❌':
		await state.finish()
		await magic_start(message)
		return
	if message.text == 'Мужчина' or message.text == 'Женщина':
		await state.update_data(profile_sex=message.text.lower())
		await message.answer('Замечательно!\nОсталось совсем чуть-чуть\n\nДавай же узнаем твой возвраст, что бы не сидеть восьмёрку лет если что👮‍♂️ ')
		await CreateProfile.next()
	elif message.text == 'Картошка🥔':
		await message.answer(cus_ans.joke_first())
		#прерывание функции
		return
	else:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return

#хендлер для заполнения возвраста
@dp.message_handler(state=CreateProfile.age)
async def create_profile_age(message: types.Message, state: FSMContext):
	try:
		if str(message.text) == 'Назад❌':
			await state.finish()
			await magic_start(message)
			return
		if int(message.text) < 6:
			await message.answer('ой🤭\nТы чёт маловат...')
			await message.answer(cus_ans.random_reapeat_list())

			#прерывание функции
			return
		elif int(message.text) > 54:
			await message.answer('Пажилой человек👨‍')
			await message.answer(cus_ans.random_reapeat_list())

			#прерывание функции
			return
		elif int(message.text) > 6 and int(message.text) < 54:
			await state.update_data(profile_age=message.text)
			#кнопки меню
			button_skip = KeyboardButton('Пропустить')

			skip_input = ReplyKeyboardMarkup(one_time_keyboard=True) 
			skip_input.add(button_skip)
			await message.answer('За№бись!!\nПоследний шаг - указать ссылку на социальную сеть\nЕсли нет желания - можно пропустить➡🔜',reply_markup=skip_input)
			await CreateProfile.next()
	except:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return
#хендлер для заполнения ссылки на социальную сеть
@dp.message_handler(state=CreateProfile.social_link)
async def create_profile_social_link(message: types.Message, state: FSMContext):
	try:
		if str(message.text) == 'Назад❌':
			await state.finish()
			await magic_start(message)
			return
		if str(message.text) == 'Пропустить':
			await message.answer('Анкета успешно создана!')
			user_data = await state.get_data()
			db.create_profile(message.from_user.id,message.from_user.username,str(user_data['profile_name']),str(user_data['profile_description']),str(user_data['profile_city']),'photo/' + str(message.from_user.id) + '.jpg',str(user_data['profile_sex']),str(user_data['profile_age']),None) #self,telegram_id,telegram_username,name,description,city,photo,sex,age,social_link
			await state.finish()
		elif str(message.text).startswith('https://'):
			await state.update_data(profile_link=message.text)
			await message.answer('Анкета успешно создана!')
			user_data = await state.get_data()
			db.create_profile(message.from_user.id,message.from_user.username,str(user_data['profile_name']),str(user_data['profile_description']),str(user_data['profile_city']),'photo/' + str(message.from_user.id) + '.jpg',str(user_data['profile_sex']),str(user_data['profile_age']),str(user_data['profile_link'])) #self,telegram_id,telegram_username,name,description,city,photo,sex,age,social_link
			await state.finish()
			await magic_start(message)
		if (not str(message.text) == 'Пропустить') and (not str(message.text).startswith('https://')) :
			await message.answer('Ссылка корявая!!\n\nОна должна начинаться с https://')

			return


	except:
		await message.answer(cus_ans.random_reapeat_list())
		#прерывание функции
		return

#хендлер для удаления анкеты
@dp.message_handler(lambda message: message.text == 'Удалить🗑')
async def delete_profile(message : types.Message):
	try:
		db.delete_profile(message.from_user.id)
		await message.answer('Анкета успешно удалена!')
		await magic_start(message)
	except:
		await message.answer(cus_ans.random_reapeat_list())
		return

#хендлер для редактирования анкеты
@dp.message_handler(lambda message: message.text == 'Редактировать анкету📝')
async def edit_profile(message : types.Message):
	try:
		if(not db.profile_exists(message.from_user.id)):
			await message.answer('У тебя нет анкеты!')
		elif(db.profile_exists(message.from_user.id)) :
			photo = open('photo_user/' + str(message.from_user.id) + '.jpg','rb')
			#кнопки выбора пола
			button_again = KeyboardButton('Заполнить анкету заново🔄')

			button_edit_description = KeyboardButton('Изменить описание анкеты📝')

			button_edit_age = KeyboardButton('Изменить количество годиков👶')

			button_cancel = KeyboardButton('Назад❌')

			edit_profile = ReplyKeyboardMarkup(one_time_keyboard=True) 
			edit_profile.add(button_again,button_edit_description,button_edit_age,button_cancel)
			caption = 'Твоя анкета:\n\nИмя - ' + str(db.all_profile(str(message.from_user.id))[0][3]).title() + '\nОписание - ' + str(db.all_profile(str(message.from_user.id))[0][4]) + '\nМесто жительство🌎 - ' + str(db.all_profile(str(message.from_user.id))[0][5]).title() + '\nСколько годиков?) - ' + str(db.all_profile(str(message.from_user.id))[0][8])  
			await message.answer_photo(photo,caption=caption,reply_markup=edit_profile)
			photo.close()
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)
		return

#хендлер для заполнения анкеты заново
@dp.message_handler(lambda message: message.text == 'Заполнить анкету заново🔄')
async def edit_profile_again(message : types.Message):
	try:
		db.delete_profile(message.from_user.id)
		await create_profile(message)

	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)
		return

#класс машины состояний FSM
class EditProfile(StatesGroup):
	description_edit = State()
	age_edit = State()

#хендлеры для изменение возвраста и описания анкеты

@dp.message_handler(lambda message: message.text == 'Изменить количество годиков👶' or message.text == 'Изменить описание анкеты📝')
async def edit_profile_age(message : types.Message):
	try:
		#кнопки для отмены
		button_cancel = KeyboardButton('Отменить❌')

		button_cancel_menu = ReplyKeyboardMarkup(one_time_keyboard=True)

		button_cancel_menu.add(button_cancel)

		if message.text == 'Изменить количество годиков👶':
			await message.answer('Введи свой новый возвраст',reply_markup=button_cancel_menu)
			await EditProfile.age_edit.set()
		elif message.text == 'Изменить описание анкеты📝':
			await message.answer('Введи новое хайп описание своей анкеты!',reply_markup=button_cancel_menu)
			await EditProfile.description_edit.set()
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)
		return
@dp.message_handler(state=EditProfile.age_edit)
async def edit_profile_age_step2(message: types.Message, state: FSMContext):
	try:
		if str(message.text) == 'Отменить❌':
			await state.finish()
			await magic_start(message)

			return
		elif int(message.text) < 6:
			await message.answer('ой🤭\nТы чёт маловат...')
			await message.answer(cus_ans.random_reapeat_list())

			#прерывание функции
			return
		elif int(message.text) > 54:
			await message.answer('Пажилой человек👨‍')
			await message.answer(cus_ans.random_reapeat_list())

			#прерывание функции
			return
		elif int(message.text) > 6 and int(message.text) < 54:
			await message.answer('Малый повзрослел получается🤗\n\nВозвраст успешно измененён!')
			await state.update_data(edit_profile_age=message.text)
			user_data = await state.get_data()

			db.edit_age(user_data['edit_profile_age'],str(message.from_user.id))
			await state.finish()	
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)
		return
@dp.message_handler(state=EditProfile.description_edit)
async def edit_profile_description_step2(message: types.Message, state: FSMContext):
	try:
		if str(message.text) == 'Отменить❌':
			await state.finish()
			await magic_start(message)

			return
		await message.answer('Прекрасное описание броди\n\nОписание успешно изменено!')
		await state.update_data(edit_profile_description=message.text)
		user_data = await state.get_data()

		db.edit_description(user_data['edit_profile_description'],str(message.from_user.id))
		await state.finish()
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)
		return

@dp.message_handler(lambda message: message.text == 'Назад❌')
async def exit(message : types.Message):
	await magic_start(message)



#класс машины состояний FSM
class SearchProfile(StatesGroup):
	city_search = State()
	in_doing = State()
	
#хендлеры для поиска по анкетам
@dp.message_handler(lambda message: message.text == 'Найти человечка🔍')
async def search_profile(message : types.Message):
	try:
		if db.profile_exists(message.from_user.id) == False:
			await message.answer('У тебя нет анкеты, заполни её а потом приходи сюда!')
		else:
			await message.answer('Выбери город для поиска человечка :)')
			await SearchProfile.city_search.set()
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		await state.finish()
		print(e)
		return

@dp.message_handler(state=SearchProfile.city_search)
async def seach_profile_step2(message: types.Message, state: FSMContext):
	try:
		await state.update_data(search_profile_city=message.text.lower())

		user_data = await state.get_data()

		db.set_city_search(str(user_data['search_profile_city']),str(message.from_user.id))
		if (bool(len(db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))))):
			try:
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			except:
				db.edit_zero_profile_status(message.from_user.id)
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			
			db.edit_profile_status(str(message.from_user.id),db.search_profile_status(str(message.from_user.id))[0])
			
			#кнопки для оценки
			button_like = KeyboardButton('👍')

			button_dislike = KeyboardButton('👎')

			button_exit = KeyboardButton('Назад❌')

			mark_menu = ReplyKeyboardMarkup()

			mark_menu.add(button_dislike,button_like,button_exit)

			name_profile = str(db.get_info(profile_id)[3])
			age_profile = str(db.get_info(profile_id)[8])
			description_profile = str(db.get_info(profile_id)[4])
			social_link_profile = str(db.get_info(profile_id)[9])
			photo_profile = open('photo_user/' + str(profile_id) + '.jpg','rb')

			city = str(db.get_info_user(message.from_user.id)[6]).title()

			final_text_profile = f'Смотри, кого для тебя нашёл☺️\n\n{name_profile},{age_profile},{city}\n{description_profile}'

			await message.answer_photo(photo_profile,caption=final_text_profile,reply_markup=mark_menu)

			

			await SearchProfile.next()
		else:
			await message.answer('Такого города нет или там нет анкет :(')
			await state.finish()
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list()) 
		await state.finish()
		await magic_start(message)
		print(e)

@dp.message_handler(state=SearchProfile.in_doing)
async def seach_profile_step3(message: types.Message, state: FSMContext):
	try:
		if str(message.text) == '👍':
			if str(message.text) == '/start' or str(message.text) == 'Назад❌':
				await state.finish()
				await magic_start(message)

			user_data = await state.get_data()

			try:
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			except IndexError:
				db.edit_zero_profile_status(message.from_user.id)
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			except Exception as e:
				print(e)
				await state.finish()
				await magic_start(message)
			db.edit_profile_status(str(message.from_user.id),db.search_profile_status(str(message.from_user.id))[0])
			name_profile = str(db.get_info(profile_id)[3])
			age_profile = str(db.get_info(profile_id)[8])
			description_profile = str(db.get_info(profile_id)[4])
			social_link_profile = str(db.get_info(profile_id)[9])
			photo_profile = open('photo_user/' + str(profile_id) + '.jpg','rb')

			city = str(user_data['search_profile_city']).title()

			final_text_profile = f'Смотри, кого для тебя нашёл☺️\n\n{name_profile},{age_profile},{city}\n{description_profile}'

			await message.answer_photo(photo_profile,caption=final_text_profile)
			
			name_profile_self = str(db.get_info(str(message.from_user.id))[3])
			age_profile_self = str(db.get_info(str(message.from_user.id))[8])
			description_profile_self = str(db.get_info(str(message.from_user.id))[4])
			social_link_profile_self = str(db.get_info(str(message.from_user.id))[9])
			photo_profile_self = open('photo_user/' + str(message.from_user.id) + '.jpg','rb')

			city_self = str(user_data['search_profile_city']).title()
			final_text_profile_self = f'Тобой кто то заинтересовался!\nСам в шоке😮..\n\n{name_profile_self},{age_profile_self},{city_self}\n{description_profile_self}\n\nЧего ты ждёшь,беги знакомиться - @{str(message.from_user.username)}'
			await bot.send_photo(profile_id,photo_profile_self,caption=final_text_profile_self)
			return
			await state.finish()
		elif str(message.text) == '👎':
			if str(message.text) == '/start' or str(message.text) == 'Назад❌':
				await state.finish()
				await magic_start(message)

			user_data = await state.get_data()

			try:
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			except IndexError:
				db.edit_zero_profile_status(message.from_user.id)
				profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[6]),str(db.get_info(str(message.from_user.id))[8]),str(db.get_info(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
			except Exception as e:
				print(e)
				await state.finish()
				await magic_start(message)
			db.edit_profile_status(str(message.from_user.id),db.search_profile_status(str(message.from_user.id))[0])
			name_profile = str(db.get_info(profile_id)[3])
			age_profile = str(db.get_info(profile_id)[8])
			description_profile = str(db.get_info(profile_id)[4])
			social_link_profile = str(db.get_info(profile_id)[9])
			photo_profile = open('photo_user/' + str(profile_id) + '.jpg','rb')

			city = str(user_data['search_profile_city']).title()

			final_text_profile = f'Смотри, кого для тебя нашёл☺️\n\n{name_profile},{age_profile},{city}\n{description_profile}'

			await message.answer_photo(photo_profile,caption=final_text_profile)
		else:
			await state.finish()
			await magic_start(message)
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		await state.finish()
		await magic_start(message)
		print(e)
		return

#хендлер для рейтинга анкет

@dp.message_handler(lambda message: message.text == 'Рейтинг анкет⭐️',state='*')
async def rating_profile(message : types.Message):
	try:
		final_top = ''
		top_count = 0
		for i in db.top_rating():
			for d in i:
				top_count +=1
				final_top = final_top + str(top_count) + ' место - ' + str(db.get_info(str(d))[3]).title() + ' из города ' + str(db.get_info(str(d))[5]).title() + '\n' 
		await message.answer(f'Рейтинг самых п#здатых в этом чат боте😎\n\n{final_top}')
	except Exception as e:
		await message.answer(cus_ans.random_reapeat_list())
		print(e)


#хендлер который срабатывает при непредсказуемом запросе юзера
@dp.message_handler()
async def end(message : types.Message):
	await message.answer('Я не знаю, что с этим делать 😲\nЯ просто напомню, что есть команда /start',parse_mode=ParseMode.MARKDOWN)






executor.start_polling(dp, skip_updates=True)