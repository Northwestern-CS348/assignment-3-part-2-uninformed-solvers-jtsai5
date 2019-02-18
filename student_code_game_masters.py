from game_master import GameMaster
from read import *
from util import *
import pdb

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        # State is the Tuple of Tuples being returned
        state = []
        # peg1's tuple
        diskson1 = []
        # Ask kb which disks bind to ?disk as being on peg1
        matches = self.kb.kb_ask(parse_input('fact: (on ?disk peg1)'))
        # If peg1 isn't empty
        if matches != False:
            for m in matches:
                string = m.bindings_dict['?disk']
                diskson1.append(int(string[-1:]))
                #print(diskson1)
            diskson1.sort()
                #print(diskson1)
            state.append(tuple(diskson1))
        # If empty, add in empty tuple
        else:
            state.append(())
        # Check if peg2 empty
        diskson2 = []
        matches = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))
        if matches != False:                
            for m in matches:
                string = m.bindings_dict['?disk']
                diskson2.append(int(string[-1:]))
                #print(diskson2)
            diskson2.sort()
            state.append(tuple(diskson2))
        # If empty, add in empty tuple
        else:
            state.append(())
        # Check if peg3 empty     
        diskson3 = []
        matches = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))
        if matches != False:
            for m in matches:
                string = m.bindings_dict['?disk']
                diskson3.append(int(string[-1:]))
                    #print(diskson3)
            diskson3.sort()
            state.append(tuple(diskson3))
        # If empty, add in empty tuple
        else:
            state.append(())
        # Return the tuple of tuples
        return tuple(state)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate != "movable":
            pass
        else:
            # Extract variables/constants from terms in the statement
            #pdb.set_trace()
            sl = movable_statement.terms
            # sl[0] = disk being moved, sl[1] = initial peg, sl[2] = target peg
            #newList = [sl[0], sl[1], sl[2]]
            # Store disk the one being moved is on top of
            matches = self.kb.kb_ask(parse_input('fact: (ontopof '+str(sl[0])+' ?disk)'))
            if matches != False:
                disk_under = matches[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (ontopof '+str(sl[0])+' '+disk_under+')'))
            else:
                pass
            #pdb.set_trace()
            #print(disk_under)
            # Store top disk of target peg, used to split for if it's none or actual disk
            matches2 = self.kb.kb_add(parse_input('fact: (topdiskof '+str(sl[2])+' ?disk)'))
            # Facts to retract
            self.kb.kb_retract(parse_input('fact: (on '+str(sl[0])+' '+str(sl[1])+')'))
            self.kb.kb_retract(parse_input('fact: (topdiskof '+str(sl[1])+' '+str(sl[0])+')'))
            if matches2:
                target_top = matches2[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (topdiskof '+str(sl[2])+' '+target_top+')'))
            else: 
                pass
            # Facts to assert
            self.kb.kb_assert(parse_input('fact: (on '+str(sl[0])+' '+str(sl[2])+')'))
            self.kb.kb_assert(parse_input('fact: (topdiskof '+str(sl[2])+' '+str(sl[0])+')'))
            if matches2:
                target_top = matches2[0].bindings_dict['?disk']
                self.kb.kb_assert(parse_input('fact: (ontopof '+str(sl[0])+' '+target_top+')'))
            else: 
                pass


        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
