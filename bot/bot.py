import os
import sys
import local_imports
import random
import inspect
from antlr4 import *
from cl.gramaticaLexer import gramaticaLexer
from cl.gramaticaParser import gramaticaParser
from cl.visitor import EvalVisitor
from telegram.ext import Updater, CommandHandler


def start(update, context):
    '''
    Paràmetres: update, context
    Descripció:
    Es dona un missatge d'inici a l'usuari.
    '''
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola! Sóc un bot 🤖 especialitzat en polígons convexos. Utilitza /poly per escriure les teves comandes")


def poly(update, context):
    '''
    Paràmetres: update, context
    Descripció:
    El missatge introduït per l'usuari es tracta com a entrada pel compilador.
    El bot envia un missatge amb la sortida (si no és buida) juntament amb les
    imatges generades.
    '''
    input_stream = InputStream(update.message.text[5:])
    lexer = gramaticaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = gramaticaParser(token_stream)
    tree = parser.root()
    visitor = EvalVisitor()
    r = random.randint(1000000, 9999999)
    s = "sortida" + str(r) + ".txt"
    file = open(s, "w")
    sys.stdout = file
    visitor.visit(tree)
    file.close()
    file = open(s, "r")
    mensaje = file.read()
    if mensaje != "":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=mensaje)
    file.close()
    os.remove(s)
    path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    current_dir = os.path.dirname(path)
    for f in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, f)):
            if (f.endswith('.png') or f.endswith('.jpg')):
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(f, 'rb'))
                os.remove(f)


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('poly', poly))

updater.start_polling()
