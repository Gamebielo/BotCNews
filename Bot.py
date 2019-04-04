import telepot
import json
from telepot.loop import MessageLoop
from telepot.namedtuple import (ForceReply, InlineKeyboardMarkup,
                                InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)
import requests
from bs4 import BeautifulSoup as bs

# Lendo o Json que contém o token do bot
load = open("token.json")
# Inserindo o token bot a variavel "token"
token = json.loads(load.read())
bot = telepot.Bot(token['token'])   # Inserindo o token no Bot

'''SOBRE: condicoes
Pega o a interação do usuario (via mensagem ou botão),
e faz alguma tomada de ação
'''

def ouvir(msg):
    print(msg['text'].lower().replace(' ','-'))

def condicoes(chatID, msg):
    if(msg == '/start'):
        inicio(chatID, bot)

##########################################################################################################

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
            chatID, "Especifique a marca e o modelo do celular.\nExemplo:\nSony Xperia 1\nXiaomi Mi A2 Lite",
            reply_markup=keyboard)



        # TESTES

        


        # TESTES 


        

        MessageLoop(bot, ouvir).run_as_thread()
 

##########################################################################################################

    elif (msg == 'Voltar'):
        inicio(chatID, bot)


'''SOBRE: callback
O parametro desta funcao eh um Json enviado do message_loop com os campos referente a interacao feita via a chave 'callback_query', ou seja, esta funcao eh responsavel por
por pegar o que foi emitido pelo usuario (texto iniline_keyboard) e seu respectivo ID, e repassar para a funcao 'condicoes' e que sera processado a requisicao
e sera emitido o devido comportamento que o usuario quer em relacao ao bot
'''


def callback(msg):
    query_id, from_id, query_data = telepot.glance(
        msg, flavor="callback_query")
    # Forma facilitada pela biblioteca "telepot" de quebrar inserir as informacoes para as respectivas variaveis
    # Ou seja, pega o Json com a chave callback_queryt' e quebra as informacoes em tres jogando o valor de 'text' para a variavel tipoMsg,
    # assim por adiante...

    chatID = from_id
    # ID do usuario que apertou o botao

    texto = query_data
    # o valor do botao que foi apertado

    print(chatID)

    bot.answerCallbackQuery(query_id, text="Só um instante")
    # retorna um POP-UP para o usuario quando ele digitou alguma coisa

    print("callback query", query_id, from_id, query_data)

    condicoes(chatID, texto)
    # pega o que foi clicado pelo usuario (callback_data) e seu ID manda para a funcao 'condicoes' que vai processar o clique


'''SOBRE: ir
O parametro desta funcao eh um Json enviado do message_loop com os campos referente a interacao via a chave 'chat', ou seja, esta funcao eh responsavel por
por pegar o que foi emitido pelo usuario (texto via mensagem) e seu respectivo ID, e repassar para a funcao  'condicoes' e que sera processado a requisicao
e sera emitido o devido comportamento que o usuario quer em relacao ao bot
'''


def ir(msg):
    # Forma facilitada pela biblioteca "telepot" de quebrar inserir as informacoes para as respectivas variaveis
    # Ou seja, pega o Json com a chave 'chat' e quebra as informacoes em tres jogando o valor de 'text' para a variavel tipoMsg,
    # assim por adiante...
    tipoMsg, tipoChat, chatID = telepot.glance(msg)

    # variavel Auxiliar para receber a texto que o usuario digitou, fiz ela porque se eu chamasse --condicoes(chatID, msg['text'])--
    texto = msg['text']
    # tava dando erro

    # pega o que foi digitado pelo usuario e seu ID manda para a funcao 'condicoes' que vai processar o a mensagem
    condicoes(chatID, texto)


'''SOBRE: inico
Esta funcao eh uma forma de facilitar o a primeira interacao ao usuario
'''


def inicio(chatID, bot):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Notícias"),
                KeyboardButton(text="Especificações")
            ]
        ], resize_keyboard=True
    )

    # Abre o arquivo Hello.md com o atributo leitura
    txt = open('Inicializacao/Hello.md', 'r')
    bot.sendMessage(chatID, txt.read(), 'Markdown', reply_markup=keyboard)
    txt.close()


''' SOBRE: message_loop
o message_loop eh o "listenen" das interacoes dos usuarios com o bot, ele retorna um Json, que quando uma interacao eh feita via mensagem,
recorre a chave 'chat' e redireciona o comportamento do bot para a funcao "ir", e quando uma interacao eh feita via inline_keyboard (callback_query)
recorre a chave callback
'''
bot.message_loop(
    {
        'chat': ir,
        'callback_query': callback,
    }
)

# responsavel por deixa o programa sempre em execucao, mas quando ocorre uma interacao, o message_loop e invocado, e quebra este laco infinito,
# e faz o comportamento requirido pelo usuario
while True:
    pass
