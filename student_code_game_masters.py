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
        if self.isMovableLegal(movable_statement) == True:
        # Extract variables/constants from terms in the statement
        #pdb.set_trace()
            sl = movable_statement.terms
            # Store disk the one being moved is on top of
            matches = self.kb.kb_ask(parse_input('fact: (ontopof '+str(sl[0])+' ?disk)'))
            if matches:
                disk_under = matches[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (ontopof '+str(sl[0])+' '+disk_under+')'))
            #pdb.set_trace()
            #print(disk_under)
            # Store top disk of target peg to retract if any
            matches2 = self.kb.kb_ask(parse_input('fact: (topdiskof '+str(sl[2])+' ?disk)'))
            if matches2:
                target_top = matches2[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (topdiskof '+str(sl[2])+' '+target_top+')'))
            else: 
                self.kb.kb_retract(parse_input('fact: (empty '+str(sl[2])+')'))
            # Disk no longer on initial peg - retract the on and topdiskof facts
            self.kb.kb_retract(parse_input('fact: (on '+str(sl[0])+' '+str(sl[1])+')'))
            self.kb.kb_retract(parse_input('fact: (topdiskof '+str(sl[1])+' '+str(sl[0])+')'))

            # Facts to assert
            self.kb.kb_assert(parse_input('fact: (on '+str(sl[0])+' '+str(sl[2])+')'))
            self.kb.kb_assert(parse_input('fact: (topdiskof '+str(sl[2])+' '+str(sl[0])+')'))
            if matches:
                disk_under = matches[0].bindings_dict['?disk']
                self.kb.kb_assert(parse_input('fact: (topdiskof '+str(sl[1])+' '+disk_under+')'))
            if matches2:
                target_top = matches2[0].bindings_dict['?disk']
                self.kb.kb_assert(parse_input('fact: (ontopof '+str(sl[0])+' '+target_top+')'))
            checker = self.kb.kb_ask(parse_input('fact: (on ?disk '+str(sl[1])+')'))
            if checker == False:
                self.kb.kb_assert(parse_input('fact: (empty '+str(sl[1])+')'))



            

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
        state = []
        # Row 1
        row1 = ['a', 'a', 'a', 'a']
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos1 pos1'))
        num1 = matches[0].bindings_dict['?tile']
        if num1 != 'empty':
            row1.insert(3, int(num1[-1:]))
        else:
            row1.insert(3, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos2 pos1'))
        num2 = matches[0].bindings_dict['?tile']
        if num2 != 'empty':
            row1.insert(4, int(num2[-1:]))
        else:
            row1.insert(4, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos3 pos1'))
        num3 = matches[0].bindings_dict['?tile']
        if num3 != 'empty':
            row1.insert(5, int(num3[-1:]))
        else:
            row1.insert(5, -1)
        row1 = [x for x in row1 if x != 'a'] 
        row1 = tuple(row1)
        # Row 2    
        row2 = ['a', 'a', 'a', 'a']
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos1 pos2'))
        num4 = matches[0].bindings_dict['?tile']
        if num4 != 'empty':
            row2.insert(3, int(num4[-1:]))
        else:
            row2.insert(3, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos2 pos2'))
        num5 = matches[0].bindings_dict['?tile']
        if num5 != 'empty':
            row2.insert(4, int(num5[-1:]))
        else:
            row2.insert(4, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos3 pos2'))
        num6 = matches[0].bindings_dict['?tile']
        if num6 != 'empty':
            row2.insert(5, int(num6[-1:]))
        else:
            row2.insert(5, -1)
        row2 = [x for x in row2 if x != 'a'] 
        row2 = tuple(row2)
        # Row 3         
        row3 = ['a', 'a', 'a', 'a']
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos1 pos3'))
        num7 = matches[0].bindings_dict['?tile']
        if num7 != 'empty':
            row3.insert(3, int(num7[-1:]))
        else:
            row3.insert(3, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos2 pos3'))
        num8 = matches[0].bindings_dict['?tile']
        if num8 != 'empty':
            row3.insert(4, int(num8[-1:]))
        else:
            row3.insert(4, -1)
        matches = self.kb.kb_ask(parse_input('fact: (coord ?tile pos3 pos3'))
        num9 = matches[0].bindings_dict['?tile']
        if num9 != 'empty':
            row3.insert(5, int(num9[-1:]))
        else:
            row3.insert(5, -1)
        #print(row3)
        row3 = [x for x in row3 if x != 'a'] 
        row3 = tuple(row3)
        state = (row1, row2, row3)
        return state

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
        #if self.isMovableLegal(movable_statement) == True and movable_statement.predicate == 'movable': 
        tilem = movable_statement.terms[0]
        old_x = movable_statement.terms[1]
        old_y = movable_statement.terms[2]
        new_x = movable_statement.terms[3]
        new_y = movable_statement.terms[4]
        # Retract old position
        self.kb.kb_retract(Fact(Statement(["coord", tilem, old_x, old_y])))
        self.kb.kb_retract(Fact(Statement(["coord", "empty", new_x, new_y])))
        # Assert new position
        self.kb.kb_assert(Fact(Statement(["coord", tilem, new_x, new_y])))
        self.kb.kb_assert(Fact(Statement(["coord", "empty", old_x, old_y])))
        return

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