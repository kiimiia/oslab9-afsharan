import telebot
import qrcode
import random
from khayyam import JalaliDatetime
from gtts import gTTS

number = random.randint(0, 50)

bot = telebot.TeleBot("2124577254:AAE4XNR7lqVx2iBhDQPlPgrUf8wYxS8mOsE")

#start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "خوش آمدی" + message.from_user.first_name)


#max
@bot.message_handler(commands=['max'])
def send_max(message):
    array = bot.send_message(message.chat.id, 'enter the numbers like this: 1,2,3,4,5 to find the max\n')   
    bot.register_next_step_handler(array, find_max)


def find_max(array):

    try:
        nums = list(map(int, array.text.split(',')))
        max_num = max(nums)
        bot.send_message(array.chat.id, "max number in your array is" + str(max_num) )

    except:
        array = bot.send_message(array.chat.id,'error!! please  enter the numbers like this: 1,2,3,4,5 to find the max')
        bot.register_next_step_handler(array, find_max)


#argmax
@bot.message_handler(commands=['argmax'])
def send_max_index(message):
    array = bot.send_message(message.chat.id, 'enter the numbers like this: 1,2,3,4,5')
    bot.register_next_step_handler(array, find_max_index)


def find_max_index(array):

    try:
        nums = list(map(int, array.text.split(',')))
        max_num = nums.index(max(nums)) + 1
        bot.send_message(array.chat.id, " max number index is " + str(max_num) )

    except:
        array = bot.send_message(array.chat.id,'error!! please  enter the numbers like this: 1,2,3,4,5')
        bot.register_next_step_handler(array, find_max_index)


#qrcode
@bot.message_handler(commands=['qrcode'])
def qrcode_generate(message):
    text = bot.send_message(message.chat.id, 'enter your text')
    bot.register_next_step_handler(text, send_qrcode)


def send_qrcode(message):

    try:
        img = qrcode.make(message.text)
        img.save('QrCode.png')
        qr_png = open('QrCode.png', 'rb')
        bot.send_photo(message.chat.id, qr_png)

    except:
        str = bot.send_message(message.chat.id, 'نه نشد! فقط متن بهم بده')
        bot.register_next_step_handler(str,send_qrcode )


#help
@bot.message_handler(commands=['help'])
def help(message):
    text = bot.send_message(message.chat.id, """
/start
welcome
/game 
to Guess the number in game
/age
Enter date of birth in Hijri Shamsi and receive your age
/voice
changing text to voice
/max
to find max number of array
/argmax
to find max number index of array
/qrcode
to receive qrcode for text
/help
commands list
        """)


#game
@bot.message_handler(commands=['game'])
def guess_number_game(message):
    global number
    number = random.randint(0, 50)
    user_guess = bot.send_message(message.chat.id, 'Guess the number in game')
    bot.register_next_step_handler(user_guess, game)


def game(user_guess):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn = telebot.types.KeyboardButton('New Game')
    markup.add(itembtn)
    global number
    if user_guess.text == "New Game":

        user_guess = bot.send_message(user_guess.chat.id, 'new game!! guess the number',reply_markup=markup)
        number = random.randint(0, 50)
        bot.register_next_step_handler(user_guess, game)

    else:

        try:

            if int(user_guess.text) < number:
                user_guess = bot.send_message(user_guess.chat.id, 'Your guess is less than number', reply_markup=markup)
                bot.register_next_step_handler(user_guess, game)

            elif int(user_guess.text) > number:
                user_guess = bot.send_message(user_guess.chat.id, 'Your guess is greater than number', reply_markup=markup)
                bot.register_next_step_handler(user_guess, game)

            else:
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                bot.send_message(user_guess.chat.id, 'you win!!!', reply_markup=markup)

        except:
            user_guess = bot.send_message(user_guess.chat.id, 'enter the number between 0-50', reply_markup=markup)
            bot.register_next_step_handler(user_guess, game)


#age
@bot.message_handler(commands=['age'])
def calculating_age(message):
    birth_day = bot.send_message(message.chat.id, ' enter the date of birth like this: year/month/day=> (1378/2/15)')
    bot.register_next_step_handler(birth_day, age_Computing)


def age_Computing(birth_day):

    try:
        b = birth_day.text.split("/")
        sub = JalaliDatetime.now() - JalaliDatetime(b[0], b[1], b[2])
        sub = str(sub)
        sub = sub.split(' ')
        year = int(int(sub[0]) / 365)
        bot.send_message(birth_day.chat.id, " you are " + str(year) )

    except:
        birth_day = bot.send_message(birth_day.chat.id,'error!! enter the date of birth like this: year/month/day=> (1378/2/15)')
        bot.register_next_step_handler(birth_day, age_Computing)


#voice
@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    sentence = bot.send_message(message.chat.id, 'enter the english text')
    bot.register_next_step_handler(sentence, text2voice)


def text2voice(sentence):
    try:
        my_text = sentence.text
        language = 'en'
        content = gTTS(text=my_text, lang=language, slow=False)
        content.save("content.mp3")
        voice = open('content.mp3', 'rb')
        bot.send_voice(sentence.chat.id, voice)
    except:
        sentence = bot.send_message(sentence.chat.id, 'error!! enter english text')
        bot.register_next_step_handler(sentence, text2voice)


bot.infinity_polling()