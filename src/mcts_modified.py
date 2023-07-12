
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    while node.child_nodes:
        tempstate = state
        if node is None:
            return -1
        action = choice(list(node.child_nodes.keys()))
        state = board.next_state(state, action)
        if tempstate == state: 
            break
        if action is not None and node.child_nodes:
            node = node.child_nodes[action]
    return node
    pass
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    action = choice(node.untried_actions)
    new_state = board.next_state(state, action)
    added_child = MCTSNode(parent = node, parent_action = action, action_list=board.legal_actions(new_state))
    node.child_nodes[action] = added_child
    node.untried_actions.remove(action)
    return added_child


    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    """
    owned_at_start = board.owned_boxes(state)
    legal_at_start = board.legal_actions(state)

    while not board.is_ended(state):
            changes = []  
            for action in legal_at_start:
                next_state = board.next_state(state, action)
                if board.owned_boxes(next_state) != owned_at_start:
                    changes.append(action)
            if action is not None and changes:
                action = choice(board.legal_actions(state))
            elif action is not None:
                action = choice(board.legal_actions(state))
                
            
#            print("state is :", state)
            state = board.next_state(state, action)
    return state 


    
    

                  

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    tempnode = node
    while tempnode is not None:
        tempnode.visits = tempnode.visits + 1
        if won:
            tempnode.wins = tempnode.wins + 1
        tempnode = tempnode.parent
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    i = num_nodes # testing value for number of nodes
    for i in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node
        new_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        child_node = new_node
        if child_node.visits == 0:
            while len(child_node.untried_actions) > 0:
                new_node = expand_leaf(child_node, board, sampled_game)
        sampled_game = board.next_state(sampled_game, new_node.parent_action)
        rollout_rest = rollout(board, sampled_game)
        win_rate = board.points_values(rollout_rest)[identity_of_bot] == 1
        backpropagate(new_node, win_rate) 
        i -= 1
        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    best_node = choice(list(root_node.child_nodes.values()))
    for children in root_node.child_nodes.values():
        if (100*(children.wins)/(children.visits+1)) > (100*best_node.wins/(best_node.visits+1)):
            best_node = children
    print('best node with winrate', 100*best_node.wins/(best_node.visits+1), 'is', best_node)
    return best_node.parent_action
