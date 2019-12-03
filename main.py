import tkinter as tk
from tkinter import *
from os import listdir
from os.path import isfile, join
from PIL import Image
from random import randint
import os, tempfile, cv2, time
import sys, webbrowser, shutil ,random, pyttsx3, threading
import json, ctypes, subprocess, pythoncom, subprocess, re
import base64, urllib, requests

global speechdatabase, proclist
print("Sorry for the shit log output in advance. I'll clean this up asap")

try:
	with open('config.ini') as data_file:
		configsetting = json.load(data_file)
	ctypes.windll.user32.MessageBoxW(0, "Welcome back to SkahdiBuddy!\nPlease note that SkahdiBuddy takes a moment to boot up. We're working on improving the boot time.", "SkahdiBuddy v1", 0)
except:
	configsetting={}
	configsetting['walkdelay'] = 0.02
	configsetting['thinkdelay'] = 0.001
	configsetting['sleepdelay'] = 0.1
	configsetting['talkdelay'] = 0.1
	configsetting['speech'] = {}
	configsetting['speech']['wordsperminute'] = 120
	configsetting['speech']['speechvolume'] = 0.9
	configsetting['speech_db'] = {}
	configsetting['speech_db']['update'] = True
	configsetting['speech_db']['encrypt_key'] = 'sbv1'
	configsetting['speech_db']['link'] = 'w5vDlsOqwqHDpsKcwqVgw6rDmcOtX8OXw5TDpcKhw5XDkcOuX8OWw5HDo2DDpsKRwqvCp8Olw5XDqMKiwqnDg8OmZcOYw5jCrsKTw5XCkcOJfcK5wpDDqsKpw6fCocOawp3CsMKT'
	j = json.dumps(configsetting, indent=4)
	f = open('config.ini', 'w')
	print(j, end="", file=f)
	f.close()
	ctypes.windll.user32.MessageBoxW(0, "Welcome to SkahdiBuddy V1.\nThis is either your very first time using me, or you messed up my config file.\nNo matter! I'll make a new one real quick!\nPlease note that SkahdiBuddy takes a moment to boot up. We're working on improving the boot time.", "Mew! SkahdiBuddy v1", 0)

def updateprocesses():
	procs = subprocess.check_output(['tasklist'], shell=True)
	procs = re.split('\s+',str(procs))
	proclist = []
	for x in procs:
		if ".exe" in x:
			proclist.append(x.replace("K\\r\\n","").lower())
	updateprocesses.proclist = list(set(proclist))	
	return proclist


## download speech data library and load it into the db
## decode and encode stolen from https://stackoverflow.com/a/38223403
## - thanks, Ryan Barrett
## PS. I think this entire decode/encode thing is really unnecessary. But ya'll asked for it in the group 
## because ya'll didn't want any speech spoilers. so this one is for you.
## PPS. speechdb.sbuddy is not encoded _yet_, sorry. We're getting there.
def update(speechlibrarylink):
	link = speechlibrarylink
	openlink = urllib.request.urlopen(link).read()
	openlink = openlink.decode()
	speechlines = openlink
	#print(speechlines)
	speechlines = speechlines.split('\r\n\r\n')
	speechdatabase = {}
	
	for x in speechlines:
		program = x.replace("\r","").split('\n',1)[0]
		comebacks = x.replace("\r","").split('\n',1)[1].split("\n")
		speechdatabase[program]={}
		speechdatabase[program]['comebacks']=comebacks
		
	j = json.dumps(speechdatabase, indent=4)
	f = open('speechdb.sbuddy', 'w')
	print(j, end = "", file = f)
	f.close()
	print("wrote.")
	#print(librarydecoded)

def decode(key, enc):
	dec = []
	enc = base64.urlsafe_b64decode(enc).decode()
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	speechlibrarylink = ("".join(dec))
	update(speechlibrarylink)

def encode(key, clear):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	print(base64.urlsafe_b64encode("".join(enc).encode()).decode())

