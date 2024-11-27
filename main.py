import platform
import os
import math
from functools import partial
import tkinter as tk
from tkinter import messagebox

EMPTY= 0
HUMAN= -1
COMP=  1

class Game():
	def __init__(self):
		self.use_alpha_beta_pruning= tk.BooleanVar()
		self.use_symmetry_reduction= tk.BooleanVar()
		self.use_minimax= tk.BooleanVar()
		self.use_Heuristic1= tk.BooleanVar()
		self.use_Heuristic2= tk.BooleanVar()
		# self.plr_turn= 0
		self.start()

	def minimax_symmetry_reduction(state, depth, player):
		pass #TODO
	# 	state = canonical_form(state)  # Use canonical form for state

	# 	if game_over(state):
	# 		return evaluate(state), None

	# 	if depth == 0:
	# 		return evaluate(state), None

	# 	best = None
	# 	if player == +1:  # AI's turn (maximize)
	# 		value = -float('inf')
	# 		for x, y in empty_cells(state):
	# 			new_state = copy.deepcopy(state)
	# 			set_move(x, y, player, new_state)
	# 			score,  = minimax(newstate, depth - 1, -player)
	# 			if score > value:
	# 				value, best = score, (x, y)
	# 	else:  # Human's turn (minimize)
	# 		value = float('inf')
	# 		for x, y in empty_cells(state):
	# 			new_state = copy.deepcopy(state)
	# 			set_move(x, y, player, new_state)
	# 			score,  = minimax(newstate, depth - 1, -player)
	# 			if score < value:
	# 				value, best = score, (x, y)
	# 	return value, best

	# def canonical_form(state):
	# 	"""
	# 	Find the canonical form of the board state by considering all rotations
	# 	and reflections, and returning the lexicographically smallest form.
	# 	"""
	# 	transformations = [state]

	# 	#Generate rotations
	# 	for _ in range(3):
	# 		state = rotate90(state)
	# 		transformations.append(state)

	# 	#Reflect the original state and rotated states
	# 	state_reflected = reflect_horizontal(state)
	# 	transformations.append(state_reflected)
	# 	for _ in range(3):
	# 		state_reflected = rotate_90(state_reflected)
	# 		transformations.append(state_reflected)

	# 	#Return the lexicographically smallest state
	# 	return min(transformations, key=lambda s: str(s))

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
	def minimax_alpha_beta(self):
		pass#TODO
	
	def heuristic1(self, state):
		"""Basic heuristic: Count potential winning lines."""
		score = 0
		for line in self.get_win_lines():
			if line.count(COMP) > 0 and line.count(HUMAN) == 0:
				score += 1
			if line.count(HUMAN) > 0 and line.count(COMP) == 0:
				score -= 1
		return score

	def heuristic2(self, state):
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
		if self.use_minimax.get():
			move= self.minimax(depth, COMP)
		elif self.use_symmetry_reduction.get():
			move= self.minimax_symmetry_reduction(depth, COMP)
		elif self.use_alpha_beta_pruning.get():
			move= self.minimax_alpha_beta()
		elif self.use_Heuristic1.get():
			move= self.heuristic1()
		elif self.use_Heuristic2.get():
			move= self.heuristic2()
		
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
		# mb_algo.add_checkbutton(label='MiniMax',     command=partial(toggle_func, self.game.use_minimax))
		mb_algo.add_checkbutton(label='MiniMax',     variable=self.game.use_minimax)
		mb_algo.add_checkbutton(label='Heuristic 1', variable=self.game.use_Heuristic1)
		mb_algo.add_checkbutton(label='Heuristic 2', variable=self.game.use_Heuristic2)
		#TODO

		mb_opti= tk.Menu(mb, tearoff=False)
		mb_opti.add_checkbutton(label='Alpha-Beta Pruning', variable=self.game.use_alpha_beta_pruning)
		mb_opti.add_checkbutton(label='Symmetry Reduction', variable=self.game.use_symmetry_reduction)

		mb_view= tk.Menu(mb, tearoff=False)
		mb_view.add_checkbutton(label='Dark Mode', command=self.toggle_darkmode)

		mb_help= tk.Menu(mb, tearoff=False)
		mb_help.add_command(label="About", command=self.about)

		mb.add_cascade(menu=mb_game, label='Game')
		mb.add_cascade(menu=mb_algo, label='Algorithm')
		mb.add_cascade(menu=mb_opti, label='Optimizations')
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
