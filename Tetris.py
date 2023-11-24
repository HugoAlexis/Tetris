#-----------------------------------------------------------------------#
# Remake of the classical Tetris, made with PyGame. Uses numpy to       #
# create and rote the figures, and to represent the board. Each         #
# figure has a key-number, wich corresponds to its color.               #
#                                                                       #
# Made by: Hugo Alexis Torres Pasillas                                  #
# Cration date: 04/24/20                  Last Update:04/28/20          #
#-----------------------------------------------------------------------#


import Constants as cts
import pygame
import random
import numpy as np 

pygame.init()


def empty_board(type=int):
	"""
	Create a numpy array wich is a depiction of the empty board.
	:param type: int-bool
	:return: Numpy.array
	"""
	EMPTY_BOARD = np.zeros((28,18))
	EMPTY_BOARD[-4:,:] = 99*np.ones((4,18))
	EMPTY_BOARD[:,0:4] = 99*np.ones((28,4))
	EMPTY_BOARD[:,-4:] = 99*np.ones((28,4))

	if type == bool:
		EMPTY_BOARD = np.array(EMPTY_BOARD,dtype=bool)
		EMPTY_BOARD = np.array(EMPTY_BOARD,dtype=int)

	return EMPTY_BOARD


def matrix_to_bool(matriz):
	"""
	Converts a matriz to binary: 0 if the element is a False-Value, and 1 otherwise.
	:param matriz: numpy array
	:return: numpy.array(dtype=int[0,1])
	"""
	matriz = matriz.copy()
	matriz = np.array(matriz,dtype=bool)
	matriz = np.array(matriz,dtype=int)

	return matriz

def print_next_figure(screen,key):
	"""
	Prints the next figure on the correspondent box of the game.
	:param screen: screen object
	:param key: int
	:return: None
	"""

	figure = cts.FIGURES[key].copy()
	imax,jmax = figure.shape

	for i in range(imax):
		for j in range(jmax):
			if figure[i,j] != 0:
				pygame.draw.rect(screen, cts.COLORS[cts.KEYS_COLORS[key]],[500-20*i,260+20*j,18,18])
class Board():
	"""
	Contains the board of the game as a matrix. In each direction, has 4 more elements, wich are used to
	find if the figure can move, fall, or rotate when a key is pressed.
	"""

	def __init__(self):
		"""
		Creates the main board, the board that will be printed on the screen, and contains the score.
		:param board_complete: Numpy.array representing the board (4 more elements in each direction,
		                       to detect colisions with the borders)
		:param real_board: Numpy.array representing the board (without the borders.)
		:param score: int
		:param GAME_OVER: Bool
		:return: None
		"""
		self.__board_complete = empty_board()
		self.__real_board = self.__board_complete[4:-4,4:-4]
		self.__score = 0
		self.GAME_OVER = False


	def print_board(self,screen):
		"""
		Prints the board on the screen.
		:param screen: screen object
		:return: None
		"""

		x_init = 120
		y_init = 40

		for i in range(10):
			for j in range(20):
				x = x_init + i*20
				y = y_init + j*20+2
				if self.__real_board[j,i] != 0:
					color = cts.KEYS_COLORS[self.__real_board[j,i]]

					pygame.draw.rect(screen,cts.COLORS[color],[x+1,y+1,18,18])

	def get_occuped_board(self):
		"""
		Returns a binary (0-1) copy of the board (matriz).
		:return: Numpy.array(dtype=int(0,1))
		"""
		board_copy = np.copy(self.__board_complete)
		board_copy = np.array(board_copy,dtype=bool)
		board_copy = np.array(board_copy,dtype=int)
		return board_copy

	def add_figure(self,figure_board):
		"""
		If the figure can't fall anymore, it is added to the main board. If a row is full, then it is
		delated and add a new empy row at the top.
		:param figure_board: int
		:return: None
		"""
		self.__board_complete += figure_board.copy()
		complet = []

		board = matrix_to_bool(self.__real_board)
		for i,row in enumerate(board):
			if np.sum(row) == 10:
				real_board = list(self.__board_complete.copy())
				real_board = [list(i) for i in real_board]
				del real_board[i+4]
				real_board.insert(0,list(empty_board()[0]))
				self.__board_complete = np.array(real_board)
				self.__real_board = self.__board_complete[4:-4,4:-4]
				self.__score += 10


		board = self.get_occuped_board()

		first_row = board[4,4:-4]
		
		if 1 in first_row:
			self.GAME_OVER = True

	def get_score(self):
		"""
		Returns the actual score.
		:return: int
		"""
		return self.__score




