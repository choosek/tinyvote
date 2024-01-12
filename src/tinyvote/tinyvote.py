"""
Minimal pure-Python library that demonstrates a basic encrypted
voting workflow via a secure multi-party computation (MPC)
`protocol <https://eprint.iacr.org/2023/1740>`__.
"""
from __future__ import annotations
from typing import List
import doctest
import tinynmc

class node:
    """
    Data structure for maintaining the information associated with a node
    and performing node operations.
    """
    def __init__(self):
        """
        Create a node instance and define its private attributes.
        """
        self._signature: List[int] = None
        self._choices: int = None
        self._nodes: List[tinynmc.node] = None

    def masks(self, request): # pylint: disable=redefined-outer-name
        """
        Return masks for a given request.

        :param request: Request from voter.
        """
        return [ # pylint: disable=unsubscriptable-object
            tinynmc.node.masks(self._nodes[i], request)
            for i in range(self._choices)
        ]

    def outcome(self, votes):
        """
        Perform computation to determine a share of the overall outcome.

        :param votes: Sequence of masked votes.
        """
        choices = len(votes[0])
        return [ # pylint: disable=unsubscriptable-object
            self._nodes[i].compute(self._signature, [vote_[i] for vote_ in votes])
            for i in range(choices)
        ]

class request(list):
    """
    Data structure for representing a request to submit a vote. A request can be
    submitted to each node to obtain corresponding masks for a vote.

    :param identifier: Integer identifying the requesting voter.

    The example below demonstrates how requests can be created.

    >>> request(identifier=1),
    ([(0, 1)],)
    >>> request(identifier=3),
    ([(0, 3)],)
    """
    def __init__(self, identifier):
        self.append((0, identifier))

class vote(list):
    """
    Data structure for representing a vote that can be broadcast to nodes.

    :param masks: Collection of masks to be applied to the vote choice.
    :param choice: Non-negative integer representing the vote choice.

    Suppose masks have already been obtained from the nodes via the steps
    below.

    >>> nodes = [node(), node(), node()]
    >>> preprocess(nodes, votes=4, choices=3)
    >>> identifier = 2
    >>> choice = 2
    >>> masks = [node.masks(request(identifier)) for node in nodes]

    This method can be used to mask the vote choice (in preparation for
    broadcasting it to the nodes).
    
    >>> isinstance(vote(masks, choice), vote)
    True
    """
    def __init__(self, masks, choice):
        """
        Create a masked vote choice that can be broadcast to nodes.
        """
        choices = len(masks[0])
        for i in range(choices):
            masks_i = [mask[i] for mask in masks]
            key = list(masks_i[0].keys())[0]
            coordinate_to_value = {}
            coordinate_to_value[key] = 2 if i == choice else 1
            self.append(tinynmc.masked_factors(coordinate_to_value, masks_i))

def preprocess(nodes, votes, choices):
    """
    Simulate a preprocessing workflow among the supplied nodes for a workflow
    that supports the specified number of votes and distinct choices (where
    choices are assumed to be integers greater than or equal to ``0`` and
    strictly less than the value ``choices``).

    :param nodes: Collection of nodes involved in the workflow.
    :param votes: Number of votes.
    :param choices: Number of distinct choices (from ``0`` to ``choices - 1``).

    The example below performs a preprocessing workflow involving three nodes.

    >>> nodes = [node(), node(), node()]
    >>> preprocess(nodes, votes=4, choices=3)
    """
    # pylint: disable=protected-access
    signature = [votes]

    for node_ in nodes:
        node_._signature = signature
        node_._choices = choices
        node_._nodes = [tinynmc.node() for _ in range(choices)]

    for i in range(choices):
        tinynmc.preprocess(signature, [node_._nodes[i] for node_ in nodes])

def reveal(shares):
    """
    Reconstruct the overall tally of votes from the shares obtained from each
    node.

    :param shares: Tally shares (where each share is a list of components,
        with one component per permitted price).

    Suppose the shares below are returned from the three nodes in a workflow.

    >>> from modulo import modulo
    >>> p = 4215209819
    >>> shares = [
    ...     [modulo(3, p), modulo(5, p), modulo(4, p)],
    ...     [modulo(1, p), modulo(2, p), modulo(9, p)],
    ...     [modulo(8, p), modulo(0, p), modulo(8, p)]
    ... ]

    This method combines such shares into an overall outcome by reconstructing
    the individual components and returning a list representing the a tally of
    the total number of votes for each choice.

    >>> reveal(shares)
    [3, 2, 4]
    """
    choices = len(shares[0])
    return [
        int(sum(share[i] for share in shares)).bit_length() - 1
        for i in range(choices)
    ]

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
