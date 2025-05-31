from dataclasses import dataclass


@dataclass
class TreeNodeChildren:
    less_than: "TreeNode | None" = None
    equals: "TreeNode | None" = None
    larger_than: "TreeNode | None" = None


class TreeNode:
    def __init__(self, character: str):
        self.character = character
        self.terminates = False
        self.children = TreeNodeChildren()

    @property
    def character(self) -> str:
        return self._character

    @character.setter
    def character(self, character: str):
        if len(character) > 1:  # allow empty string
            raise ValueError("input must be a character string")
        self._character = character

    @property
    def terminates(self) -> bool:
        return self._terminates

    @terminates.setter
    def terminates(self, terminates: bool):
        self._terminates = terminates

    @property
    def children(self) -> TreeNodeChildren:
        return self._children

    @children.setter
    def children(self, children: TreeNodeChildren):
        self._children = children


class TernarySearchTree:
    def __init__(self, root: TreeNode | None = None) -> None:
        self.root = root

    @property
    def root(self) -> TreeNode | None:
        return self._root

    @root.setter
    def root(self, node: TreeNode | None):
        self._root = node

    def __len__(self) -> int:
        """
        Calculates the number of complete strings stored in the ternary search
        tree.

        A string is considered stored if it terminates at a node marked as a
        terminal node.

        Returns:
            int: the number of distinct strings stored in the tree.
        """
        def count(node: TreeNode | None):
            if node is None:
                return 0

            total = int(node.terminates)
            total += count(node.children.less_than)
            total += count(node.children.equals)
            total += count(node.children.larger_than)
            return total

        return count(self.root)

    def insert(self, term: str) -> bool:
        """
        Inserts a string into the ternary search tree.

        All strings, including the empty string, are allowed.

        Args:
            term (str): the string to insert into the tree.

        Returns:
            bool: True if the string was inserted successfully, False
            otherwise.
        """
        def _insert(node, term, index):
            if term == "":
                character = ""
            else:
                character = term[index]

            if node is None:
                node = TreeNode(character)

            if character < node.character:
                node.children.less_than = _insert(
                    node.children.less_than,
                    term,
                    index
                )

            elif character > node.character:
                node.children.larger_than = _insert(
                    node.children.larger_than,
                    term,
                    index
                )

            else:
                if term == "":
                    node.terminates = True

                elif index + 1 == len(term):
                    node.terminates = True

                else:
                    node.children.equals = _insert(
                        node.children.equals,
                        term,
                        index + 1
                    )

            return node

        self.root = _insert(self.root, term, 0)
        return True
