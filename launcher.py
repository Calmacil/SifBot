#!/usr/bin/env python

import discord
from discord.ext import commands
import random
import asyncio
import re
import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sifbot.dice import DiceBag, DiceError
from sifbot.macros import Macro

"""
all the true stuff beyond this point

discord user id: 275289707796103168
"""

description = """ FiveBot est un lanceur de dés pour le système Roll n' Keep.
Entre autres choses. """

bot = commands.Bot(command_prefix='.', description=description)
dbe = create_engine('sqlite:///bot.db')
base = declarative_base()
DBSession = sessionmaker(bind=dbe)
dbs = DBSession()

# TODO Tu changes ces deux machins là
bot_email = "thekingofthenight@yopmail.com"
bot_password = "les noms c'est ma nemesis"


@bot.event
@asyncio.coroutine
def on_ready():
    print("Connecté en tant que:")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

@bot.command(pass_context=True, description="Kills the bot")
@asyncio.coroutine
def kill(ctx):
    print("Kill command received")

    if (ctx.message.author.name=="Calmacil"):
        yield from bot.say("Hé salut les amis!")
        yield from bot.logout()
    yield from bot.send_message(ctx.message.channel, "Bien essayé, petit coquin, mais c’est raté! *Fait une croix*")

# macro commands
@bot.group(pass_context=True)
@asyncio.coroutine
def macro(ctx):
    if ctx.invoked_subcommand is None:
        yield from bot.say("Non, la cuiller [{}] n'existe pas".format(ctx.subcommand_passed))

@macro.command(name='add', pass_context=True)
@asyncio.coroutine
def _macro_add(ctx, name : str, roll : str, comment=None):
    """ Registers a new macro

    .macro add <name> <"5k3 + 2"> <"Some cool comment">
    """
    discord_userid = ctx.message.author.id

    new_macro = Macro(discord_userid=discord_userid, name=name, roll=roll, comment=comment)
    dbs.add(new_macro)
    dbs.commit()
    yield from bot.say("Le nouveau jet de dés est enregistré.")

@macro.command(name='list', pass_context=True)
@asyncio.coroutine
def _macro_list(ctx):
    """ Lists all the macros for the user """
    discord_userid = ctx.message.author.id
    macros = dbs.query(Macro).filter(Macro.discord_userid == discord_userid).all()

    if len(macros):
        yield from bot.say("Voici les commandes que tu connais, petit yoriki:")
        for macro in macros:
            yield from bot.say("!{}: {}".format(macro.name, macro.roll))
    else:
        yield from bot.say("Tu n’as pas encore enregistré de jets de dés, petit scarabée.")

@macro.command(name='del', pass_context=True)
@asyncio.coroutine
def _macro_del(ctx, name : str):
    """ Delete the specified macro

    .macro del <name>
    """
    discord_userid = ctx.message.author.id
    macro = dbs.query(Macro).filter(Macro.discord_userid == discord_userid).filter(Macro.name == name).first()
    dbs.delete(macro)
    dbs.commit()
    yield from bot.say("Le jet {} a été supprimé".format(name))

@bot.event
@asyncio.coroutine
def on_message(msg):
    """ Parses incoming messages """
    response = None
    comment = ""

    if not isinstance(msg, discord.Message):
        raise TypeError("Message expected")

    chan = msg.channel
    user_nick = msg.author.name
    content = ' '.join(msg.content.replace('+', ' + ').replace('-', ' - ').split())
    if hasattr(msg.author, 'nick'):
        user_nick = msg.author.nick

    # get comment
    comment_pos = content.find('#')     # no excetpion raised if not found
    if comment_pos > 0:
        comment = content[comment_pos+1:]
        content = content[:comment_pos]

    # splits the string
    content = content.split(' ')

    # check for dice roll
    dice_pattern = re.compile('\d+[kKdD]')

    if dice_pattern.match(content[0]):
        print("Roll detected")
        bag = DiceBag(content)
        try:
            #resp = "%s a lancé %s et a obtenu %s\n%s" % (user_nick,
            #                                             " ".join(content),
            #                                             bag.roll(),
            #                                             comment)
            result, successes = bag.roll()

            resp = "%s a lancé %s et a obtenu %s" % (user_nick, " ".join(content), result)
            if comment: resp += "\n%s" % (comment)
        except DiceError as e:
            resp = e.args[0]

        del bag
        yield from bot.send_message(chan, resp)
    elif content[0].startswith('!'):
        m = dbs.query(Macro).filter(Macro.discord_userid == msg.author.id).filter(Macro.name == content[0][1:])
        if not len(m.all()):
            yield from bot.say("Je ne connais pas cette commande.")
        else:
            m = m.one()
            cmd = m.roll + " ".join(content[1:])
            bag = DiceBag(cmd.split(" "))
            try:
                resp = "%s a lancé %s et a obtenu %s" % (user_nick,cmd, bag.roll())
                if m.comment is not None: resp += "\n# %s" % m.comment
                if comment: resp += "\n# %s" % comment
            except DiceError as e:
                resp = e.args[0]
            del bag
            yield from bot.send_message(chan, resp)

    yield from bot.process_commands(msg)


bot.run(bot_email, bot_password)