#encode(configsetting['speech_db']['encrypt_key'], "https://www.dropbox.com/s/5vrsrq6ap4ev8bb/SLF.txt?dl=1")


if configsetting['speech_db']['update'] == True:
	print("Updating speech library...")
	try:
		decencstr = configsetting['speech_db']['link']
		encrypt_key = configsetting['speech_db']['encrypt_key']
		decode(encrypt_key, decencstr)
		try:
			with open('speechdb.sbuddy') as data_file:
				speechdatabase = json.load(data_file)
		except:
			ctypes.windll.user32.MessageBoxW(0, "Sorry for bothering, but I kinda need an internet connection right now.\n\nI'm trying to download the speech databasis, cos it doesn't exist on your local storage.", "SkahdiBuddy v1", 0)
			sys.exit()
	except:
		...

		
if configsetting['speech_db']['update'] == False:
	try:
		with open('speechdb.sbuddy') as data_file:
			speechdatabase = json.load(data_file)
	except:
		ctypes.windll.user32.MessageBoxW(0, "Sorry for bothering, but I kinda need an internet connection right now.\n\nI'm trying to download the speech databasis, cos it doesn't exist on your local storage.", "SkahdiBuddy v1", 0)
		sys.exit()



spritepath = "./sprites"
onlyfiles = [f for f in listdir(spritepath) if isfile(join(spritepath, f))]
print("Extracting Animations...")

if os.path.exists("./anims"): shutil.rmtree("./anims")

for x in onlyfiles:

	#print(onlyfiles)
	animation_name = x.split("!")[0]
	im = cv2.imread(spritepath+"/"+x)
	#print(animation_name)
	#print(animation_name)
	#print(animation_name)
	
	if not os.path.exists("./anims"): 
		os.mkdir("./anims")
		#print("made animation folder")
	
	if not os.path.exists("./anims/"+animation_name): 
		os.mkdir("./anims/"+animation_name)
		#print("made animation name")
	
	if not os.path.exists("./anims/"+animation_name+"/left"): 
		os.mkdir("./anims/"+animation_name+"/left")
		#print("made animation name / left")
	
	
	if not os.path.exists("./anims/"+animation_name+"/right"): 
		os.mkdir("./anims/"+animation_name+"/right")
		#print("made animation name / right")

	shape_height=(im.shape)[0]
	shape_width=(im.shape)[1]
	blocks = x.split("!")[1]
	
	#print(str(shape_height), str(shape_width), str(blocks), "=", str(int(shape_width)/int(blocks)))
	
	equs = int(shape_width)/int(blocks)
	
	imageObject = Image.open(spritepath+"/"+x)
	## ----------------------------------------------------------------

	#print("Stripping sprites from tilesets...")
	size=(100,100)

	for direction in range(0,1):
		for y in range(1,int(blocks)+1):
			direction = "right"
			#print("BLOCKS: ", blocks)
			#print(equs*y)
			cropped = imageObject.crop((round(equs*y)-equs-1, 0,  round(equs*y), shape_height))
			#cropped.save(x+str(y)+".png")
			cropped = cropped.resize(size)
			cropped.save("./anims/"+animation_name+"/"+direction+"/"+str(y)+".png")

		for y in range(1,int(blocks)+1):
			direction = "left"
			#print("BLOCKS: ", blocks)
			#print(equs*y)
			cropped = imageObject.crop((round(equs*y)-equs-1, 0,  round(equs*y), shape_height))
			cropped = cropped.transpose(Image.FLIP_LEFT_RIGHT)
			cropped = cropped.resize(size)
			cropped.save("./anims/"+animation_name+"/"+direction+"/"+str(y)+".png")

	## ----------------------------------------------------------------

print("Spawning SkahdiBuddy...")
root = tk.Tk()
root.overrideredirect(True)# Make window invisible
root.wm_attributes("-topmost", True)# Keep skahdi on top even after min
root.wm_attributes("-transparentcolor", "white")
direction = 'right'
char_position = "+10+627"
root.geometry(char_position)

