import platform
import os
import math
from functools import partial
import tkinter as tk
from tkinter import messagebox

EMPTY= 0
HUMAN= -1
COMP=  1

USE_MINIMAX=    0
USE_HUERISTIC1= 1
USE_HUERISTIC2= 2
USE_ALPHA_BETA= 3
USE_SYMMETRY=   4

class Game():
	def __init__(self):
		# self.use_alpha_beta_pruning= tk.BooleanVar(value=False)
		# self.use_symmetry_reduction= tk.BooleanVar(value=False)
		# self.use_minimax= tk.BooleanVar(value=False)
		# self.use_Heuristic1= tk.BooleanVar(value=False)
		# self.use_Heuristic2= tk.BooleanVar(value=False)

		self.algo= tk.IntVar(value=USE_MINIMAX)
		self.start()

	def minimax(self, depth, player):
		best= [-1, -1, -math.inf if player==COMP else math.inf]
	
		if depth==0 or self.end(): #leaves
			score= self.evaluate()
			return [-1, -1, score]

		for cell in self.empty_cells():
			x, y= cell[0], cell[1]
			self.state[x][y]= player
			score= self.minimax(depth-1, -player)
			self.state[x][y]= 0
			score[0], score[1]= x, y
			if player==COMP:
				if score[2]>best[2]:
					best= score #max value
			else:
				if score[2]<best[2]:
					best= score #min value
		return best

	def minimax_alpha_beta(self, depth, alpha, beta, player):
		best = [-1, -1, -math.inf if player == COMP else math.inf]

		if depth == 0 or self.end():  # Leaf node
			score = self.evaluate()
			return [-1, -1, score]

		for cell in self.empty_cells():
			x, y = cell
			self.state[x][y] = player
			score = self.minimax_alpha_beta(depth - 1, alpha, beta, -player)
			self.state[x][y] = 0
			score[0], score[1] = x, y

			if player == COMP:  # Maximize AI
				if score[2] > best[2]:
					best = score
				alpha = max(alpha, score[2])
			else:  # Minimize Human
				if score[2] < best[2]:
					best = score
				beta = min(beta, score[2])

			if beta <= alpha:  # Prune remaining branches
				break
		return best

	def canonical_form(self, state):
		"""
		Generate the canonical form of the board state.
		Find the lexicographically smallest form among rotations and reflections.
		"""
		transformations = [state]

		# Generate rotations (90, 180, 270 degrees)
		for _ in range(3):
			state = list(zip(*state[::-1]))  # Rotate 90 degrees clockwise
			transformations.append(state)

		# Reflect horizontally
		reflected = [row[::-1] for row in state]
		transformations.append(reflected)

		# Reflect vertically
		reflected = state[::-1]
		transformations.append(reflected)

		# Return the lexicographically smallest state
		return min(transformations, key=lambda s: str(s))
	
	def heuristic1(self):
		"""Basic heuristic: Count potential winning lines."""
		score = 0
		for line in self.get_win_lines():
			if line.count(COMP) > 0 and line.count(HUMAN) == 0:
				score += 1
			if line.count(HUMAN) > 0 and line.count(COMP) == 0:
				score -= 1
		return score

	def heuristic2(self):
		"""Advanced heuristic: Weighted evaluation of game state."""
		score = 0
		weights = [3, 2, 1]  # Example weights for positions closer to forming lines
		for line in self.get_win_lines():
			if line.count(COMP) > 0 and line.count(HUMAN) == 0:
				score += weights[line.count(COMP) - 1]
			if line.count(HUMAN) > 0 and line.count(COMP) == 0:
				score -= weights[line.count(HUMAN) - 1]
		return score

	def start(self):
		self.state= [[0,0,0] for _ in range(3)]

	def empty_cells(self):
		return [[i, j] for i, row in enumerate(self.state)
			for j, cell in enumerate(row)
			if cell==EMPTY]

	def evaluate(self):
		if self.wins(COMP):
			return 1
		elif self.wins(HUMAN):
			return -1
		else:
			return 0

	def wins(self, player):
		win_state= [
			[self.state[0][0], self.state[0][1], self.state[0][2]],  # [1,-1,0]
			[self.state[1][0], self.state[1][1], self.state[1][2]],  # [0  -1  1]
			[self.state[2][0], self.state[2][1], self.state[2][2]],  # [-1 -1  0]
			[self.state[0][0], self.state[1][0], self.state[2][0]],  # [1 0 1]
			[self.state[0][1], self.state[1][1], self.state[2][1]],  # [-1 -1 -1]
			[self.state[0][2], self.state[1][2], self.state[2][2]],  # [0 1 0]
			[self.state[0][0], self.state[1][1], self.state[2][2]],  # [1 -1 0]
			[self.state[2][0], self.state[1][1], self.state[0][2]],  # [0 -1 -1]
		]
		return [player, player, player] in win_state
	
	def end(self):
		return self.wins(HUMAN) or self.wins(COMP)
	
	def input_ai(self):
		depth= len(self.empty_cells())
		if depth==0 or self.end():
			return
		
		if   self.algo==USE_MINIMAX:
			move= self.minimax(depth, COMP)
			print('using minimax')
		elif self.algo==USE_HUERISTIC1:
			move= self.heuristic1()
			print('using hueristic1')
		elif self.algo==USE_HUERISTIC2:
			move= self.heuristic2()
			print('using hueristic2')
		elif self.algo==USE_ALPHA_BETA:
			move= self.minimax_alpha_beta(depth, -math.inf, math.inf, COMP)
			print('using alpha beta')
		elif self.algo==USE_SYMMETRY:
			move= self.minimax_symmetry_reduction(depth, COMP)
			print('using symmetry')

		else:
			messagebox.showinfo('ERROR', 'No Algorithm Selected')
			return

		x, y= move[0], move[1]
		self.state[x][y]= COMP

	def input_human(self, x, y):
		if [x, y] in self.empty_cells():
			self.state[x][y]= HUMAN
		else:
			print('I got here')#TODO test if this is even reachable otherwise inline this code

