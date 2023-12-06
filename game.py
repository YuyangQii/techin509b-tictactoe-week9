import os
import csv
import logging
from board import Board
from player import Player

class Game:
    def __init__(self, players):
        self.board = Board()
        self.players = players
        self.current_player_index = 0
        self.move_number = 1  # 记录移动编号
        self.first_player = players[0]  # 记录第一个玩家
        self.game_moves = []  # To track moves and stats for CSV
        self.last_result = None  # 记录上一轮的游戏结果
        self.setup_logging()

    def start(self):
        logging.info("Game started")
        while self.board.get_winner() is None and not self.board.is_full():
            self.board.print_board()
            current_player = self.players[self.current_player_index]
            row, col = current_player.make_move(self.board.board)
            if self.board.make_move(row, col, current_player.symbol):
                self.log_move(current_player, row, col)
                result = self.board.get_winner()
                if result and result != "Draw":  # 排除 "Draw" 结果
                    result_str = f"{result} wins!"
                    if self.move_number == 1 or result_str != self.last_result:
                        print(f"\n{result_str}")
                else:
                    result_str = "Continue"
                self.game_moves.append([self.move_number, current_player.symbol, row, col, result_str])
                self.switch_player()
                self.move_number += 1
                self.last_result = result_str
            else:
                logging.warning(f"Invalid move by {current_player.symbol}")
        self.end_game()
        self.save_game_results_to_csv()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def end_game(self):
        self.board.print_board()
        winner = self.board.get_winner()
        if winner and winner != "Draw":  # 排除 "Draw" 结果
            result = f"{winner} wins!"
            if self.move_number == 1 or result != self.last_result:
                print(f"\n{result}")
        else:
            result = "Draw"
            if self.move_number == 1 or result != self.last_result:
                print(f"\nThe game is a {result}.")
        
        # 将游戏结果添加到游戏日志中
        if self.move_number == 1 or result != self.last_result:
            self.game_moves.append([self.move_number, self.first_player.symbol, result])

    def log_move(self, player, row, col):
        logging.info(f'Player {player.symbol} moved to ({row}, {col})')

    def save_game_results_to_csv(self):
        csv_file = 'game_results.csv'
        with open(csv_file, 'a', newline='') as file:  # 使用 'a' 模式以追加数据到现有文件
            writer = csv.writer(file)
            if self.move_number == 1:
                writer.writerow(["Movenumber", "player", "Row", "Column", "Result"])  # 写入列标题
            for move in self.game_moves:
                writer.writerow(move)

    @staticmethod
    def setup_logging():
        log_directory = "logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        logging.basicConfig(
            filename=os.path.join(log_directory, 'game.log'),
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

if __name__ == '__main__':
    single_player_mode = input("Single player mode? (y/n): ").lower() == 'y'
    player1 = Player('X')
    if single_player_mode:
        player2 = Player('O', is_bot=True)
    else:
        player2 = Player('O')
    game = Game([player1, player2])
    game.start()
