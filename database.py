import sqlite3


class dbworker:
	def __init__(self,database_file):
		self.connection = sqlite3.connect(database_file)
		self.cursor = self.connection.cursor()
	def user_exists(self, user_id):
		'''Проверка есть ли юзер в бд'''
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	def add_user(self,telegram_username,telegram_id,full_name):
		'''Добавляем нового юзера'''
		with self.connection:
			return self.cursor.execute("INSERT INTO `users` (`telegram_username`, `telegram_id`,`full_name`) VALUES(?,?,?)", (telegram_username,telegram_id,full_name))
	def create_profile(self,telegram_id,telegram_username,name,description,city,photo,sex,age,social_link):
		'''Создаём анкету'''
		with self.connection:
			return self.cursor.execute("INSERT INTO `profile_list` (`telegram_id`,`telegram_username`,`name`,`description`,`city`,`photo`,`sex`,`age`,`social_link`) VALUES(?,?,?,?,?,?,?,?,?)", (telegram_id,telegram_username,name,description,city,photo,sex,age,social_link))
	def profile_exists(self,user_id):
		'''Проверка есть ли анкета в бд'''
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `profile_list` WHERE `telegram_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	def delete_profile(self,user_id):
		'''Удаление анкеты'''
		with self.connection:
			return self.cursor.execute("DELETE FROM `profile_list` WHERE `telegram_id` = ?",(user_id,))
	def all_profile(self,user_id):
		'''поиск по анкетам'''
		with self.connection:
			return self.cursor.execute("SELECT * FROM `profile_list` WHERE `telegram_id` = ?",(user_id,)).fetchall()
	def edit_description(self,description,user_id):
		'''изменение описания'''
		with self.connection:
			return self.cursor.execute('UPDATE `profile_list` SET `description` = ? WHERE `telegram_id` = ?',(description,user_id))
	def edit_age(self,age,user_id):
		'''изменение возвраста'''
		with self.connection:
			return self.cursor.execute('UPDATE `profile_list` SET `age` = ? WHERE `telegram_id` = ?',(age,user_id))
	def search_profile(self,city,age,sex):
		'''поиск хаты'''
		try:
			if str(sex) == 'мужчина':
				sex_search = 'женщина'
			else:
				sex_search = 'мужчина'
			with self.connection:
				return self.cursor.execute("SELECT `telegram_id` FROM `profile_list` WHERE `city` = ? AND `sex` = ? ORDER BY `age` DESC",(city,sex_search)).fetchall()
		except Exception as e:
			print(e)
	def get_info(self,user_id):
		'''получение ифнормации по профилю'''
		with self.connection:
			return self.cursor.execute("SELECT * FROM `profile_list` WHERE `telegram_id` = ?",(user_id,)).fetchone()
	def search_profile_status(self,user_id):
		'''возвращение статуса'''
		with self.connection:
			return self.cursor.execute("SELECT `search_id` FROM `users` WHERE `telegram_id` = ?",(user_id,)).fetchone()
	def edit_profile_status(self,user_id,num):
		'''изменение статуса'''
		with self.connection:
			return self.cursor.execute('UPDATE `users` SET `search_id` = ? WHERE `telegram_id` = ?',(str(num + 1),user_id))
	def edit_zero_profile_status(self,user_id):
		'''изменение статуса на 0 когда анкеты заканчиваются'''
		with self.connection:
			return self.cursor.execute('UPDATE `users` SET `search_id` = 0 WHERE `telegram_id` = ?',(user_id,))
	def set_city_search(self,city,user_id):
		'''задования города для поиска'''
		with self.connection:
			return self.cursor.execute('UPDATE `users` SET `city_search` = ? WHERE `telegram_id` = ?',(city,user_id))
	def get_info_user(self,user_id):
		'''получение информации по юзеру'''
		with self.connection:
			return self.cursor.execute("SELECT * FROM `users` WHERE `telegram_id` = ?",(user_id,)).fetchone()
	def check_rating(self,user_id):
		'''чек по рейтингу'''
		with self.connection:
			return self.cursor.execute("SELECT `rating` FROM `profile_list` WHERE `telegram_id` = ?",(user_id,)).fetchone()
	def up_rating(self,count,user_id):
		'''добавление по рейтингу'''
		with self.connection:
			return self.cursor.execute('UPDATE `profile_list` SET `rating` = ? WHERE `telegram_id` = ?',(count + 1,user_id))
	def top_rating(self):
		'''вывод топа по рейтингу'''
		with self.connection:
			return self.cursor.execute('SELECT `telegram_id` FROM `profile_list` ORDER BY `rating` DESC LIMIT 5').fetchall()
	def count_user(self):
		'''вывод кол-ва юзеров'''
		with self.connection:
			return self.cursor.execute('SELECT COUNT(*) FROM `users`').fetchone()
	def report_exists(self,user_id,recipent):
		'''Проверка есть ли репорт в бд'''
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `reports` WHERE `send` = ? AND `recipient` = ?', (user_id,recipent)).fetchall()
			return bool(len(result))
	def throw_report(self,user_id,recipent):
		'''отправка репорта'''
		with self.connection:
			return self.cursor.execute("INSERT INTO `reports` (`send`, `recipient`) VALUES(?,?)", (user_id,recipent))
	def backup(self,name,age,city,description):
		'''откат действий'''
		with self.connection:
			return self.cursor.execute('SELECT `telegram_id` FROM `profile_list` WHERE `name` = ? AND `age` = ? AND `city` = ? AND `description` = ?', (name,age,city,description)).fetchall()
	def city_search_exists(self,user_id):
		'''есть ли city search у юзера'''
		with self.connection:
			result = self.cursor.execute('SELECT `city_search` FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchone()
			return result
	def add_like(self,sender,recipent):
		'''добавление лайка в таблицу'''
		with self.connection:
			return self.cursor.execute('INSERT INTO `likes` (`sender`,`recipient`) VALUES(?,?)', (sender,recipent))
	def add_like_exists(self,sender,recipient):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `likes` WHERE `sender` = ? AND `recipient` = ?', (sender,recipient)).fetchall()
			return bool(len(result))