updateprocesses()
proclist = (updateprocesses.proclist)

def popupmenu(event):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()

def idleloop(char_position, direction, proclist):
	"""
	Idle loop spawns the cat at bottom left.
	"""
	#print("IDLE ANIMATION", char_position)
	global talkvar
	talkvar = False
	count=0
	DIR = "./anims" + '/sprite_thinking/' +direction+"/"
	countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
	nextmove = randint(0,100)
	#nextmove = 40
	nextmove_start = 0
	play_animation = 0
	## play_animation
	## 0 - pause/sleep
	## 1 - play/think
	## 2 - talk
	walkspeed = configsetting['walkdelay']
	talkloops = 5 ## this var runs the talking animation for 5 loops before it returns back to the idle animation
	talknumber = 0
	while 1: #loop for idle animation
		DIR = "./anims" + '/sprite_thinking/' +direction+"/"
		countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		delay = configsetting['thinkdelay']
	
		if play_animation == 0:
			DIR = "./anims" + '/sprite_thinking/' +direction+"/"
			countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
			delay = configsetting['thinkdelay']
			
		if play_animation == 1:		
			DIR = "./anims" + '/sprite_sleeping/' +direction+"/"
			countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
			delay = configsetting['sleepdelay']
		
		if play_animation == 2:
			DIR = "./anims" + '/sprite_talking/' + direction + '/'
			countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
			delay = configsetting['talkdelay']
			talknumber = talknumber + 1
			if talknumber==talkloops:
				talknumber = 0
				talkvar = False ## end the talk animation
			
		#print(pausevar)
		
		if count == countmax:
			#updateproc = threading.Thread(target=updateprocesses)
			#updateproc.daemon = True
			#updateproc.start()
			count = 0
		count = count+1
		
		#print(nextmove_start, nextmove)
		## This block decides the character's next move
		if nextmove_start==nextmove:
			nextmove = randint(40,100)
			play_animation = randint(3,20)
			#print("PLAYANIMATION",play_animation)
			nextmove_start = 0
			#play_animation = 1
			
			## Base Animations
			##  - walk
			##  - talk
			##  - idle
			
			if pausevar == True:
				play_animation = 1
				
			if talkvar == True:
				play_animation = 2

			
			if 3 <= play_animation <= 14: ## Walk!
				walk_range = randint(10,200)
				direction = random.choice(['left','right'])
				print("Walking "+direction)
				lr_block = int(char_position.split("+")[1])  ## Left - Right
				ud_block = int(char_position.split("+")[-1]) ## Up - Down
				## Now load the animation files
				DIR = "./anims" + '/sprite_walking/' + direction + '/'
				count = 0
				countmax = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
				stepjump = lr_block
				for steps in range(1,int(walk_range)):
					
					## stepjump max = 1340
					## stepjump min = 0
					
					if stepjump>=1345:
						stepjump=-80
					if stepjump<=-100:
						stepjump=1340
						
					if direction=="left":
						stepjump=stepjump-5
					if direction=="right":
						stepjump=stepjump+5
					
					if count==countmax:
						count=0
					count=count+1
					#increment by 5. Always
					char_position = "+"+str(stepjump)+"+"+str(ud_block)
					root.geometry(char_position)
					root.image = tk.PhotoImage(file=DIR+str(count)+'.png')
					skahlabel = tk.Label(root, image=root.image, bg='white')
					skahlabel.pack(side="bottom")
					root.update()
					skahlabel.destroy()
					root.update_idletasks()
					time.sleep(walkspeed)
					

			if 15 <= play_animation <= 20:
				print("talking "+direction+" "+str(talkvar))
				if talkvar == True:
					pass
				elif talkvar == False:
					print("I should be talking -",direction)
					talkvar = True ## this makes skahdi speak. please set to false when done speaking.
					## speech thread here.
					updateprocesses()
					proclist = (updateprocesses.proclist)
					print("Items in process list",len(proclist))
					speak = threading.Thread(target=saysomething, args=(char_position,proclist,))
					speak.daemon = True
					speak.start()
					## speech thread end
			
			#if play_animation==1: ## 1 is always pause.
			#	playpause = 1
				
			#if play_animation!=1:
			#	playpause = 0

			#	## pause animation here
			#	...
			
		try:		
			nextmove_start+=1
			root.geometry(char_position)
			root.image = tk.PhotoImage(file=DIR+str(count)+'.png')
			skahlabel = tk.Label(root, image=root.image, bg='white')
			skahlabel.pack(side="bottom")
			root.bind("<Button-3>", popupmenu)
			root.update()
			skahlabel.destroy()
			root.update_idletasks()
			time.sleep(delay) # Time module delay
		except:
			count=0

