I strongly recomend running this program on IDE.

Because certain characters ("♠","♥","♦","♣") in the output might be printed out of place.

if you want to run in terminal:
	python3 main.py
	

Program Args:

starting from line 384:
	see_AI = 1       see AI hand                          0 off - 1 on 
	
	simulation = 0   AI plays against random card player  0 off - 1 on
	
	game_count = 1000  how many games you want to simulate


You can tweek this parameters to play the game with AI or to simulate win percentage of this algorithm against someone who plays random cards. Current algorithm can win %75-85 of the matches.

Also if you want to see the AI hand it's possible to do so with setting see_AI param to 1.



How to play:
	
	Depending on how many cards you have type 1-4 and you will play the "n"th card in your hand.
	
AI	? ? ? 
	♣Q 
YOU	♣9 ♠5 ♠10 
	------------------
	Enter a number between 1 and 3: 2  ENTERED 2 which mean you will play the 2nd card in your hand
AI	You played: ♠5
	? ? ? 
	♠5 
YOU	♣9 ♠10



Certain rules:
1)	You can only do pisti if there is ONLY 1 card on the table

2)	Pisti will count as 10 points everytime (Not 20 in certain scenarios)


***
Turns will be saved as tur{n th turn}.txt
***