class figure:
	"""
	Contains a type of the figures. It controls the print of the figure in the screen, the position and
	the rotations. Also, cheks if the figure can move rotate or fall, and in this last case, if not, the 
	figure is added to the board (with add_figure() method).
	"""
	
	def __init__(self, num_figure):
		"""
		Select the figure with the key num_figure, and define the init position (x,y) in the board, as well as 
		the rotation (ramdom number between 0 to 3).
		:para num_figure: int
		:return: None
		"""

		self.__key_figure = num_figure
		self.__figure = self.__key_figure * cts.FIGURES[self.__key_figure].copy()
		
		self.__x_pos = 4
		self.__y_pos = 0

		self.__rot = random.randint(0,3)

	def __board_figure(self):
		"""
		Creates an empty board, and in it, add the current figure in the position and rotation wich will be in the
		real board.
		:return: numpy array
		"""
		board = empty_board()
		board[2+self.__y_pos:5+self.__y_pos,4+self.__x_pos:7+self.__x_pos] = np.rot90(self.__figure,k=self.__rot)

		return board


	def print_figure(self,screen):
		"""
		Prints out the figure on the screen.
		:param screen: screen (pygame) object
		:return: None
		"""
		board = self.__board_figure()
		real_board = board[4:-4,4:-4]
		
		x_init = 120
		y_init = 40

		for i in range(10):
			for j in range(20):
				x = x_init + i*20
				y = y_init + j*20+2
				if real_board[j,i] != 0:
					color = cts.KEYS_COLORS[real_board[j,i]]
					pygame.draw.rect(screen,cts.COLORS[color],[x+1,y+1,18,18])

	def get_board_figure(self):
		"""
		Return a copy of the figure in the empty board.
		:return: numpy array
		"""


		tboard = np.zeros((28,18))
		tboard[2+self.__y_pos:5+self.__y_pos,4+self.__x_pos:7+self.__x_pos] = np.rot90(self.__figure,k=self.__rot)


		return tboard
	def rot_figure(self,direction):
		"""
		Rotates the figure in the direction passed (1 to 90 degrees, and -1 to -90 degrees, both clockwise).
		:param: int (+1 or -1)
		:return: None
		"""

		if self.__key_figure != 4:
			if direction == 1:
				self.__rot = (self.__rot + 1)%4
			elif direction == -1:
				self.__rot = (self.__rot - 1)%4
			else:
				assert True, "Invalid direction"
	
	def move_figure_x(self,direction):
		"""
		Moves the figure horizontally (1 to right ane -1 to left.)
		:param direction: int (+1 or -1)
		"""

		if direction == 1:
			self.__x_pos += 1
		elif direction == -1:
			self.__x_pos -=1
		else:
			assert True, "Invalid direction"

	def fall_figure(self):
		"""
		Moves the figure vertically.
		:return: None
		"""
		self.__y_pos += 1

	def can_move(self,bool_board,direction):
		"""
		Determine weather the figure can moves horizontally or not.
		:param bool_board: numpy array(dtyep=int(0,1) or bool)
		:param direction: int (+1 or -1)
		:return: Bool
		"""
		
		if direction in [-1,1]:
			x_pos = self.__x_pos + direction
		else:
			assert True, "Invalid direction"

		board = np.zeros((28,18))
		board[2+self.__y_pos:5+self.__y_pos,4+x_pos:7+x_pos] = np.rot90(self.__figure,k=self.__rot)

		board = matrix_to_bool(board) + bool_board


		if 2 in board:
			return False
		else:
			return True
	
	def can_rot(self,bool_board):
		"""
		Determine weather the figure can rotates or not.
		:param bool_board: numpy array(dtype = int(+1,-1) or bool)
		:return: Bool
		"""
		rot = self.__rot + 1

		board = np.zeros((28,18))
		board[2+self.__y_pos:5+self.__y_pos,4+self.__x_pos:7+self.__x_pos] = np.rot90(self.__figure,k=rot)

		board = matrix_to_bool(board) + bool_board


		if 2 in board:
			return False
		else:
			return True

	def can_fall(self,bool_board):
		"""
		Determine weather the figure can fall (move vertically) or not.
		:param bool_board: numpy array(dtype=int (+1,-1) or Bool)
		:return : Bool
		"""
		y_pos = self.__y_pos + 1

		board = np.zeros((28,18))
		board[2+y_pos:5+y_pos,4+self.__x_pos:7+self.__x_pos] = np.rot90(self.__figure,k=self.__rot)

		board = matrix_to_bool(board) + bool_board


		if 2 in board:
			return False
		else:
			return True
