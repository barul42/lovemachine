#!/usr/bin/python
# -*- coding: utf8 -*-
 
import irclib
import ircbot
import re
import hashlib 
import random
import os

class BotModeration(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)],"Lovemachine", "pour barul et les autres")
 
    def on_welcome(self, serv, ev):

	self.citations = []

	with open("citfinal") as fichier:
		for ligne in fichier:
			self.citations.append(ligne)


        serv.join("##lovemachinearch")
 
    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0] 

	if re.search("^!help", message):
		serv.privmsg(auteur,"!imdb FILM : Affiche la note du film FILM sur imdb.com")
		serv.privmsg(auteur,"!love TRUC,MACHIN : Affiche la compatibilité amoureuse entre TRUC et MACHIN")
		serv.privmsg(auteur,"!pof [MESSAGE] : Tire à pile ou face")
		serv.privmsg(auteur,"!8ball [QUESTION] : Répond à la question")
		serv.privmsg(auteur,"!cita : Affiche une citation")


	if re.search("^!imdb ", message):
		film = message[6:]
		resultat = os.popen("bash /home/biganon/imdb \""+film+"\"").read()
		serv.privmsg(canal, resultat)

	if re.search("^!love .+,.+", message):
		message = re.sub(" *, *",",",message)
		tab = message[6:].split(",")
		nom1 = tab[0].lower()
		nom2 = tab[1].lower()
		liste=sorted([nom1, nom2])
		chaine=liste[0]+" "+liste[1]
		hachis=int(hashlib.md5(chaine).hexdigest(),16)
		serv.privmsg(canal, str(hachis % 101)+" % de compatibilité amoureuse entre "+tab[0]+" et "+tab[1]+" !")

	if re.search("^!pof", message):
		if random.randint(0,1) == 0:
			serv.privmsg(canal, auteur+": Pile !")
		else:
			serv.privmsg(canal, auteur+": Face !")

	if re.search("^!8ball", message):
		reponse = ["à coup sûr","sans aucun doute","je crois bien","c'est fort probable","oui","n'y compte pas","non","il semble que non","on dirait bien que non","j'en doute fortement"][random.randint(0,9)]
		serv.privmsg(canal, auteur+": "+reponse)
	
	if re.search("^!rimshot", message):
		serv.privmsg(canal, "PADAM TCH")

	if re.search("^!cita( |$)",message):
		if len(message) > 7:
			motcle = message[6:]
			tabCitations = [ citation for citation in self.citations if re.search("\\b"+motcle+"\\b",citation,re.I) ]
		else:
			tabCitations = self.citations

		try:
			has = random.randint(0,len(tabCitations)-1)
			sortie = tabCitations[has]
			serv.privmsg(canal,auteur+": "+sortie)
		except (IndexError,ValueError) :
			serv.privmsg(canal,auteur+": aucune citation trouvée.")
		


    def on_privmsg(self, serv, ev):
	if irclib.nm_to_n(ev.source()) == "Biganon":
		serv.privmsg("##lovemachinearch", ev.arguments()[0])

		
 
if __name__ == "__main__":
    BotModeration().start()
