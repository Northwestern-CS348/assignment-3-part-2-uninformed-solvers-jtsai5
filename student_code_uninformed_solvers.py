from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # Check if victory condition
        if self.currentState.state == self.victoryCondition:
            return True
        # Check if currentState has been visited
        # if self.currentState.state in self.visited:
        #     pass
        # else:
        #     self.visited[self.currentState] = True
        # Get list of movables to populate children
        moves = self.gm.getMovables()
        if moves:
            for m in moves:
                self.gm.makeMove(m)
                new = GameState(self.gm.getGameState(), self.currentState.depth+1, m)
                self.currentState.children.append(new)
                new.parent = self.currentState
                self.gm.reverseMove()
        # Visit children in list
        # If reached the end with nextchildtovisit, if end go up, if not visit that child
            # If not already visited, add to visited and set to true and increment next child to visit
            # make the move
            for c in self.currentState.children: 
                if c not in self.visited:
                    # Add it to visited
                    self.visited[c] = True
                    c.nextchildtovisit += 1
                    # Make move to get to that child 
                    self.gm.makeMove(self.currentState.children[c].requiredMovable)
                    # Set curr state to new node
                    self.currentState = self.currentState.children[c]
                    break 
        # If there are no movables, at a leaf. Reverse till can go back down
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)





class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