def main():
	"""
	Main function of the game.
	:return : None
	"""

	screen_size = (640,480)
	screen = pygame.display.set_mode(screen_size)
	background_image = pygame.image.load("Tetris.jpg")
	game_over_image = pygame.image.load("game_over.jpg")
	clock = pygame.time.Clock()

	FPS = 60
	window_open = True
	contador = 0
	print_every = 20
	my_board = Board()


	next_figure = random.randint(1,7)
	my_figure =figure(random.randint(1,7))

	
	## To print out the score
	font = pygame.font.SysFont("calibri",40,True,False)

	# Main loop of the game.
	while window_open:

		#Control the events of the game.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window_open = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT and my_figure.can_move(my_board.get_occuped_board(),1):     # Move right
					my_figure.move_figure_x(1)
				elif event.key == pygame.K_LEFT and my_figure.can_move(my_board.get_occuped_board(),-1):  # Move left
					my_figure.move_figure_x(-1)
				elif event.key == pygame.K_SPACE  and my_figure.can_rot(my_board.get_occuped_board()):      # Rotates
					my_figure.rot_figure(1)
				elif event.key == pygame.K_DOWN:															# # Accelerate the fall						
					print_every = 1

			if event.type == pygame.KEYUP: 														# Deccelerate the fall
				if event.key == pygame.K_DOWN:
					print_every = 20
					
				
		screen.fill(cts.COLORS["WHITE"])

		if not my_board.GAME_OVER:
			screen.blit(background_image, [0, 0])
			my_board.print_board(screen)

		### Fall the figure each print_every cicles.
			if contador == 0:
                
                ### Checks if the figure can still fall.			
				if my_figure.can_fall(my_board.get_occuped_board()):
					my_figure.fall_figure()
				else:
                ### Else, add the figure at the board and create a new figure at the top.
					my_board.add_figure(my_figure.get_board_figure())
					my_figure = figure(next_figure)
					next_figure = random.randint(1,7)
				
		    #Prints out the next figure board
			my_figure.print_figure(screen)
			print_next_figure(screen,next_figure)
            #Prints out the score.
			text = font.render("{:3.0f}".format(my_board.get_score()),True,cts.COLORS["WHITE"])
			screen.blit(text,[500,400])

		else:
			screen.blit(game_over_image,[0,0])

			
		pygame.display.flip()

		contador = (contador+1)%print_every
		clock.tick(FPS)

	pygame.quit()

if __name__ == "__main__":
	main()