class GameTieError(Exception):
    pass


class Player:
    def _init_(self, name: str, marker: str):
        self.name = name
        self.marker = marker


class Board:
    def _init_(self, size: int):
        self.reset(size)

    def reset(self, size: int):
        self.board = [['' for x in range(size)].copy() for y in range(size)]
        self.rowsCount = {}
        self.colsCount = {}
        self.diagonalsCount = {}
        self.size = size
        self.pieceCount = 0

    def place(self, player: Player, x: int, y: int):

        if x < 0 or y < 0 or x >= self.size or y >= self.size or self.board[x][y] != '':
            raise ValueError('Invalid Move')
        else:
            marker = player.marker
            self.board[x][y] = marker
            self.pieceCount += 1
            self.rowsCount[x] = self.rowsCount.get(x, {})
            self.rowsCount[x][marker] = self.rowsCount[x].get(marker, 0) + 1
            if self.rowsCount[x][marker] == self.size:
                return True
            self.colsCount[y] = self.colsCount.get(y, {})
            self.colsCount[y][marker] = self.colsCount[y].get(marker, 0) + 1
            if self.colsCount[y][marker] == self.size:
                return True
            if x == y:
                self.diagonalsCount["forward"] = self.diagonalsCount.get("forward", {})
                self.diagonalsCount["forward"][marker] = self.diagonalsCount["forward"].get(marker, 0) + 1
                if self.diagonalsCount["forward"][marker] == self.size:
                    return True
            if x + y == self.size - 1:
                self.diagonalsCount["backward"] = self.diagonalsCount.get("backward", {})
                self.diagonalsCount["backward"][marker] = self.diagonalsCount["backward"].get(marker, 0) + 1
                if self.diagonalsCount["backward"][marker] == self.size:
                    return True
            if self.pieceCount >= self.size ** 2:
                raise GameTieError('Game Tie')
            return False


class Game:
    def _init_(self, player1: Player, player2: Player, board: Board):
        self.player1 = player1
        self.player2 = player2
        self.board = board

    def play_game(self):
        curr_turn = 1
        game_done = False
        while not game_done:
            curr_player = self.player1 if curr_turn % 2 == 1 else self.player2
            x = int(input(f"{curr_player.name} Write x position of marker: "))
            y = int(input(f"{curr_player.name} Write y position of marker: "))
            try:
                if self.board.place(curr_player, x, y):
                    game_done = True
                    print(f"{curr_player.name} Wins!")
                else:
                    curr_turn += 1
            except ValueError as e:
                print(e)

            except GameTieError as e:
                print(e)
                game_done = True


player1 = Player("Shashank", "x")
player2 = Player("Nihal", "y")
board = Board(3)
game = Game(player1, player2, board)
game.play_game()