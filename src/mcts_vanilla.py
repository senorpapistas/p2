
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1
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
    while not board.is_ended(state):
        if node is None:
            return -1
        action = choice(node.untried_actions)
#        print("Action is:", action)
#        print("Bot number:", identity)
        state = board.next_state(state, action)
        if action is not None and node.child_nodes:
            node = node.child_nodes[action]
    return node
    # pass
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
    pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        action = choice(board.legal_actions(state))
        state = board.next_state(state,action)
    return state
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    # root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    while node is not None:
        node.visits = node.visits + 1
        if won:
            node.wins = node.wins + 1
        node = node.parent
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

    while not board.is_ended(state):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node
        new_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        if len(new_node.untried_actions) > 0:
            new_node = expand_leaf(new_node, board, sampled_game)
        sampled_game = board.next_state(sampled_game, node.parent_action)
        rollout_rest = rollout(board, sampled_game)
        win_rate = board.points_values(rollout_rest)[identity_of_bot] == 1
        backpropagate(new_node, win_rate) 
        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    #best_winrate = max(root_node.child_nodes.values())
    return new_node.parent_action
