
# Author: Sami Noor Syed
# GitHub username: saminoorsyed
# Date: 3/10/2022
# Description: Defines the battle ship game outlined in the readme file. contains two classes Ship and Ship Game with the requisite functionalities. This project also has a related tester file. I included a note at the top of the readme explaining my thought process and some areas of possible improvement that I may pursue given the time

class Ship:
    """
     A class that stores all of the coordinates that belong a ship. This class will have the following methods and data members:
•	An init method that takes the parameters of a list of coordinates 
•	A delete method that deletes one of the coordinates contained within the list
•	A get method that retrieves the coordinates of a ship
•	Ship coordinates are stored as a private data member as a list of lists
    """

    def __init__(self, list_coordinates):
        """
        initializes the ships coordinates which should come as a list of lists
        :param list_coordinates: list of lists
        """
        self._coordinates = list_coordinates

    def get_coordinates(self):
        """
        controls access to private data member
        :return: a list of coordinates that are in the form [x,y]
        """
        return self._coordinates

    def delete_coordinate(self, torpedo_location):
        """
        checks whether the coordinate is within the list if it is not, returns true, if it is, method removes the coordinate and returns false
        :param torpedo_location:
        :return: Boolean
        """
        if torpedo_location in self._coordinates:
            self._coordinates.remove(torpedo_location)


