
class Game:
    def __init__(self ,boards ,player1 ,player2):
        self.__boards = boards
        self.__player1 = player1
        self.__player2 = player2



    def get_player1(self):
        return self.__player1

    def get_player2(self):
        return self.__player2

    def get_boards(self):
        return self.__boards