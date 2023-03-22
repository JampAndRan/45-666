import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload


session = vk_api.VkApi(token="vk1.a.WRWJRkg-dHk5cA6lzb79ZYOdJl3ITOFOPgexqilZJ15vFb0V4vgZOUqNPUMuxuCKH_zH-cti54eDSebP25ksaCvuw9L-oWaFNz-urMKmjLqBoNevSkMDhSFQF8dbsNs8exa4njLKPekCFeIuQ0f1u-ucNWKW-NUQ4MAs296hyvF5NPG8nKmU0wW-xNA1mdFRg-VzNDWQCUgovZiu4GZ3Cw")

playing_field=[
   [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
   [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
   [1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
   [1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
]
column = {
   "а": 0,
   "б": 1,
   "в": 2,
   "г": 3,
   "д": 4,
   "е": 5,
   "ё": 6,
   "ж": 7,
   "з": 8,
   "и": 9
}
list_of_participantslist_of_participants = []

def proverka(row, col):
   neighbors = []

   # Просматриваем 8 соседних ячеек (все ячейки, кроме текущей)
   for i in range(max(0, row - 1), min(row + 2, 10)):
       for j in range(max(0, col - 1), min(col + 2, 10)):
           if i != row or j != col:  # исключаем текущую ячейку
               neighbors.append(playing_field[i][j])
   return neighbors

def check(user_id):
   while True:
       for event in VkLongPoll(session).listen():
           if event.type == VkEventType.MESSAGE_NEW and event.to_me:
               choice = event.text.lower()
               if choice[0] in "абвгдеёжзи":
                   if len(choice) == 2 and choice[1] in "123456789" or len(choice) == 3 and choice[1:] == "10":
                       return [choice[0], int(choice[1:])]

                   else:
                       send_message(user_id, "Некорректное сообщение. Отправь сообщение в формате буква и цифра. Пример: Д8")

               else:
                   send_message(user_id, "Некорректное сообщение. Отправь сообщение в формате буква и цифра. Пример: Д8")



def game(user_id):
   count = 0
   while True:
       choice = check(user_id)
       if playing_field[choice[1] - 1][column[choice[0]]] == 1:
           send_message(user_id, "Госпожа удача не покинула нас. Ты попал ")
           count +=1
           playing_field[choice[1] - 1][column[choice[0]]] = -1
           if 1 in proverka(choice[1] - 1, column[choice[0]]):
               send_message(user_id, "Твоя битва еще не завершена. Делай следующий ход")
           else:
               send_message(user_id, "Капитан, мы смогли!\n корабль отправлен на дно морское")
               return count
       else:
           send_message(user_id, "О нет, это был неверный ход")
           igra = False
           return -1



def send_message(user_id, message):
  post = {
      "user_id": user_id,
      "message": message,
      "random_id": 0
  }

  session.method("messages.send",post)



for event in VkLongPoll(session).listen():



  if event.type == VkEventType.MESSAGE_NEW and event.to_me:

      text = event.text.lower()
      user_id = event.user_id

      if text == "start":
          if user_id not in list_of_participantslist_of_participants:
              #list_of_participantslist_of_participants.append(user_id)
              send_message(user_id, " Давай сыграем в морской бой! \nПравила очень просты. Я загадал поле 10 на 10 клеток, на котором, как в оригинальной игре, есть:\n1 четырехпалубный корабль\n2 трехпалубных корабля\n3 двухпалубных корабля\n4 однопалубных корабля\nТвоя задача потопить всего 1 корабль, но помни, чем лучше корабль затопишь, тем ценнее приз тебе достанется. Я буду принимать за выбор только сообщения в формате буква из кирилицы и цифра. Пример: Д8\nСтолбцы обозначаются буквами (от А до И включительно), а строки цифрами (от 1 до 10 включительно).\nУ тебя нет права на ошибку, удачи!")
              count = game(user_id)
              if count == -1:
                  send_message(user_id, "*звуки грустного тромбона*\nК сожалению, ты проиграл ((.\n Но не отчаивайся, ты проиграл битву, но не войну!")
              else:
                  send_message(user_id, "Поздравляю, ты победил!\nТы смог потопить корабль ценность которого равна {0}\nПриходи в аудиторию 2116 и найди там Торшину Ольгу Анатольевну".format(count))


          else:
              send_message(user_id, "Все попытки исчерпаны\nНо ничего, повезет в следующий раз")
      else:
          send_message(user_id,"""Я пока мало что умею\nНапиши мне start и мы с тобой сыграем""")