class ShipGame:
    """
    The ShipGame class should have these methods:
* an init method that has no parameters and sets all data members to their initial values
* `place_ship` takes as arguments: the player (either 'first' or 'second'), the length of the ship, the coordinates of the square it will occupy that is closest to A1, and the ship's orientation - either 'R' if its squares occupy the same row, or 'C' if its squares occupy the same column (there are a couple of examples below). If a ship would not fit entirely on that player's grid, or if it would overlap any previously placed ships on that player's grid, or if the length of the ship is less than 2, the ship should not be added and the method should **return False**. Otherwise, the ship should be added and the method should **return True**. * `get_current_state` returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'.
* `fire_torpedo` takes as arguments the player firing the torpedo (either 'first' or 'second') and the coordinates of the target square, e.g. 'B7'. If it's not that player's turn, or if the game has already been won, it should just **return False**. Otherwise, it should record the move, update whose turn it is, update the current state (if this turn sank the opponent's final ship), and **return True**. If that player has fired on that square before, that's not illegal - it just wastes a turn. You can assume `place_ship` will not be called after firing of the torpedos has started.
* `get_num_ships_remaining` takes as an argument either "first" or "second" and returns how many ships the specified player has left.
    """

    def __init__(self):
        """
        an init method that has no parameters and sets all data members to their initial values of each player’s board and whose turn it is. Will initialize the constraints for piece placement including an empty list in which to store the coordinates of each ship placed per each player. It also initializes an empty list for each player that will later be used to store a list of ships
        """
        self._letter_map = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
            'I': 9,
            'J': 10
        }
        self._constraint = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self._player_master_lists = {
            "first": [],
            "second": []
        }
        self._player_ships = {
            "first": [],
            "second": []
        }
        self._torpedo_shots = {
            "first": [],
            "second": []
        }
        self._player_turn = 'first'
        self._player_not_turn = 'second'
        self._game_status = 'UNFINISHED'

    def get_payer_torpedo_shots(self,player):
        """
        returns a player's list of torpedo shots
        :param player: string, 'first' or 'second'
        :return: list of lists
        """
        return self._torpedo_shots[player]

    def get_master_list(self, player):
        """
        returns a player's master list of ship coordinates remaining on the board
        :param: string , 'first' or 'second'
        :return: list object
        """
        return self._player_master_lists[player]

    def get_ship_list(self, player):
        """
        returns the list of player Ship objects
        :param player: string, 'first' or 'second'
        :return: list of Ship objects
        """
        return self._player_ships[player]

    def get_player_turn(self):
        """
        gets which player's turn it currently is
        :return: string, either 'first' or 'second'
        """
        return self._player_turn


    def place_ship(self, player, ship_length, input_coordinate, orientation):
        """
        place_ship takes as arguments: the player (either 'first' or 'second'), the length of the ship, the coordinates of the square it will occupy that is closest to A1, and the ship's orientation - either 'R' if its squares occupy the same row, or 'C' if its squares occupy the same column. If a ship will not fit entirely on that player's grid, or if it overlaps any previously placed ships on that player's grid, or if the length of the ship is less than 2, the ship should not be added and the method should **return False**. Otherwise, the ship should be added and the method should **return True**.  This method will translate the string coordinates to integer coordinates [x,y] and store those integers in a player’s master list as well as in a ship class that is appended to a player’s list of ships.
        :param player: string either 'first' or 'second'
        :param ship_length: integer
        :param input_coordinate: string
        :param orientation: string
        :return: Boolean
        """
        new_ship_coord = []
        if ship_length <= 1:
            return False
        if input_coordinate[0] not in self._letter_map:
            return False
        else:
            # change letter to integer, and store in coordinate value as [x,y]
            coordinate = [int(input_coordinate[1]), self._letter_map[input_coordinate[0]]]
            # check that the initial placement is within the field of play.
            if coordinate[0] not in self._constraint or coordinate[1] not in self._constraint:
                return False
            if orientation == "C":
                # check that the whole ship can fit on the field
                if coordinate[1] + ship_length - 1 >= 11:
                    return False
                # check coordinate points by iterating through each column value with a constant row value and check against previous placements
                for y_coord in range(coordinate[1], coordinate[1] + ship_length):
                    if [coordinate[0], y_coord] in self._player_master_lists[player]:
                        return False
                    else:
                        self._player_master_lists[player].append([coordinate[0], y_coord])
                        new_ship_coord.append([coordinate[0], y_coord])
                self._player_ships[player].append(Ship(new_ship_coord))
                return True
            if orientation == "R":
                # check that the whole ship can fit on the field
                if coordinate[0] + ship_length - 1 >= 11:
                    return False
                # check coordinate points by iterating through each row value with a constant column value and check against previous placements
                for x_coord in range(coordinate[0], coordinate[0] + ship_length):
                    if [x_coord, coordinate[1]] in self._player_master_lists[player]:
                        return False
                    else:
                        self._player_master_lists[player].append([x_coord, coordinate[1]])
                        new_ship_coord.append([x_coord, coordinate[1]])
                self._player_ships[player].append(Ship(new_ship_coord))
                return True

    def get_current_state(self):
        """
         get_current_state returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED.’ It does so by checking each players master list. If a player’s master list’s length is zero, then that player has lost and the other player has won
        :return: string
        """
        if len(self._player_master_lists['first']) == 0 and len(self._player_master_lists['second']) == 0:
            return self._game_status
        if len(self._player_master_lists['first']) != 0 and len(self._player_master_lists['second']) != 0:
            self._game_status = "UNFINISHED"
            return self._game_status
        if len(self._player_master_lists['first']) == 0:
            self._game_status = 'SECOND_WON'
            return self._game_status
        if len(self._player_master_lists['second']) == 0:
            self._game_status = 'FIRST_WON'
            return self._game_status
        else:
            return self._game_status

    def fire_torpedo(self, player, input_coordinate):
        """
        fire_torpedo takes as arguments the player firing the torpedo (either 'first' or 'second') and the coordinates of the target square, If it's not that player's turn, or if the game has already been won, it should just **return False**. Otherwise, it should record the move, delete the coordinate from a player’s ships and master list, update whose turn it is, update the current state (if this turn sank the opponent's final ship), and **return True**. If that player has fired on that square before, that's not illegal - it just wastes a turn.
        :param player: string either 'first' or 'second'
        :param input_coordinate: string
        :return: Boolean
        """
        if player != self._player_turn or self._game_status != 'UNFINISHED':
            return False
        else:
            self._torpedo_shots[player].append(input_coordinate)
            # change letter to integer, and store in coordinate value as [x,y]
            coordinate = [int(input_coordinate[1]), self._letter_map[input_coordinate[0]]]
            # change player turn
            if self._player_turn == "first":
                self._player_turn = "second"
                self._player_not_turn = "first"
            elif self._player_turn == "second":
                self._player_turn = "first"
                self._player_not_turn = "second"
            if coordinate in self._player_master_lists[self._player_turn]:
                self._player_master_lists[self._player_turn].remove(coordinate)
                for ship in self._player_ships[self._player_turn]:
                    if coordinate in ship.get_coordinates():
                        ship.delete_coordinate(coordinate)
                        return True

            return True

    def get_num_ships_remaining(self, player):
        """
        get_num_ships_remaining takes as an argument either "first" or "second" and returns how many ships the specified player has left by checking the length of each ship’s coordinate in their list of ships.
        :param player: string either 'first' or 'second'
        :return: integer
        """
        ships_left = 0
        for ship in self._player_ships[player]:
            if len(ship.get_coordinates()) >= 1:
                ships_left += 1
        return ships_left

    def print_player_board(self, player):
        """
        takes the desired player as a parameter and prints a representation of their board that is easy to read
        :param player: string, 'first' or 'second'
        :return: None
        """
        board = {
            "0": ["0", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "1": ["A", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "2": ["B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "3": ["C", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "4": ["D", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "5": ["E", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "6": ["F", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "7": ["G", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "8": ["H", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "9": ["I", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "10": ["J", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

        for coordinate in self._player_master_lists[player]:
            # change 0 to one on board representation wherever a ship is
            board[str(coordinate[1])][coordinate[0]] = 1

        for row in range(0, 11):
            print(board[str(row)])

    def print_torpedo_shots(self, player):
        """
        returns a representation of a players shots on a board
        :param player: string, 'first' or 'second'
        :return: None
        """

        board = {
            "0": ["0", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "1": ["A", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "2": ["B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "3": ["C", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "4": ["D", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "5": ["E", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "6": ["F", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "7": ["G", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "8": ["H", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "9": ["I", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "10": ["J", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        for input_coordinate in self._torpedo_shots[player]:
            coordinate = [int(input_coordinate[1]), self._letter_map[input_coordinate[0]]]
            # change 0 to one on board representation wherever a ship is
            board[str(coordinate[1])][coordinate[0]] = 1
        for row in range(0, 11):
            print(board[str(row)])
