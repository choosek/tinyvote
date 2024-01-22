"""
Minimal pure-Python library that demonstrates a basic encrypted
voting workflow via a secure multi-party computation (MPC)
`protocol <https://eprint.iacr.org/2023/1740>`__.
"""
from __future__ import annotations
from typing import Dict, List, Tuple, Sequence, Iterable
import doctest
from modulo import modulo
import tinynmc

class node:
    """
    Data structure for maintaining the information associated with a node
    and performing node operations.

    Suppose that a secure decentralized voting workflow is supported by three
    parties. The :obj:`node` objects would be instantiated locally by each of
    these three parties.

    >>> nodes = [node(), node(), node()]

    The preprocessing workflow that the nodes must execute can be simulated
    using the :obj:`preprocess` function. The number of voters that the
    workflow supports must be known, and it is assumed that all permitted
    choices are integers greater than or equal to ``0`` and strictly less
    than a fixed maximum value. The number of voters and the number of
    distinct choices must be supplied to the :obj:`preprocess` function.

    >>> preprocess(nodes, votes=4, choices=2)

    Each voter must then submit a request for the opportunity to submit their
    vote. The voters can create :obj:`request` instances for this purpose. In
    the example below, each of the four voters creates such a request.

    >>> request_zero = request(identifier=0)
    >>> request_one = request(identifier=1)
    >>> request_two = request(identifier=2)
    >>> request_three = request(identifier=3)

    Each voter can deliver their request to each node, and each node can then
    locally use its :obj:`masks` method to generate masks that can be returned
    to the requesting voter.

    >>> masks_zero = [node.masks(request_zero) for node in nodes]
    >>> masks_one = [node.masks(request_one) for node in nodes]
    >>> masks_two = [node.masks(request_two) for node in nodes]
    >>> masks_three = [node.masks(request_three) for node in nodes]

    Each voter can then generate locally a :obj:`vote` instance (*i.e.*, a
    masked vote choice).

    >>> vote_zero = vote(masks_zero, 0)
    >>> vote_one = vote(masks_one, 1)
    >>> vote_two = vote(masks_two, 1)
    >>> vote_three = vote(masks_three, 1)

    Every voter can broadcast its masked vote choice to all the nodes. Each
    node can locally assemble these as they arrive. Once a node has received
    all masked votes, it can determine its shares of the overall tally of the
    votes using the :obj:`outcome` method.

    >>> shares = [
    ...     node.outcome([vote_zero, vote_one, vote_two, vote_three])
    ...     for node in nodes
    ... ]

    The overall outcome can be reconstructed from the shares by the voting
    workflow operator using the :obj:`reveal` function. The outcome is
    represented as a :obj:`list` in which each entry contains the tally for
    the choice corresponding to the entry's index.

    >>> reveal(shares)
    [1, 3]
    """
    def __init__(self: node):
        """
        Create a node instance and instantiate its private attributes.
        """
        self._signature: List[int] = None
        self._choices: int = None
        self._nodes: List[tinynmc.node] = None

    def masks( # pylint: disable=redefined-outer-name
            self: node,
            request: Iterable[Tuple[int, int]]
        ) -> List[Dict[Tuple[int, int], modulo]]:
        """
        Return masks for a given request.

        :param request: Request from voter.
        """
        return [ # pylint: disable=unsubscriptable-object
            tinynmc.node.masks(self._nodes[i], request)
            for i in range(self._choices)
        ]

    def outcome(self: node, votes: Sequence[vote]) -> List[modulo]:
        """
        Perform computation to determine a share of the overall outcome.

        :param votes: Sequence of masked votes.
        """
        choices: int = len(votes[0])
        return [ # pylint: disable=unsubscriptable-object
            self._nodes[i].compute(self._signature, [vote_[i] for vote_ in votes])
            for i in range(choices)
        ]

class request(List[Tuple[int, int]]):
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
    def __init__(self: request, identifier: int):
        self.append((0, identifier))

class vote(List[Dict[Tuple[int, int], modulo]]):
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
    def __init__(
            self: vote,
            masks: List[List[Dict[Tuple[int, int], modulo]]],
            choice: int
        ):
        """
        Create a masked vote choice that can be broadcast to nodes.
        """
        choices: int = len(masks[0])
        for i in range(choices):
            masks_i = [mask[i] for mask in masks]
            key = list(masks_i[0].keys())[0]
            coordinate_to_value = {}
            coordinate_to_value[key] = 2 if i == choice else 1
            self.append(tinynmc.masked_factors(coordinate_to_value, masks_i))

def preprocess(nodes: Sequence[node], votes: int, choices: int):
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
    signature: List[int] = [votes]

    for node_ in nodes:
        node_._signature = signature
        node_._choices = choices
        node_._nodes = [tinynmc.node() for _ in range(choices)]

    for i in range(choices):
        tinynmc.preprocess(signature, [node_._nodes[i] for node_ in nodes])

def reveal(shares: List[List[modulo]]) -> List[int]:
    """
    Reconstruct the overall tally of votes from the shares obtained from each
    node.

    :param shares: Shares of overall outcome tally (where each share is a list
        of components, with one component per permitted choice).

    Suppose the shares below are returned from the three nodes in a workflow.

    >>> from modulo import modulo
    >>> p = 4215209819
    >>> shares = [
    ...     [modulo(3, p), modulo(5, p), modulo(4, p)],
    ...     [modulo(1, p), modulo(2, p), modulo(9, p)],
    ...     [modulo(8, p), modulo(0, p), modulo(8, p)]
    ... ]

    This method combines such shares into an overall outcome by reconstructing
    the individual components and returning a list representing a tally of the
    total number of votes for each choice.

    >>> reveal(shares)
    [3, 2, 4]
    """
    choices: int = len(shares[0])
    return [
        int(sum(share[i] for share in shares)).bit_length() - 1
        for i in range(choices)
    ]

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
