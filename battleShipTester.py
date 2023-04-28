import unittest
from battleShip import Ship, ShipGame


class TestShipGame(unittest.TestCase):
    """
    test class for ShipGame file to check functionality of each individual functionality
    """

    def test_ShipClass(self):
        """
        outlines tests for Ship class:
        1) Tests if Ship class instance exists
        2) Tests that Ship coordinates store properly and that getter method can retrieve.
        3) tests that delete_coordinate() method functions
        """

        # tests that instance of ship object is stored correctly
        test_ship = Ship([[1, 2], [2, 3], [3, 4]])
        self.assertIsInstance(test_ship, Ship,
                              "check that test_ship stores a Ship object ")

        # tests getter method and storage of coordinates
        self.assertTrue(test_ship.get_coordinates() == [[1, 2], [2, 3], [3, 4]],
                        "check the Ship's coordinates are returned by getter function")

        # tests delete_coordinate method
        test_ship.delete_coordinate([2, 3])
        self.assertTrue(test_ship.get_coordinates() == [[1, 2], [3, 4]],
                        "check that the delete_coordinate method works for the ship class")

    def test_ShipGameClass(self):
        """
        outlines test for initializing the ShipGame class:
        1) tests if ShipGame class instance exists.
        """
        test_game = ShipGame()

        self.assertIsInstance(test_game, ShipGame,
                              "check that test_game stores a ShipGame object ")

    def test_place_ship(self):
        """
        outlines ship placement test for method:
        1) tests that ships are stored in specified player ship list with proper coordinates.
        2) tests that ships' coordinates are stored in a player's master list.
        :return:
        """

        test_game = ShipGame()

        test_game.place_ship('first', 10, 'A1', 'R')

        # tests that ships can be placed at the top and far right and left edges of the board
        self.assertTrue(
            test_game.get_master_list('first') == [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
                                                   [9, 1], [10, 1]],
            "check that player master list updates with new coordinates")
        self.assertTrue(
            test_game.get_ship_list('first')[0].get_coordinates() == [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1],
                                                                   [7, 1], [8, 1], [9, 1], [10, 1]],
            "check that player ship list has new ship with proper coordinates")

        # test that ships can be placed along the top, bottom and left edge of the board
        test_game.place_ship('second', 10, 'A1', 'C')

        self.assertTrue(
            test_game.get_master_list('second') == [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9],[1, 10]],
            "check that player master list updates with new coordinates")
        self.assertTrue(
            test_game.get_ship_list('second')[0].get_coordinates() == [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9],[1, 10]],
            "check that second player ship list updates with the proper coordinates")

    def test_false_ship_placement(self):
        """
        tests that incorrect ship placements return False as per project specifications:
        1) tests that overlapping ships placements return False
        2) tests that any ships with x coordinates outside of the board return False
        3) tests that any ships with y coordinates outside of the board return False
        4) tests that coordinates not input in proper format (A-J,1-10, ex: F8) return False
        5) tests that ship placements of less than length 2 return False

        """
        test_game = ShipGame()

        # test that overlapping ship placement return false overlaps at J1
        test_game.place_ship('first', 10, 'A1', 'R')
        self.assertFalse(test_game.place_ship('first', 7, 'J1', 'C'),
                        "check that overlapping coordinates cannot be placed")
        # test that ships with placements outside of board return False by row and then by column
        self.assertFalse(test_game.place_ship('first', 7, 'B6', 'R'),
                         "check that ships ending outside of x-axis of the board are returned False")
        self.assertFalse(test_game.place_ship('first', 7, 'J1', 'C'),
                         "check that ships ending outside of y-axis of the board are returned False")

        # check that ships with improper string format return False
        self.assertFalse(test_game.place_ship('first', 7, '11', 'C'),
                         "check that coordinates of the incorrect string format are returned False")

        # check that ships of less than length 2 return False
        self.assertFalse(test_game.place_ship('first', 1, 'B2', 'C'),
                         "check that coordinates of the incorrect string format are returned False")

    def test_get_current_state(self):
        """
        tests the get_current_state method of Ship game
        1) returns 'UNFINISHED' when neither player has placed a ship
        2) returns 'SECOND_WON' when the first players master list contains no coordinates
        3) returns 'UNFINISHED' when both players still have coordinates in their player_master_lists
        4) returns 'FIRST_WON' when the Second players master list contains no coordinates
        :return:
        """
        test_game = ShipGame()
        # test 1
        self.assertTrue(test_game.get_current_state() == 'UNFINISHED',
                        "check that get_current state returns 'UNFINISHED' when neither player has placed a ship")
        # test 2
        test_game.place_ship('first', 2, 'A1', 'R')
        self.assertTrue(test_game.get_current_state() == 'FIRST_WON',
                        "check that get_current state returns 'FIRST_WON' when only first player has no coordinates in player_master_lists")
        # test 3
        test_game.place_ship('second', 2, 'A1', 'R')
        self.assertTrue(test_game.get_current_state() == 'UNFINISHED',
                        "check that get_current state returns 'UNFINISHED' when both players still have coordinates placed")

        # test 4
        test_game1 = ShipGame()
        test_game1.place_ship('second', 2, 'A1', 'R')
        self.assertTrue(test_game1.get_current_state() == 'SECOND_WON',
                        "check that get_current state returns 'FIRST_WON' when only second player has no coordinates in player_master_lists")

    def test_fire_torpedo(self):
        """
        tests the following functionality of the fire_torpedo method:
        1) tests that method deletes coordinates that hit opposing player's ships from opposing player's player_master_lists
        2) tests that method deletes coordinates that hit opposing players ships from opposing player's player_ship_lists' ship
        3) tests that method records coordinates of each player's torpedo shots in relevant _torpedo_shots list
        4) tests that the _player_turn changes from 'first' to 'second'
        5) tests that the player turn changes from 'second' to 'first'
        6) tests that once a players ships are all sunk, the Status of the game changes to represent that one of the players has won
        """

        test_game = ShipGame()

        test_game.place_ship('second', 3, "B2", "R")
        test_game.place_ship('first', 2, "B2", "R")
        test_game.fire_torpedo('first','B3')

        # test 1
        self.assertTrue(test_game.get_master_list('second') == [[2, 2], [4, 2]],
                        "checks that the ship's middle coordinate is deleted from the player's master list")
        # test 2
        self.assertTrue(test_game.get_ship_list('second')[0].get_coordinates() == [[2, 2], [4, 2]],
                        "checks that the ship's middle coordinate is deleted from the player's ship in the player's ship list")
        # test 3
        self.assertTrue(test_game.get_payer_torpedo_shots('first') == ['B3'],
                        "checks that player's torpedo shots are recorded")

        # test 4
        self.assertTrue(test_game.get_player_turn() == 'second',
                        "checks that _player_turn data member changes from 'first' to 'second' ")
        # test 5
        test_game.fire_torpedo('second', 'B2')
        self.assertTrue(test_game.get_player_turn() == 'first',
                        "checks that _player_turn data member changes from 'second' to 'first ")

        # test 6
        test_game.fire_torpedo('first', 'B2')
        test_game.fire_torpedo('second', 'B3')
        self.assertTrue(test_game.get_current_state() == 'SECOND_WON',
                        "checks that once the second player has shot down the first player's ships, that the status of the game updates to 'SECOND_WON'")

    def test_fire_torpedo_false(self):
        """
        tests that the method returns False when appropriate:
        1) tests that when it is not a player's turn, the method returns False
        2) tests that once a player has won, the method returns False
        """
        test_game = ShipGame()

        test_game.place_ship('second', 3, "B2", "R")
        test_game.place_ship('first', 2, "B2", "R")

        # test 1
        self.assertFalse(test_game.fire_torpedo('second', 'B3'),
                         "checks that only the player whose turn it is can fire a torpedo")
        # test 2
        test_game.fire_torpedo('first', 'B3')
        test_game.fire_torpedo('second', 'B2')
        test_game.fire_torpedo('first', 'B3')
        test_game.fire_torpedo('second', 'B3')
        self.assertFalse(test_game.fire_torpedo('second', 'B3'),
                         "checks that after the game has finished, that torpedoes cannot be fired")

    def test_get_number_ships(self):
        """
        tests the following functionality of the method:
        1) returns the number of ships left on a players board when no ship has been sunk
        2) returns the number of ships left on a players board when a ship has been sunc
        :return:
        """

        test_game = ShipGame()

        test_game.place_ship('second', 3, "B2", "R")
        test_game.place_ship('first', 2, "B2", "R")

        # test 1
        self.assertTrue(test_game.get_num_ships_remaining('first') ==1,
                        "checks that the number of ships is correct when no ships have been sunk")
        # test 2
        test_game.fire_torpedo('first', 'B3')
        test_game.fire_torpedo('second', 'B2')
        test_game.fire_torpedo('first', 'B3')
        test_game.fire_torpedo('second', 'B3')
        self.assertTrue(test_game.get_num_ships_remaining('first') == 0,
                        'checks that the number of ships is correct when one ship has been sunk')