import sys
import time
import json
import telepot
import requests
from bs4 import BeautifulSoup as bs
from telepot.loop import MessageLoop
from telepot.namedtuple import (ForceReply, InlineKeyboardMarkup,
                                InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Clique Aqui', callback_data='press')],
               ])

    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

def on_callback_query(msg):                         # flavor = tipo de mensagem
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Boa Muleke')

###################################################################


def inicio(chatID, bot):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Notícias"),
                KeyboardButton(text="Especificações")
            ]
        ], resize_keyboard=True
    )

    # Abre o arquivo Hello.md e lê o conteúdo
    txt = open('Inicializacao/Hello.md', 'r')

    bot.sendMessage(chatID, txt.read(), 'Markdown', reply_markup=keyboard)
    txt.close()


def condicoes(chatID, msg):
    if (msg == '/start'):
        inicio(chatID, bot)


# NÓTÍCIAS
    elif (msg == 'Notícias'):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Mais Recentes"),
                    KeyboardButton(text="Mais Vistos"),
                    KeyboardButton(text="Voltar")
                ]
            ], resize_keyboard=True
        )
        bot.sendMessage(
            chatID, "Todas as informações relevantes na área de smartphone estão aqui.", reply_markup=keyboard)

    elif(msg == 'Mais Recentes'):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Mais Recentes"),
                    KeyboardButton(text="Mais Vistos"),
                    KeyboardButton(text="Voltar")
                ]
            ], resize_keyboard=True
        )

        urlCel = 'https://www.tudocelular.com/page/1/'
        html = requests.get(urlCel)
        sopa = bs(html.content, 'html.parser')
        urlCel = sopa.findAll('a', {'class': 'title_new'})

        cont = 0
        for i in urlCel:
            if cont >= 5:
                break
            else:
                bot.sendMessage(
                    chatID, i['href'], reply_markup=keyboard)
            cont += 1

    elif(msg == 'Mais Vistos'):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Mais Recentes"),
                    KeyboardButton(text="Mais Vistos"),
                    KeyboardButton(text="Voltar")
                ]
            ], resize_keyboard=True
        )

        urlCel = 'https://www.tudocelular.com/maisvistos/'
        html = requests.get(urlCel)
        sopa = bs(html.content, 'html.parser')
        urlCel = sopa.findAll('a', {'class': 'title_new'})

        cont = 0
        for i in urlCel:
            if cont >= 7:
                break
            else:
                bot.sendMessage(
                    chatID, i['href'], reply_markup=keyboard)
            cont += 1

# Especificações
    elif (msg == 'Especificações'):
    
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Voltar")
                ]
            ], resize_keyboard=True
        )
        bot.sendMessage(
            chatID, "Especifique a marca e o modelo do celular.\nExemplo:\nSony Xperia 1\nXiaomi Mi A2 Lite\n\n"\
            'ESTE PROCESSO PODE LEVAR ALGUNS SEGUNDOS!',
            reply_markup=keyboard)


    elif (msg == 'Voltar'):
        inicio(chatID, bot)

# Dentro da 'Especificações', após usuário digitar o celular, virá para ca
    else:
        def pegaEspec(msg):
            a = msg
            a = a.replace(' ', '+')
            url = f'https://www.gsmarena.com/res.php3?sSearch={a}'
            html = requests.get(url)
            soup = bs(html.content, 'html.parser')
            #ulTag = soup.body.findAll('ul')[2].li
            ulTag = soup.findAll('div', {'class': 'makers'})

            linkCelu = []

            count = 0
            for i in ulTag:
                linkCel = i.ul
                for x in linkCel:
                    # Limitando a quantidade de mensagem escrita
                    if count <= 3:
                        url = str(x)
                        posi = 0
                        url = url[13:]            
                        outrapos = url.find('"')
                        url = url[:outrapos]
                        linkCelu.append(url)
                        count += 1
                    
            # Concatenando os links e chamando outra função para printar
            for i in range(1, len(linkCelu)-1):
                url = f'https://www.gsmarena.com/{linkCelu[i]}'
                returnEspecs(url)


        def returnEspecs(url):
            html = requests.get(url)
            soup = bs(html.content, 'html.parser')
            
            # Pegando Algumas Especificações
            title = soup.find('h1', {'class': 'specs-phone-name-title'}).text
            chipset = soup.find('div', {'data-spec': 'chipset-hl'}).text
            memory = soup.find('td', {'data-spec': 'internalmemory'}).text
            battery = soup.find('span', {'data-spec': 'batsize-hl'}).text
            camTraseira = soup.find('td', {'data-spec': 'cam1modules'}).text
            camSelfie = soup.find('td', {'data-spec': 'cam2modules'}).text

            keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Voltar")
                ]
            ], resize_keyboard=True
            )
            bot.sendMessage(
            chatID, '\n' + title + '\n'\
            f'Chipset: {chipset}\n'\
            f'Memória: {memory}\n'\
            f'Memória: {memory}\n'\
            f'Camera(s) Traseira (s): {camTraseira}\n'\
            f'Camera(s) Selfie: {camSelfie}\n',
            reply_markup=keyboard)
            
        pegaEspec(msg)



##########################################################################################################


def ir(msg):
    # Forma facilitada pela biblioteca "telepot" de quebrar inserir as informacoes para as respectivas variaveis
    # Ou seja, pega o Json com a chave 'chat' e quebra as informacoes em tres jogando o valor de 'text' para a variavel tipoMsg,
    # assim por adiante...
    tipoMsg, tipoChat, chatID = telepot.glance(msg)

    # variavel Auxiliar para receber a texto que o usuario digitou, fiz ela porque se eu chamasse --condicoes(chatID, msg['text'])--
    texto = msg['text']

    # pega o que foi digitado pelo usuario e seu ID manda para a funcao 'condicoes' que vai processar a mensagem
    condicoes(chatID, texto)


#####################################################################################



    # ▼ MAIN ▼

# Lendo o Json que contém o token do bot
load = open("token.json")
# Inserindo o token bot a variavel "token"
token = json.loads(load.read())
bot = telepot.Bot(token['token'])   # Inserindo o token no Bot

MessageLoop(bot, {'chat': ir,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