def saysomething(char_position,proclist):
	global bubble, speechbubble, lastprocess
	print("I'm talking")
	
	try:
		bubble.destroy()
		#speechbubble.destroy()
	except Exception as e:
		...
	
	print("booting blocks")
	lr_block = int(char_position.split("+")[1])  ## Left - Right
	ud_block = int(char_position.split("+")[-1]) ## Up - Down
	print("Spawning new tk bubble")
	
	## this block needs to run once, then never again...
	try:
		print(bubble)
		bubble.destroy()
		T.destroy()
	except:
		bubble = tk.Tk()
		print("tk.tk set")
		bubble.config(background = "white")
		bubble.overrideredirect(True)# Make window invisible
		bubble.wm_attributes("-topmost", True)# Keep skahdi on top even after min
	
	print("bubble spawned")
	#bubble.wm_attributes("-transparentcolor", "white")
	bubbleposition = "+"+str(lr_block)+"+"+str(ud_block-randint(50,300))
	bubble.geometry(bubbleposition)	
	print("bubble geometry set")
	
	## check for matching processes
	for proc in speechdatabase.keys():
		try:
			if proc.lower() in proclist:
				print("I FOUND "+proc)
				selectedcomeback = random.choice(speechdatabase[proc]['comebacks'])
				T = tk.Text(bubble, height=1, width = len(selectedcomeback), fg = "black", bg = "white")
				T.configure(relief = GROOVE, font=("Courier", 15))
				T.pack()
				T.insert(tk.END, selectedcomeback)
				T.configure(state = "disabled")
				bubble.update()
				bubble.update_idletasks()
				print(selectedcomeback)
				break
		except Exception as errormsg:
			print("-->",errormsg)
			
	try:
		## text width is equal to number of letters in comeback
		engine = pyttsx3.init()
		engine.setProperty('rate',configsetting['speech']['wordsperminute']) # wordsperminute
		engine.setProperty('volume',configsetting['speech']['speechvolume']) # speechvolume
		engine.say(selectedcomeback)
		engine.runAndWait()

		print("Reached the mainloop")
	except:
		print("--> I don't think I found any processes")
		pass
	
def save_config():
	j = json.dumps(configsetting, indent=4)
	f = open('config.ini', 'w')
	print(j, end="", file=f)
	f.close()
	print("Database Updated")
	
def openkofi():
	webbrowser.open('https://ko-fi.com/snepdev', new=2)
	
def exitskahdi():
	root.destroy()

def hibernate():
	global pausevar
	print("hibenate called")
	try:
		if pausevar==True: pausevar=False
		elif pausevar==False: pausevar=True
	except Exception as e:
		print("Loading pause script")
		pausevar = False
	print("Pause Skahd?",str(pausevar))
	
	if pausevar == True:
		count = 0
		while pausevar == True:
			break

popup = Menu(root, tearoff=1, title="SB (0.1)", relief=RAISED)
#popup.add_command(label="Tell me a joke")
popup.add_separator()
popup.add_command(label="❤-Donate-❤", command=openkofi)
popup.add_command(label="Pause/Play", command=hibernate)
popup.add_command(label="Exit", command=exitskahdi)
hibernate() ## load pausevar

print("Done!")
idleloop(char_position, direction, proclist)
