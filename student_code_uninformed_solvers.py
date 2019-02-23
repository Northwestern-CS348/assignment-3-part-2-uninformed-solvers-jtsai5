from solver import *
from collections import deque

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
        #print(self.currentState.requiredMovable)
        if self.currentState.state == self.victoryCondition:
            return True
        for m in self.gm.getMovables():
            #print(m)
            self.gm.makeMove(m)
            new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, m)
            new_state.parent = self.currentState
            if new_state not in self.visited and new_state not in self.currentState.children:
                self.currentState.children.append(new_state)
            self.gm.reverseMove(m)
        #print(self.currentState.requiredMovable)
        while self.currentState.nextChildToVisit >= len(self.currentState.children) and self.currentState is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        while self.currentState.nextChildToVisit < len(self.currentState.children):
            next_state = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            if next_state not in self.visited:
                self.currentState = next_state
                self.visited[self.currentState] = True
                self.gm.makeMove(next_state.requiredMovable)
                if self.currentState.state == self.victoryCondition:
                    return True
                break 
            while self.currentState.nextChildToVisit >= len(self.currentState.children) and self.currentState is not None:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
        return False
                

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()

    def traverse_to_state(self, next_state):
        # If relationship is child and parent, just go down
        if next_state.parent == self.currentState:
            self.gm.makeMove(next_state.requiredMovable)
            self.currentState = next_state
            return
        # Get lineage from current to root
        lineage_from = []
        state = self.currentState
        while state.parent:
            lineage_from.append(state.parent)
            state = state.parent
        # Get lineage from next state to root
        lineage_to = []
        state = next_state
        while state.parent:
            lineage_to.append(state.parent)
            state = state.parent
        # Finding earliest common ancestor
        for state in lineage_to:
            if state in lineage_from:
                ancestor = state
                break
        # Get moves required to go from current to common ancestor                
        s = self.currentState
        moves_from = []
        while s is not ancestor:
            moves_from.append(s.requiredMovable)
            s = s.parent
        # Get moves required to go from next state to common ancestor
        s = next_state
        moves_to = []
        while s is not ancestor:
            moves_to.append(s.requiredMovable)
            s = s.parent
        # Move from current to ancestor
        for m in moves_from:
            self.gm.reverseMove(m)
        # Move from ancestor to next
        for m in reversed(moves_to):
            self.gm.makeMove(m)

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
        # If in victoryCondition 
        self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True
        # Add unvisited states to queue
        for m in self.gm.getMovables():
            self.gm.makeMove(m)
            new_state = GameState(self.gm.getGameState(), self.currentState.depth+1, m)
            new_state.parent = self.currentState
            if new_state not in self.visited and new_state not in self.queue:
                self.queue.append(new_state)
            self.gm.reverseMove(m)
        # If not victoryCondition and no more states to explore --> Failure
        if len(self.queue) == 0:
            return False
        # Get next state to explore   
        next_state = self.queue.popleft()
        self.traverse_to_state(next_state)
        self.currentState = next_state
        return False
