import random
#0scissors 1rock 2paper

i=0
while i<5:
#1.define 2 variable

	#player
	playerInput = input("Please input (0scissors 1rock 2paper): ")

	player = int(playerInput)

	#computer
	computer = random.randint(0,2)

	#2.judge
	if (player==0 and computer==2) or (player==1 and computer==0) or (player==2 and computer==1) :
		#win
		print("win, happy!")
	elif player==computer :
		#draw
		print("draw, another game?")
	else:
		#lose
		print("lose, keep fighting till dawn")
	i+=1
