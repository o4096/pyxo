import os
import platform
from functools import partial
import tkinter as tk
from tkinter import messagebox

EMPTY= 0
HUMAN= -1
AI=  1
algorithms=[
	'Minimax',
	'Minimax w/Alpha Beta',
	'Minimax w/Symmetry Reduction',
	'Hueristic 1',
	'Hueristic 2',
]

class Game():
	def __init__(self):
		self.algo= tk.StringVar(value=algorithms[2])
		self.start()

	def start(self):
		self.state= [[EMPTY, EMPTY, EMPTY] for _ in range(3)]

	def wins(self, player):
		win_state= [
			[self.state[0][0], self.state[0][1], self.state[0][2]],#top row
			[self.state[1][0], self.state[1][1], self.state[1][2]],#middle row
			[self.state[2][0], self.state[2][1], self.state[2][2]],#bottom row
			[self.state[0][0], self.state[1][0], self.state[2][0]],#left column
			[self.state[0][1], self.state[1][1], self.state[2][1]],#middle column
			[self.state[0][2], self.state[1][2], self.state[2][2]],#right column
			[self.state[0][0], self.state[1][1], self.state[2][2]],#main diagonal
			[self.state[2][0], self.state[1][1], self.state[0][2]],#other diagonal
		]
		return [player, player, player] in win_state
	
	def end(self):
		return self.wins(HUMAN) or self.wins(AI)
	
	def evaluation(self):#TODO inline this or something
		if self.wins(AI):
			return 1
		elif self.wins(HUMAN):
			return -1
		else:
			return 0

	def empty_cells(self):
		return [(y, x) for y in range(3) for x in range(3) if self.state[y][x]==EMPTY]
	
	def play(self, move:tuple, player=HUMAN):
		self.state[move[0]][move[1]]= player
		# if move in self.empty_cells():
		# 	self.state[move[0]][move[1]]= player
		# else:
		# 	print('I got here')#TODO test if this is even reachable otherwise inline this code
	
	def ai(self):
		depth= len(self.empty_cells())
		if depth==0 or self.end():
			return
		
		if   self.algo.get()=='Minimax':#TODO turn all of these into a single line
			move, _= self.minimax(depth)
		elif self.algo.get()=='Minimax w/Alpha Beta':
			move, _= self.minimax_abp(depth)
		elif self.algo.get()=='Minimax w/Symmetry Reduction':
			move, _= self.minimax_sr(depth)
		elif self.algo.get()=='Hueristic 1':
			move, _= self.heuristic1()
		elif self.algo.get()=='Hueristic 2':
			move= self.heuristic2()
		else:#this code is unreachable so long as self.algo is initialized
			messagebox.showinfo('ERROR', 'No Algorithm Selected')
			return

		self.play(move, AI)

	def minimax(self, depth, player=AI):
		best_move= None
		best_score= float('-inf') if player==AI else float('inf')
	
		if depth==0 or self.end():#base case
			return best_move, self.evaluation()

		for y, x in self.empty_cells():
			self.state[y][x]= player
			_, score= self.minimax(depth-1, -player)
			self.state[y][x]= EMPTY
			if(best_score<score if player==AI else best_score>score):#maximize ai, minimize player
				best_move= (y, x)
				best_score= score
		return best_move, best_score

	def minimax_abp(self, depth, player=AI, alpha=float('-inf'), beta=float('inf')):
		best_move= None
		best_score= float('-inf') if player==AI else float('inf')

		if depth==0 or self.end():#base case
			return best_move, self.evaluation()
		
		for y, x in self.empty_cells():
			self.state[y][x]= player
			_, score= self.minimax_abp(depth-1, -player, alpha, beta)
			self.state[y][x]= EMPTY
			if(best_score<score if player==AI else best_score>score):#maximize ai, minimize player
				best_move= (y, x)
				best_score= score
			if player==AI:
				alpha= max(alpha, best_score)
			else:
				beta= min(beta, best_score)
			if beta<=alpha:
				break
		return best_move, best_score

	def _get_symmetries(self, state):
		syms= [tuple(state)]

		for _ in range(3):#rotate 90, 180, 270 deg clockwise
			state= list(zip(*state[::-1]))#rotate 90 deg clockwise
			syms.append(state)
		# state= list(zip(*state[::-1]))#return back to original form (360)
		syms.append([row[::-1] for row in state])#horizontal flip
		syms.append(state[::-1])#vertical flip
		return tuple(syms)

	def _get_lexical_form(self, state):
		'''returns an in order string representation of board state'''
		return ''.join(str(cell) for row in state for cell in row)

	def _get_canonical_form(self, state):
		syms= self._get_symmetries(state)
		# return min(tuple(map(tuple, sym)) for sym in syms)
		return min(self._get_lexical_form(sym) for sym in syms)#return smallest lexical state

	def minimax_sr(self, depth, player=AI, checked:dict=None):
		best_move= None
		best_score= float('-inf') if player==AI else float('inf')
		if checked==None: checked= {}
		canonical= self._get_canonical_form(self.state)

		if canonical in checked.keys():#quick base case
			return best_move, checked[canonical]

		if depth==0 or self.end():#base case
			return best_move, self.evaluation()
		
		for y, x in self.empty_cells():
			self.state[y][x]= player
			_, score= self.minimax_sr(depth-1, -player, checked)
			self.state[y][x]= EMPTY
			if(best_score<score if player==AI else best_score>score):#maximize ai, minimize player
				best_move= (y, x)
				best_score= score
		checked[canonical]= best_score
		return best_move, best_score

	def heuristic1(self, depth=4, player=AI):#TODO test edge cases
		best_move= None
		best_score= float('-inf') if player==AI else float('inf')
	
		if   self.wins(AI):#heuristic evaluation
			return best_move, 10
		elif self.wins(HUMAN):
			return best_move, -10
		if depth==0:
			return best_move, 0

		for y, x in self.empty_cells():
			self.state[y][x]= player
			_, score= self.heuristic1(depth-1, -player)
			self.state[y][x]= EMPTY
			if(best_score<score if player==AI else best_score>score):#maximize ai, minimize player
				best_move= (y, x)
				best_score= score
		return best_move, best_score

	def heuristic2(self):
		best_score = -float('inf')
		best_move = None

		for y, x in self.empty_cells():
			self.state[y][x] = AI
			score = self.evaluate_position(y, x)
			self.state[y][x] = EMPTY

			if score > best_score:
				best_score = score
				best_move = (y, x)

		return best_move

	def evaluate_position(self, y, x):
		score = 0
		weights = [3, 2, 1]

		for line in self.get_win_lines():
			if (y, x) in line:
				comp_count = 0
				human_count = 0
				for i, j in line:
					if self.state[i][j] == AI:
						comp_count += 1
					elif self.state[i][j] == HUMAN:
						human_count += 1

				if comp_count > 0 and human_count == 0:
					score += weights[comp_count - 1]
				elif human_count > 0 and comp_count == 0:
					score -= weights[human_count - 1]

		return score
	def get_win_lines(self):
		# Define the lines representing possible wins
		return [
			# Rows
			[(0, 0), (0, 1), (0, 2)],
			[(1, 0), (1, 1), (1, 2)],
			[(2, 0), (2, 1), (2, 2)],
			# Columns
			[(0, 0), (1, 0), (2, 0)],
			[(0, 1), (1, 1), (2, 1)],
			[(0, 2), (1, 2), (2, 2)],
			# Diagonals
			[(0, 0), (1, 1), (2, 2)],
			[(0, 2), (1, 1), (2, 0)],
		]

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
		bg= self.get_theme('bg')
		self.root.config(bg=bg)
		self.buttons= [[tk.Button(self.root, font=('Helvetica', 20), width=4, height=2) for _ in range(3)] for _ in range(3)]
		self.game= Game()
		
		mb= tk.Menu(self.root)
		
		mb_game= tk.Menu(mb, tearoff=False)
		mb_game.add_command(label='New Game', command=self.new_game)
		mb_game.add_command(label='Exit',     command=partial(exit, 0))

		mb_algo= tk.Menu(mb, tearoff=False)

		for algo in algorithms:
			mb_algo.add_radiobutton(label=algo, variable=self.game.algo, value=algo)

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
			self.game.ai()
		self.gui_render()

	def gui_render(self):
		for i in range(3):
			for j in range(3):
				if self.game.state[i][j]==HUMAN:
					sym= 'X'
				elif self.game.state[i][j]==AI:
					sym='O'
				else:
					sym=''
				self.buttons[i][j].config(text=sym, state='active' if sym=='' else 'disabled')

		# self.cmd_clear()
		# self.cmd_printState()

	def gui_click(self, btn: tk.Button):
		move= btn.grid_info()['row'], btn.grid_info()['column']
		self.game.play(move)
		self.gui_render()
		if self.game.end():
			messagebox.showinfo('Game Over', 'You Win!')
			self.start()
			return
		
		self.game.ai()
		self.gui_render()
		if self.game.end():
			messagebox.showinfo('Game Over', 'You Lose!')
			self.start()
			return
		
		elif not self.game.empty_cells():
			messagebox.showinfo('Game Over', 'Tie!')
			self.start()
			return

	def new_game(self):
		if messagebox.askyesno('New Game', 'Are you sure you want to start a new game?'):
			self.start()

	def about(self):
		messagebox.showinfo('Tic-Tac-Toe', 'AI project, Helwan University 2024')
	
	def get_theme(self, element:str):
		return self.themes[self.darkmode][element]
	
	def toggle_darkmode(self):
		self.darkmode= not self.darkmode
		bg= self.get_theme('bg')
		fg= self.get_theme('fg')
		self.root.config(background=bg, bg=bg)
		for i in range(3):
			for j in range(3):
				self.buttons[i][j].config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg, disabledforeground=fg)

	def cmd_clear(self):
		os.system('cls' if platform.system()=='Windows' else 'clear')
	
	def cmd_printState(self):#TODO
		for i in range(3):
			for j in range(3):
				if self.game.state[i][j]==HUMAN:
					sym= 'X'
				elif self.game.state[i][j]==AI:
					sym='O'
				else:
					sym=''
				print(sym)

if __name__=='__main__':
	app= Application()
	app.start()
	tk.mainloop()