class Application():
	def __init__(self):
		self.root= tk.Tk()
		self.root.title('Tic-Tac-Toe')
		self.root.geometry('400x400')
		self.darkmode= True
		self.themes= [
			{#dark mode is OFF
				'bg': '#CCCCCC',
				'fg': '#000000',
			},
			{#dark mode is ON
				'bg': '#222222',
				'fg': '#EEEEEE',
			},
		]
		bg= self.get_theme()['bg']
		fg= self.get_theme()['fg']
		self.root.config(bg=bg)
		self.buttons= [[tk.Button(self.root, font=('Helvetica', 20), width=4, height=2) for _ in range(3)] for _ in range(3)]
		self.game= Game()
		
		mb= tk.Menu(self.root)
		
		mb_game= tk.Menu(mb, tearoff=False)
		mb_game.add_command(label='New Game', command=self.new_game)
		mb_game.add_command(label='Exit',     command=partial(exit, 0))

		mb_algo= tk.Menu(mb, tearoff=False)


		mb_algo.add_radiobutton(label='MiniMax',            variable=self.game.algo, value=0)
		mb_algo.add_radiobutton(label='Heuristic 1',        variable=self.game.algo, value=1)
		mb_algo.add_radiobutton(label='Heuristic 2',        variable=self.game.algo, value=2)
		mb_algo.add_radiobutton(label='Alpha-Beta Pruning', variable=self.game.algo, value=3)
		mb_algo.add_radiobutton(label='Symmetry Reduction', variable=self.game.algo, value=4)
		#TODO

		mb_view= tk.Menu(mb, tearoff=False)
		mb_view.add_checkbutton(label='Dark Mode', command=self.toggle_darkmode)

		mb_help= tk.Menu(mb, tearoff=False)
		mb_help.add_command(label="About", command=self.about)

		mb.add_cascade(menu=mb_game, label='Game')
		mb.add_cascade(menu=mb_algo, label='Algorithm')
		# mb.add_cascade(menu=mb_opti, label='Optimizations')
		mb.add_cascade(menu=mb_help, label='Help')
		mb.add_cascade(menu=mb_view, label='View')
		self.root.config(menu=mb)

		# frame= tk.Frame(self.root, background='#f0f0f0')
		# frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

		for i in range(3):
			for j in range(3):
				self.buttons[i][j].grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
				self.buttons[i][j].config(command=partial(self.gui_click, self.buttons[i][j]))
	
		# Configure grid weights to allow resizing
		for i in range(3):
			self.root.grid_rowconfigure(i, weight=1)#Allow rows to expand
		for j in range(3):
			self.root.grid_columnconfigure(j, weight=1)#Allow columns to expand

		self.root.pack_propagate(True)
		self.toggle_darkmode()

	def start(self):
		self.game.start()
		if not messagebox.askyesno('New Game', 'Would you like to go first?'):
			self.game.input_ai()
		self.gui_render()

	def gui_render(self):
		for i in range(3):
			for j in range(3):
				if self.game.state[i][j]==HUMAN:
					sym= 'X'
				elif self.game.state[i][j]==COMP:
					sym='O'
				else:
					sym=''
				self.buttons[i][j].config(text=sym, state='active' if sym=='' else 'disabled')

	def gui_click(self, btn: tk.Button):
		x, y= btn.grid_info()['row'], btn.grid_info()['column']

		self.game.input_human(x, y)
		self.gui_render()
		if self.game.end():
			if messagebox.askyesno('Game Over', 'You Win!\nWould you like to go again?'):
				self.start()
			return
		
		self.game.input_ai()
		self.gui_render()
		if self.game.end():
			if messagebox.askyesno('Game Over', 'You Lose!\nWould you like to go again?'):
				self.start()
			return
		
		elif not self.game.empty_cells():
			if messagebox.askyesno('Game Over', 'Tie!\nWould you like to go again?'):
				self.start()
			return

	def new_game(self):
		if messagebox.askyesno('New Game', 'Are you sure you want to start a new game?'):
			self.start()

	def about(self):
		messagebox.showinfo('Tic-Tac-Toe', 'AI project, Helwan University 2024')
	
	def get_theme(self):
		return self.themes[self.darkmode]
	
	def toggle_darkmode(self):
		self.darkmode= not self.darkmode
		bg= self.get_theme()['bg']
		fg= self.get_theme()['fg']
		self.root.config(background=bg, bg=bg)
		for i in range(3):
			for j in range(3):
				self.buttons[i][j].config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg, disabledforeground=fg)

	# def cmd_clear(self):
	# 	os.system('cls' if platform.system()=='Windows' else 'clear')

if __name__=='__main__':
	app= Application()
	app.start()
	tk.mainloop()
