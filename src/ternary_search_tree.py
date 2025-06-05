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

    def __repr__(self) -> str:
        """
        Returns an ASCII representation of the ternary search tree.

        Each node is displayed with its character and '*' if it terminates a
        word. Children are shown with labeled branches: < (less), = (equal),
        and > (greater).

        Returns:
            str: the tree structure as a string.
        """
        lines = []

        def render(node: TreeNode | None, prefix: str = "", label: str = ""):
            if node is None:
                return

            node_repr = node.character + ("*" if node.terminates else "")
            lines.append(f"{prefix}{label}{node_repr}")
            indent = prefix + ("│  " if label else "   ")

            render(node.children.less_than, indent, "├─< ")
            render(node.children.equals, indent, "├─= ")
            render(node.children.larger_than, indent, "└─> ")

        render(self.root)
        return "\n".join(lines) if lines else "<empty tree>"

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

    def search(self, term: str, exact: bool = False) -> bool:
        """
        Searches for a string or prefix in the ternary search tree.

        Args:
            term (str): the string to search for.
            exact (bool): if True, checks for a full match (must terminate at
            the final node). If False, checks for a valid prefix match.

        Returns:
            bool: True if the term or prefix exists in the tree, False
            otherwise.
        """
        def _search(node: TreeNode | None, index: int) -> bool:
            if node is None:
                return False

            if term == "":
                character = ""
            else:
                character = term[index]

            if character < node.character:
                return _search(node.children.less_than, index)
            elif character > node.character:
                return _search(node.children.larger_than, index)
            else:
                if term == "":
                    return True
                elif index == len(term) - 1:
                    return node.terminates if exact else True
                return _search(node.children.equals, index + 1)

        if term == "" and not exact:
            return bool(len(self))

        return _search(self.root, 0)

    def all_strings(self) -> list[str]:
        """
        Retrieves all complete strings currently stored in the ternary search
        tree.

        This performs a full traversal of the tree and collects strings that
        terminate at valid nodes.

        Returns:
            list[str]: a list of all strings stored in the tree.
        """
        result = []

        def collect(node: TreeNode | None, path: str):
            if node is None:
                return

            collect(node.children.less_than, path)
            new_path = path + node.character

            if node.terminates:
                result.append(new_path)

            collect(node.children.equals, new_path)
            collect(node.children.larger_than, path)

        collect(self.root, "")
        return result
