import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        return set(self.cells) if len(self.cells) == self.count else set()
  
    def known_safes(self):
        return set(self.cells) if self.count == 0 else set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            return

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # 1) Mark the cell as a move made
        self.moves_made.add(cell)
        
        # 2) Mark the cell as safe
        self.mark_safe(cell)
        
        # 3) Add new sentence to knowledge base
        # First, get ALL neighbors
        all_neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    all_neighbors.add((i, j))
        
        # Separate known mines and unknown cells
        known_mine_count = 0
        unknown_neighbors = set()
        for neighbor in all_neighbors:
            if neighbor in self.mines:
                known_mine_count += 1
            elif neighbor not in self.safes:
                unknown_neighbors.add(neighbor)
        
        # Create sentence with adjusted count
        new_count = count - known_mine_count
        if len(unknown_neighbors) > 0:
            new_sentence = Sentence(unknown_neighbors, new_count)
            self.knowledge.append(new_sentence)
        else:
            # If all neighbors are known, nothing new to add
            pass
        
        # 4) & 5) Mark cells and infer new sentences
        new_inferences = True
        while new_inferences:
            new_inferences = False
            
            # Check for newly known mines and safes
            for sentence in self.knowledge:
                known_mines = sentence.known_mines()
                for mine in known_mines:
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        new_inferences = True
                
                known_safes = sentence.known_safes()
                for safe in known_safes:
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        new_inferences = True
            
            # Infer new sentences
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue
                    if s1.cells <= s2.cells:
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge and len(new_cells) > 0:
                            self.knowledge.append(new_sentence)
                            new_inferences = True

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))
        
        if possible_moves:
            return random.choice(possible_moves)
        return None
