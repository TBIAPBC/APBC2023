import numpy as np
import argparse as ap


def read_matrix(path):
    """
    Reads in the file that contains the cost matrix, the cost bound and the letters for the capitals.

    :param path: path to the matrix file
    :return: bound: cost bound, capitals: list of capitals, matrix: cost matrix as numpy array
    """
    with open(path, "r") as f:
        data = f.readlines()
        bound = int(data[0].split()[1])
        capitals = data[1].split()
        matrix = data[2:]
        matrix = [s.split() for s in matrix]
        matrix = np.array(matrix)
        return bound, capitals, matrix


class Tree:
    """
    Class for tree that can be built with different pairings of capitals
    """
    def __init__(self, bound, matrix, capitals, optimize):
        """

        :param bound: Initial cost bound
        :param matrix: Initital cost matrix
        :param capitals: List of capitals
        :param optimize: whether result should be optimized
        """
        self.root = Node(overall_cost=0, pairing=None, matrix=np.copy(matrix),
                         available_capitals=capitals)
        self.bound = [bound]
        self.matrix = matrix
        self.no_capitals = len(capitals)
        self.pairings = list()
        self.optimize = optimize

    def __str__(self):
        pairings = [" ".join(["".join(pair) for pair in pairing]) for pairing in self.pairings]
        return "\n".join(pairings)

    def build(self):
        """
        Builds up the tree by branching away from the root and collecting the pairings
        """
        self.root.branch(self.bound, self.optimize)
        self.pairings = self.get_pairings()

    def get_pairings(self):
        """
        :return: successfull pairings
        """
        all_pairings = list()
        self.traverse_nodes(self.root, all_pairings)
        return all_pairings

    def traverse_nodes(self, node, all_pairings, pairings=None):
        """
        Uses DFS to traverse to the leaves of the tree and collect all the pairings that contain all the capitals
        """
        if pairings is None:
            pairings = list()
        else:
            pairings.append(node.pairing)
        if not node.children:
            if len(pairings) == self.no_capitals / 2:
                all_pairings.append(pairings)
            return
        for child in node.children:
            self.traverse_nodes(child, all_pairings, list(pairings))


class Node:
    """
    The class Node represents a single pairing in the tree
    """
    def __init__(self, overall_cost, pairing, matrix, available_capitals):
        """

        :param overall_cost: cost of current plus previous pairings
        :param pairing: pair of capitals
        :param matrix: cost matrix without already chosen pairings
        :param available_capitals: capitals that are still available
        """
        self.pairing = pairing
        self.children = list()
        self.matrix = matrix
        self.overall_cost = overall_cost
        self.available_capitals = available_capitals

    def branch(self, bound, optimize):
        """
        Chooses feasible branches away from the current node
        :param bound: should bot be exceeded by overall cost
        :param optimize: whether to optimize solution
        :return: None
        """
        if self.matrix.shape == (0, 0):
            if optimize is True and self.overall_cost < bound[0]:
                bound[0] = self.overall_cost
            return
        row = self.matrix[0, :]
        self.traverse_row(row, bound, optimize)

    def traverse_row(self, row, bound, optimize):
        """
        Goes through values in current row, if a pairing is feasible it will be added as a child to the current node
        and new branches will be built from it (DFS)
        :param row: Current row of the cost matrix
        :param bound: should not be exceeded by overall cost
        :param optimize: whether to optimize
        """
        for column, value in enumerate(row):
            if value == "-":
                continue
            cost = self.overall_cost + int(value)
            updated_matrix = self.update_matrix(column)
            if cost > bound[0]:
                continue
            pairing = [self.available_capitals[0], self.available_capitals[column]]
            updated_capitals = self.update_capitals(column)
            child = Node(cost, pairing, updated_matrix, list(updated_capitals))
            self.children.append(child)
            child.branch(bound, optimize)

    def update_matrix(self, column):
        """
        Deletes the rows and columns if a pairing is no longer available
        :param column: column index of used capital
        :return: Updated matrix
        """
        updated_matrix = np.copy(self.matrix)
        updated_matrix = np.delete(updated_matrix, (0, column), axis=0)
        updated_matrix = np.delete(updated_matrix, (0, column), axis=1)
        return updated_matrix

    def update_capitals(self, column):
        """
        Deletes capitals that are no longer available
        :param column: column index of used capital
        :rtype: list
        """
        updated_capitals = list(self.available_capitals)
        updated_capitals.pop(0)
        updated_capitals.pop(column - 1)
        return updated_capitals


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Assignment Problem")
    parser.add_argument("path", help="path to file with cost matrix")
    parser.add_argument("-o", action="store_true", help="optimize solution")
    args = parser.parse_args()
    bound, capitals, cost_matrix = read_matrix(args.path)
    tree = Tree(bound, cost_matrix, capitals, args.o)
    tree.build()
    if not args.o:
        print(tree)
    else:
        print(tree.bound[0])
