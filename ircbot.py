#!/usr/bin/env python3

import irc.bot
import irc.connection

import ssl
import time
import random
import datetime
from concurrent.futures import ProcessPoolExecutor

from options import get_irc_credentials


class IrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, port, channel, nickname, server_password):
        if server_password == "":
            server_password = None

        server_list = [irc.bot.ServerSpec(server, port, server_password)]
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(self, server_list, nickname, nickname, connect_factory=factory)
        self.channel = channel
        self.password = server_password
        self.nickname = nickname

    def say(self, c, msg):
        c.privmsg(self.channel, msg)

    def on_nicknameinuser(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        # don't reply to private messages
        pass


class Anna(IrcBot):
    messages = [
        "jag är ingen bot ;)",
        "jag är en väldigt"
    ]

    def on_welcome(self, c, e):
        c.join(self.channel)

        def tick():
            print("called tick")
            msg = random.choice(Anna.messages)
            c.privmsg(self.channel, msg)

            video_msg = "https://www.youtube.com/watch?v=RYQUsp-jxDQ"
            c.privmsg(self.channel, video_msg)

        interval = datetime.timedelta(hours=1)
        self.reactor.scheduler.execute_every(period=interval, func=tick)
        tick()


class BassHunter(IrcBot):
    lyrics = [
        """
        Jag känner en bot
        Hon heter Anna. Anna heter hon
        Och hon kan banna banna dig så hårt
        Hon röjer upp I våran kanal
        Jag vill berätta för dig att jag känner en bot
        """,

        """
        Jag känner en bot
        Hon heter Anna. Anna heter hon
        Och hon kan banna banna dig så hårt
        Hon röjer upp I våran kanal
        Jag vill berätta för dig att jag känner en bot
        Som alltid vaktar alla som är här
        Och som ser till att vi blir utan besvär
        Det finns ingen take-over som lyckas
        Kom ihåg att det är jag som känner en bot
        """,

        """
        En bot som ingen ingen annan slår
        Och hon kan kicka utan att hon får
        Hon gör sig av med alla som spammar
        Ja ingen kan slå våran bot
        """
    ]

    messages = [
        "Total kick!",
        "Jo det är nog bäst",
        "Totalt ur balans!",
        "Men varför?!!!",
        "Varför Anna?!",
        "OMG",
        "Varför",
        "Skicka en bild annars tror vi inte pä dig",
        "OMG hon löper amook!",
        "Va?!",
        "Skämtar du med mig?!",
        "Helt sjukt detta!!",
        "Vadä, sä du menar att du är en riktig tjo",
        "Varst vad boten ven"  # end of line truncated
    ]

    def on_welcome(self, c, e):
        c.join(self.channel)

        def tick():
            print("called tick")
            choices = [BassHunter.lyrics] + [BassHunter.messages] * 5
            source = random.choice(choices)

            if source == BassHunter.lyrics:
                for msg in [m.strip() for m in random.choice(source).split("\n") if len(m.strip()) > 0]:
                    c.privmsg(self.channel, msg)
            elif source == BassHunter.messages:
                msg = random.choice(source)
                c.privmsg(self.channel, msg)

            video_msg = "https://www.youtube.com/watch?v=RYQUsp-jxDQ"
            c.privmsg(self.channel, video_msg)

        interval = datetime.timedelta(hours=1)
        self.reactor.scheduler.execute_every(period=interval, func=tick)
        tick()




if __name__ == '__main__':
    creds = get_irc_credentials()

    server = creds["server"]
    port = int(creds["port"])
    channel = creds["channel"]
    server_password = creds["server_password"]
    nickname = creds["nickname"]

    import logging

    logging.basicConfig(level=logging.DEBUG)

    anna = Anna(server, port, channel, nickname, server_password)
    basshunter = BassHunter(server, port, channel, "BassHunter", server_password)


    def run_anna():
        anna.start()


    def run_basshunter():
        basshunter.start()


    try:
        tpe = ProcessPoolExecutor(max_workers=10)
        tpe.submit(run_anna)
        time.sleep(5)
        tpe.submit(run_basshunter)
    except KeyboardInterrupt:
        print("killed")
        anna.disconnect()
        basshunter.disconnect()
