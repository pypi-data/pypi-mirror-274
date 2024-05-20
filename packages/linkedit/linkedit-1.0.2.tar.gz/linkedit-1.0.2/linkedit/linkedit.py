# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.abderrezzak@gmail.com>

"""Sophisticate Linked List"""

from tabulate import tabulate


def red(text: str) -> str:
    """Red Coloring Function"""
    return "\033[91;1m{}\033[00m".format(text)


def green(text: str) -> str:
    """Green Coloring Function"""
    return "\033[92;1m{}\033[00m".format(text)


def yellow(text: str) -> str:
    """Yellow Coloring Function"""
    return "\033[93;1m{}\033[00m".format(text)


def blue(text: str) -> str:
    """Blue Coloring Function"""
    return "\033[94;1m{}\033[00m".format(text)


def cyan(text: str) -> str:
    """Cyan Coloring Function"""
    return "\033[36;1m{}\033[00m".format(text)


def white(text: str) -> str:
    """White Coloring Function"""
    return "\033[37;1m{}\033[00m".format(text)


# for the background coloring
BG_RED: str = "\033[41m"
RESET: str = "\033[0m"


class linkedList:
    def __init__(
        self: "linkedList",
        data: int | float | complex | str | list | tuple | set | dict | None = None,
        *,
        circular: bool = False,
        detail: bool = False,
        base: int = 16,
        reverse: bool = False,
    ) -> None:
        """constructor special method"""
        self.circular: bool = circular
        self.detail: bool = detail
        if self.detail:
            self.base: int = base
        else:
            # if detail is not true we assign directely the default base 16 hexa
            self._base: int = base
        # O(1) len (track the object)
        self.len: int = 0
        self._tail: object | None = None
        self.head: object | None = data
        self.rev: bool = reverse

    def __len__(self: "linkedList") -> int:
        """length special method"""
        return self.len

    def __contains__(
        self: "linkedList",
        item: int | float | complex | str | list | tuple | set | dict | None,
    ) -> bool:
        head = self._head
        for _ in range(self.len):
            if head.data == item:
                return True
            head = head.next
        return False

    def __mul__(self: "linkedList", other: int) -> None:
        if not isinstance(other, int):
            raise ValueError("Unsupported operand type for *")
        if self.isEmpty:
            for _ in range(other):
                self.append(None)
            return self
        else:
            length = self.len
            for _ in range(other - 1):
                head = self._head
                for _ in range(length):
                    self.append(head.data)
                    head = head.next
            return self

    def __setitem__(
        self: "linkedList",
        index: int,
        value: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        self.node(index).data = value

    def __eq__(self, other) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            if id(self) == id(other):
                return True
            elif len(self) != len(other):
                return False
            elif len(self) == 0 and len(other) == 0:
                return True
            else:
                head1 = self._head
                head2 = other._head
                for _ in range(len(self)):
                    if head1.data == head2.data:
                        pass
                    else:
                        return False
                    head1 = head1.next
                    head2 = head2.next
                return True
        else:
            return False

    def __gt__(self, other) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            return len(self) > len(other)
        else:
            raise TypeError(
                f"'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __ge__(self, other) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            return len(self) >= len(other)
        else:
            raise TypeError(
                f"'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
            )

    @property
    def base(self: "linkedList") -> int:
        """base getter"""
        return self._base

    @base.setter
    def base(self: "linkedList", base: int) -> None:
        """base setter"""
        valid_bases: list = [2, 8, 10, 16]
        if not isinstance(base, int):
            # if the base is not an integer we keep the default base 16 hexa
            self._base: int = 16
            print(
                red("Warning")
                + white(" : Base must be integer, ")
                + red(f"{type(base)} ")
                + white("object not valid")
            )
        else:
            if base not in valid_bases:
                # if the base is not a valid base integer we keep the default base 16 hexa
                self._base: int = 16
                print(
                    red("Warning")
                    + white(" : Base must be one of these ")
                    + green("[")
                    + blue("2")
                    + white(", ")
                    + blue("8")
                    + white(", ")
                    + blue("10")
                    + white(", ")
                    + blue("16")
                    + green("]")
                    + white(", ")
                    + red(f"{base} ")
                    + white("not a valid base")
                )
            else:
                self._base: int = base

    def node(self: "linkedList", index: int) -> object:
        """node(s) searching method"""
        if not isinstance(index, int):
            if not self.circular:
                raise TypeError(
                    "non circular singly linked list indices must be integers"
                )
            else:
                raise TypeError("circular singly linked list indices must be integers")
        elif not self._head or index >= self.len:
            if not self.circular:
                raise IndexError("non circular singly linked list index out of range")
            else:
                raise IndexError("circular singly linked list index out of range")
        else:
            if index == 0:
                return self._head
            else:
                if index < 0:
                    if -index <= self.len:
                        index = self.len + index
                    else:
                        if not self.circular:
                            raise IndexError(
                                "non circular singly linked list index out of range"
                            )
                        else:
                            raise IndexError(
                                "circular singly linked list index out of range"
                            )
                head: object = self._head
                if index == self.len - 1:
                    return self._tail
                for _ in range(index):
                    head: object | None = head.next
                return head

    @property
    def tail(
        self: "linkedList",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        try:
            return self._tail
        except AttributeError as e1:
            pass
        if not self.circular:
            raise TypeError("Empty non circular singly linked list")
        else:
            raise TypeError("Empty circular singly linked list")

    @tail.deleter
    def tail(self: "linkedList") -> None:
        self._tail = None

    def isEmpty(self: "linkedList") -> bool:
        return not self._head

    def to_list(self: "linkedList", node: bool = False) -> list:
        head: object | None = self._head
        new_list: list = []
        for _ in range(self.len):
            if not node:
                new_list.append(head.data)
            else:
                new_list.append(head)
            head: object | None = head.next
        return new_list

    def index(
        self: "linkedList",
        value: int | float | complex | str | list | tuple | set | dict | None,
    ) -> int:
        """Return first index of value.

        Raises ValueError if the value is not present."""
        head: object | None = self._head
        for i in range(self.len):
            if head.data == value:
                return i
            head: object | None = head.next
        if not self.circular:
            error_msg: str = f"{value} is not in the non circular linked list"
            raise ValueError(error_msg)
        else:
            error_msg: str = f"{value} is not in the circular linked list"
            raise ValueError(error_msg)

    def clear(self: "linkedList") -> None:
        self._head: None = None
        self._tail: None = None
        self.len: int = 0

    def append(
        self: "linkedList",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """Append object to the end of the linked list."""
        self.insert(self.len, data)

    def remove(
        self: "linkedList",
        value: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """Remove first occurrence of value.

        Raises ValueError if the value is not present."""
        node_index: int = self.index(value)
        try:
            self.pop(node_index)
            return
        except IndexError as e2:
            pass
        if not self.circular:
            error_msg: str = f"{value} not in the non circular singly linked list"
            raise ValueError(error_msg)
        else:
            error_msg: str = f"{value} not in the circular singly linked list"
            raise ValueError(error_msg)

    # O(n log n) sort (Tim Sort => hybrid sorting algorithm = Merge Sort + Insertion Sort)
    def sort(self: "linkedList", *, reverse: bool = False) -> None:
        """Sort the linked list in ascending order and return None.

        The sort is in-place (i.e. the linked list itself is modified) and stable (i.e. the order of two equal elements is maintained).

        If a key function is given, apply it once to each linked list item and sort them, ascending or descending, according to their function values.

        The reverse flag can be set to sort in descending order."""
        non_sorted_list: list = []
        head: object | None = self._head
        if self.len >= 1:
            for _ in range(self.len - 1):
                if type(head.data) == type(head.next.data):
                    non_sorted_list.append(head.data)
                    head: object | None = head.next
                else:
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(head.next.data).__name__}'"
                    )
            non_sorted_list.append(head.data)
            non_sorted_list.sort(reverse=reverse)
            head: object = self._head
            for i in range(self.len):
                head.data = non_sorted_list[i]
                head: object | None = head.next

    def count(
        self: "linkedList",
        value: int | float | complex | str | list | tuple | set | dict | None,
    ) -> int:
        """Return number of occurrences of value."""
        head: object | None = self._head
        counter: int = 0
        if self.len >= 1:
            for _ in range(self.len):
                if head.data == value:
                    counter += 1
                head: object | None = head.next
            return counter

    def reverse(self: "linkedList") -> None:
        head: object | None = self._head
        elements: list = []
        for _ in range(self.len):
            elements.append(head.data)
            head: object | None = head.next
        head: object | None = self._head
        for i in range(1, self.len + 1):
            head.data = elements[-i]
            head: object | None = head.next

    def right_shift(self: "linkedList", rotate: int) -> None:
        if not isinstance(rotate, int):
            raise TypeError("rotate must be an integer")
        helper1: list = []
        helper2: list = []
        head: object | None = self._head
        try:
            rotate: int = rotate % self.len
        except ZeroDivisionError as e3:
            return
        for _ in range(self.len - rotate):
            helper1.append(head.data)
            head: object | None = head.next
        for _ in range(self.len - rotate, self.len):
            helper2.append(head.data)
            head: object | None = head.next
        head: object | None = self._head
        helper2.extend(helper1)
        for i in range(self.len):
            head.data = helper2[i]
            head: object | None = head.next

    def left_shift(self: "linkedList", rotate: int) -> None:
        if not isinstance(rotate, int):
            raise TypeError("rotate must be an integer")
        helper1: list = []
        helper2: list = []
        head: object | None = self._head
        try:
            rotate: int = rotate % self.len
        except ZeroDivisionError as e4:
            return
        for _ in range(rotate):
            helper1.append(head.data)
            head: object | None = head.next
        for _ in range(rotate, self.len):
            helper2.append(head.data)
            head: object | None = head.next
        head: object | None = self._head
        helper2.extend(helper1)
        for i in range(self.len):
            head.data = helper2[i]
            head: object | None = head.next

    def prepend(
        self: "linkedList",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        self.insert(0, data)


class singlyLinkedListNode:
    def __init__(
        self: "singlyLinkedListNode",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> object:
        self.data: int | float | complex | str | list | tuple | set | dict | None = data
        self.next: object | None = None

    def get_data(
        self: "singlyLinkedListNode",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        return self.data

    def next_node(self: "singlyLinkedListNode") -> object:
        return self.next


class singlyLinkedList(linkedList):
    @property
    def head(
        self: "singlyLinkedList",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        try:
            return self._head
        except AttributeError as e5:
            pass
        if not self.circular:
            raise TypeError("Empty non circular singly linked list")
        else:
            raise TypeError("Empty circular singly linked list")

    @head.setter
    def head(
        self: "singlyLinkedList",
        data: int | float | str | complex | list | tuple | set | dict | None,
    ) -> None:
        self._head: None = None
        if isinstance(data, singlyLinkedList):
            self._head: object | None = data._head
        elif isinstance(data, singlyLinkedListNode):
            old_head: object = data
            old_self_head: object = data
            new_head: object = singlyLinkedListNode(data.data)
            self._head: object = new_head
            self.len += 1
            old_head: object | None = old_head.next
            while old_head and old_head != old_self_head:
                new_node: object = singlyLinkedListNode(old_head.data)
                self.len += 1
                new_head.next = new_node
                new_head: object | None = new_head.next
                old_head: object | None = old_head.next
            if self.circular:
                new_node.next = self._head
            self._tail: object = new_node
        else:
            try:
                if len(data) > 0:
                    for i in data:
                        self.append(i)
            except TypeError as e6:
                if data is not None:
                    new_node: object = singlyLinkedListNode(data)
                    self.len += 1
                    self._head: object = new_node
                    if self.circular:
                        new_node.next = new_node
                    self._tail: object = new_node

    @head.deleter
    def head(self: "singlyLinkedList") -> None:
        self._head = None

    def copy(self: "singlyLinkedList") -> "singlyLinkedList":
        """Return a shallow copy of the non circular/circular singly linked list."""
        return singlyLinkedList(
            self._head,
            detail=self.detail,
            circular=self.circular,
            base=self._base,
        )

    def set_circular(self: "singlyLinkedList") -> None:
        self._tail.next = self._head
        self.circular: bool = True

    def set_non_circular(self: "singlyLinkedList") -> None:
        self._tail.next = None
        self.circular: bool = False

    def __add__(
        self: "singlyLinkedList",
        other: object | int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        helper: list = []
        head1: object | None = self._head
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            head2: object | None = other._head
        else:
            other: object = singlyLinkedList(other)
            head2: object = other._head
        for _ in range(self.len):
            helper.append(head1.data)
            head1: object | None = head1.next
        for _ in range(other.len):
            helper.append(head2.data)
            head2: object | None = head2.next
        return singlyLinkedList(helper, circular=other.circular)

    def __str__(self: "singlyLinkedList") -> str:
        """Return str(self)."""
        if not self._head:
            if not self.circular:
                raise TypeError("Empty non circular singly linked list")
            else:
                raise TypeError("Empty circular singly linked list")
        else:
            head: object = self._head
            linked_list: list = []
            counter: int = 0
            if not self.detail:
                while head and head.next != self._head:
                    if isinstance(head.data, str):
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}] -> ")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}'] -> ")
                        else:
                            linked_list.append(f'["{head.data}"] -> ')
                    else:
                        linked_list.append(f"[{head.data}] -> ")
                    head: object | None = head.next
                if not self.circular:
                    linked_list.append("None (NULL)")
                else:
                    linked_list.insert(0, "> ")
                    if isinstance(head.data, str):
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}]")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}']")
                        else:
                            linked_list.append(f'["{head.data}"]')
                    else:
                        linked_list.append(f"[{head.data}]")
                    linked_list.append(" -")
                return "".join(linked_list)
            else:
                linked_list.append(
                    [
                        white("current value"),
                        white("current value ") + green("@") + white("ddress"),
                        white("next value"),
                        white("next value ") + green("@") + white("ddress"),
                    ]
                )
                if head.next == self._head:
                    linked_list.append(
                        [
                            (
                                blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            cyan(
                                f"{bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head))}"
                            ),
                            (
                                blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            ),
                            cyan(
                                f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                            ),
                        ]
                    )
                elif not head.next:
                    linked_list.append(
                        [
                            (
                                blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            cyan(
                                f"{bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head))}"
                            ),
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}",
                            yellow(
                                f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))} "
                            )
                            + white("(")
                            + red("nil")
                            + white("/")
                            + (
                                red("0b0")
                                if self._base == 2
                                else (
                                    red("0o0")
                                    if self._base == 8
                                    else (red("0") if self._base == 10 else red("0x0"))
                                )
                            )
                            + white(")"),
                        ]
                    )
                    head: object | None = head.next
                else:
                    linked_list.append(
                        [
                            (
                                blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            f"{cyan(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}",
                            (
                                blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            ),
                            f"{yellow(bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next)))}",
                        ]
                    )
                    head: object | None = head.next
                    while head and head.next != self._head:
                        first: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        second: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                            + (" " if head.next is None else "")
                        )
                        try:
                            after: str = (
                                blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            )
                        except AttributeError as e7:
                            after: str = (
                                f"{blue('None')} {green('(')}{red('NULL')}{green(')')}"
                            )
                        linked_list.append(
                            [
                                (
                                    blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                yellow(first) if counter % 2 == 0 else red(first),
                                after,
                                (
                                    (
                                        red(second)
                                        + white("(")
                                        + green("nil")
                                        + white("/")
                                        + (
                                            green("0b0")
                                            if self._base == 2
                                            else (
                                                green("0o0")
                                                if self._base == 8
                                                else (
                                                    green("0")
                                                    if self._base == 10
                                                    else green("0x0")
                                                )
                                            )
                                        )
                                        + white(")")
                                        if second.endswith(" ")
                                        else red(second)
                                    )
                                    if counter % 2 == 0
                                    else (
                                        yellow(second)
                                        + white("(")
                                        + red("nil")
                                        + white("/")
                                        + (
                                            red("0b0")
                                            if self._base == 2
                                            else (
                                                red("0o0")
                                                if self._base == 8
                                                else (
                                                    red("0")
                                                    if self._base == 10
                                                    else red("0x0")
                                                )
                                            )
                                        )
                                        + white(")")
                                        if second.endswith(" ")
                                        else yellow(second)
                                    )
                                ),
                            ]
                        )
                        counter += 1
                        head: object | None = head.next
                    if self.circular:
                        first: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        second: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        )
                        linked_list.append(
                            [
                                (
                                    blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                yellow(first) if counter % 2 == 0 else red(first),
                                (
                                    blue(f"{head.next.data}")
                                    if not isinstance(head.next.data, str)
                                    else (
                                        blue(f"'{head.next.data}'")
                                        if len(head.next.data) == 1
                                        else (
                                            blue(f'"{head.next.data}"')
                                            if len(head.next.data) > 1
                                            else f"{head.next.data}"
                                        )
                                    )
                                ),
                                cyan(second),
                            ]
                        )
                if not self.circular:
                    linked_list.append(
                        [
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}",
                            (
                                (
                                    f"{yellow(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                    + white("(")
                                    + red("nil")
                                    + white("/")
                                    + (
                                        red("0b0")
                                        if self._base == 2
                                        else (
                                            red("0o0")
                                            if self._base == 8
                                            else (
                                                red("0")
                                                if self._base == 10
                                                else red("0x0")
                                            )
                                        )
                                    )
                                    + white(")")
                                )
                                if counter % 2 == 0
                                else (
                                    f"{red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                    + white("(")
                                    + green("nil")
                                    + white("/")
                                    + (
                                        green("0b0")
                                        if self._base == 2
                                        else (
                                            green("0o0")
                                            if self._base == 8
                                            else (
                                                green("0")
                                                if self._base == 10
                                                else green("0x0")
                                            )
                                        )
                                    )
                                    + white(")")
                                )
                            ),
                            BG_RED + " " * len("next value") + RESET,
                            BG_RED + " " * len("next value @ddress") + RESET,
                        ]
                    )
                return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    def insert(
        self: "singlyLinkedList",
        index: int,
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """Insert object before index."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            new_node: object = singlyLinkedListNode(data)
            self._head: object = new_node
            self.len += 1
            self._tail: object = new_node
            if self.circular:
                self._head.next = self._head
        else:
            if index == 0:
                new_node: object = singlyLinkedListNode(data)
                self.len += 1
                new_node.next = self._head
                if self.circular:
                    self._tail.next = new_node
                self._head: object = new_node
            elif index >= self.len:
                new_node: object = singlyLinkedListNode(data)
                self._tail.next = new_node
                if self.circular:
                    new_node.next = self._head
                self.len += 1
                self._tail: object = new_node
            else:
                if index < 0:
                    if index > -self.len:
                        index = self.len + index
                    else:
                        self.insert(0, data)
                        return
                new_node: object = singlyLinkedListNode(data)
                prev_head: object = self.node(index - 1)
                new_node.next = prev_head.next
                prev_head.next = new_node
                self.len += 1

    def pop(
        self: "singlyLinkedList", index: int = -1
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            if not self.circular:
                raise IndexError("pop from empty non circular singly linked list")
            else:
                raise IndexError("pop from empty circular singly linked list")
        else:
            head: object = self._head
            if index == 0 or index == -self.len:
                old_head_value: (
                    int | float | complex | str | list | tuple | set | dict | None
                ) = self._head.data
                old_head: object = self._head
                if not self.circular:
                    self._head: object = head.next
                    if self.len == 1:
                        self._tail: None = None
                    self.len -= 1
                else:
                    if self._head != head.next:
                        self._tail.next = head.next
                        self._head: object = head.next
                    else:
                        self._head: None = None
                        self._tail: None = None
                    self.len -= 1
                del old_head
                return old_head_value
            elif index == -1 or index == self.len - 1:
                prev_current: object = self.node(index - 1)
                removed_node_value: (
                    int | float | complex | str | list | tuple | set | dict | None
                ) = prev_current.next.data
                removed_node: object = prev_current.next
                if self.circular:
                    prev_current.next = self._head
                else:
                    prev_current.next = None
                self.len -= 1
                self._tail: object = prev_current
                del removed_node
                return removed_node_value
            elif index > self.len - 1 or index < -self.len:
                raise IndexError("pop index out of range")
            else:
                prev_node: object = self.node(index - 1)
                removed_node_value: (
                    int | float | complex | str | list | tuple | set | dict | None
                ) = prev_node.next.data
                removed_node: object = prev_node.next
                prev_node.next = prev_node.next.next
                self.len -= 1
                del removed_node
                return removed_node_value

    def extend(
        self: "singlyLinkedList",
        extended_object: (
            singlyLinkedListNode
            | int
            | float
            | complex
            | str
            | list
            | tuple
            | set
            | dict
            | None
        ),
    ) -> None:
        """Extend non circular/circular singly linked list by appending elements from the iterable."""
        if isinstance(extended_object, singlyLinkedList):
            first_last_node: object | None = self._tail
            second_first_node: object | None = extended_object._head
            for _ in range(extended_object.len):
                new_node: object = singlyLinkedListNode(second_first_node.data)
                first_last_node.next = new_node
                first_last_node: object = first_last_node.next
                second_first_node: object | None = second_first_node.next
            self.len += extended_object.len
            if self.circular:
                first_last_node.next = self._head
        else:
            extended_linked_list: object = singlyLinkedList(extended_object)
            self.extend(extended_linked_list)

    def __getitem__(
        self: "linkedList", index: int
    ) -> str | int | complex | float | list | tuple | set | dict | None:
        if not isinstance(index, slice):
            return self.node(index).data
        else:
            head: object | None = self._head
            new_list: list = []
            for _ in range(self.len):
                new_list.append(head.data)
                head: object | None = head.next
            try:
                new_list: list = new_list[index.start : index.stop : index.step]
                return singlyLinkedList(
                    new_list,
                    detail=self.detail,
                    circular=self.circular,
                    base=self._base,
                )
            except TypeError as e8:
                pass
            raise TypeError(
                "slice indices must be integers or None or have an __index__ method"
            )

    def to_doubly(self: "singlyLinkedList") -> object:
        return doublyLinkedList() + self

    def add(
        self: "singlyLinkedList",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """To add in an organized manner"""
        if not self._head:
            self._head: singlyLinkedListNode = singlyLinkedListNode(data)
            self.len += 1
            self._tail = self._head
            if self.circular:
                self._head.next = self._head
        else:
            head: singlyLinkedListNode = self._head
            prev_head: singlyLinkedListNode | None = None
            for i in range(self.len):
                if type(head.data) != type(data):
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(data).__name__}'"
                    )
                else:
                    if not self.rev:
                        if data < head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: singlyLinkedListNode = singlyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                prev_head.next = new_node
                                self.len += 1
                                break
                        else:
                            prev_head: singlyLinkedListNode = head
                            head = head.next
                    else:
                        if data > head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: singlyLinkedListNode = singlyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                prev_head.next = new_node
                                self.len += 1
                                break
                        else:
                            prev_head: singlyLinkedListNode = head
                            head: singlyLinkedListNode = head.next
            else:
                self.insert(self.len, data)

    def to_dict(self: "linkedList", node: bool = False) -> dict:
        head: object | None = self._head
        new_dict: dict = {}
        for _ in range(self.len):
            try:
                next_value: (
                    int | float | complex | str | list | tuple | set | dict | None
                ) = head.next.data
            except AttributeError as e9:
                next_value: None = None
            new_dict[head.data] = {
                "current value @ddress" if not node else "current node": (
                    (
                        (
                            bin(id(head))
                            if self._base == 2
                            else (
                                oct(id(head))
                                if self._base == 8
                                else id(head) if self._base == 10 else hex(id(head))
                            )
                        )
                    )
                    if not node
                    else head
                ),
                "next value" if not node else "next node value": next_value,
                "next value @ddress" if not node else "next node": (
                    (
                        bin(id(head.next))
                        if self._base == 2
                        else (
                            oct(id(head.next))
                            if self._base == 8
                            else (
                                id(head.next)
                                if self._base == 10
                                else hex(id(head.next))
                            )
                        )
                    )
                    if not node
                    else head.next
                ),
            }
            head: object | None = head.next
        return new_dict


class sll(singlyLinkedList):
    pass


class doublyLinkedListNode:
    def __init__(
        self: "doublyLinkedListNode",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> object:
        self.data: int | float | complex | str | list | tuple | set | dict | None = data
        self.prev: object | None = None
        self.next: object | None = None

    def get_data(
        self: "doublyLinkedListNode",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        return self.data

    def prev_node(self: "doublyLinkedListNode") -> object:
        return self.prev

    def next_node(self: "doublyLinkedListNode") -> object:
        return self.next


class doublyLinkedList(linkedList):
    @property
    def head(
        self: "linkedList",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        try:
            return self._head
        except AttributeError as e10:
            if not self.circular:
                raise TypeError("Empty non circular doubly linked list")
            else:
                raise TypeError("Empty circular doubly linked list")

    @head.setter
    def head(
        self: "doublyLinkedList",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        self._head: None = None
        if isinstance(data, doublyLinkedList):
            self._head: object | None = data._head
        elif isinstance(data, doublyLinkedListNode):
            old_head: object = data
            old_self_head: object = data
            new_head: object = doublyLinkedListNode(data.data)
            if self.circular:
                new_head.prev = data.prev
            self._head: object = new_head
            self.len += 1
            old_head: object | None = old_head.next
            while old_head and old_head != old_self_head:
                new_node: object = doublyLinkedListNode(old_head.data)
                self.len += 1
                new_head.next = new_node
                new_node.prev = new_head
                new_head: object | None = new_head.next
                old_head: object | None = old_head.next
            if self.circular:
                new_node.next = self._head
            self._tail: object = new_node
        else:
            try:
                if len(data) > 0:
                    for i in data:
                        self.append(i)
            except TypeError as e11:
                if data is not None:
                    new_node: object = doublyLinkedListNode(data)
                    self.len += 1
                    self._head: object = new_node
                    if self.circular:
                        new_node.next = new_node
                        new_node.prev = new_node
                    self._tail: object = new_node

    @head.deleter
    def head(self: "doublyLinkedList") -> None:
        self._head = None

    def set_circular(self: "doublyLinkedList") -> None:
        self._tail.next = self._head
        self._head.prev = self._tail
        self.circular: bool = True

    def set_non_circular(self: "doublyLinkedList") -> None:
        self._tail.next = None
        self._head.prev = None
        self.circular: bool = False

    def __add__(
        self: "doublyLinkedList",
        other: object | int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        helper: list = []
        head1: object | None = self._head
        if isinstance(other, doublyLinkedList) or isinstance(other, singlyLinkedList):
            head2: object | None = other._head
        else:
            other: object = doublyLinkedList(other)
            head2: object = other._head
        for _ in range(self.len):
            helper.append(head1.data)
            head1: object | None = head1.next
        for _ in range(other.len):
            helper.append(head2.data)
            head2: object | None = head2.next
        return doublyLinkedList(helper, circular=other.circular)

    def __str__(self: "doublyLinkedList") -> str:
        """Return str(self)."""
        if not self._head:
            if not self.circular:
                raise TypeError("Empty non circular doubly linked list")
            else:
                raise TypeError("Empty circular doubly linked list")
        else:
            head: object = self._head
            linked_list: list = []
            counter: int = 0
            if not self.detail:
                if not self.circular:
                    linked_list.append("None (NULL) <- ")
                else:
                    linked_list.append("=> ")
                while head and head.next != self._head:
                    if not isinstance(head.data, str):
                        linked_list.append(
                            f"[{head.data}] " + ("<=> " if head.next else "-> ")
                        )
                    else:
                        if len(head.data) == 0:
                            linked_list.append(
                                f"[{head.data}] " + ("<=> " if head.next else "-> ")
                            )
                        elif len(head.data) == 1:
                            linked_list.append(
                                f"['{head.data}'] " + ("<=> " if head.next else "-> ")
                            )
                        else:
                            linked_list.append(
                                f'["{head.data}"] ' + ("<=> " if head.next else "-> ")
                            )
                    head = head.next
                if not self.circular:
                    if self.len > 1:
                        linked_list.append("None (NULL)")
                    else:
                        try:
                            if not isinstance(head.data, str):
                                linked_list.append(f"[{head.data}] -> None (NULL)")
                            else:
                                if len(head.data) == 0:
                                    linked_list.append(f"[{head.data}] -> None (NULL)")
                                elif len(head.data) == 1:
                                    linked_list.append(
                                        f"['{head.data}'] -> None (NULL)"
                                    )
                                else:
                                    linked_list.append(
                                        f'["{head.data}"] -> None (NULL)'
                                    )
                        except AttributeError as e12:
                            linked_list.append("None (NULL)")
                else:
                    if not isinstance(head.data, str):
                        linked_list.append(f"[{head.data}] <=")
                    else:
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}] <=")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}'] <=")
                        else:
                            linked_list.append(f'["{head.data}"] <=')
                return "".join(linked_list)
            else:
                linked_list.append(
                    [
                        white("previous value"),
                        white("previous value ") + green("@") + white("ddress"),
                        white("current value"),
                        white("current value ") + green("@") + white("ddress"),
                        white("next value"),
                        white("next value ") + green("@") + white("ddress"),
                    ]
                )
                if not self.circular:
                    linked_list.append(
                        [
                            BG_RED + " " * len("previous value") + RESET,
                            BG_RED + " " * len("previous value @ddress") + RESET,
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}",
                            f"{yellow(bin(id(None)) if self._base == 2 else oct(id(None)) if self._base == 8 else id(None) if self._base == 10 else hex(id(None)))} "
                            + white("(")
                            + red("nil")
                            + white("/")
                            + (
                                red("0b0")
                                if self._base == 2
                                else (
                                    red("0o0")
                                    if self._base == 8
                                    else (red("0") if self._base == 10 else red("0x0"))
                                )
                            )
                            + white(")"),
                            BG_RED + " " * len("next value") + RESET,
                            BG_RED + " " * len("next value @ddress") + RESET,
                        ]
                    )
                try:
                    helper: (
                        int | float | complex | str | list | tuple | set | dict | None
                    ) = head.next.data
                except AttributeError as e13:
                    helper: None = None
                linked_list.append(
                    [
                        (
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}"
                            if not head.prev
                            else (
                                blue(f"{head.prev.data}")
                                if not isinstance(head.prev.data, str)
                                else (
                                    blue(f"'{head.prev.data}'")
                                    if len(head.prev.data) == 1
                                    else (
                                        blue(f'"{head.prev.data}"')
                                        if len(head.prev.data) > 1
                                        else f"{head.prev.data}"
                                    )
                                )
                            )
                        ),
                        f"{yellow(bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev)))} "
                        + (
                            white("(")
                            + red("nil")
                            + white("/")
                            + (
                                red("0b0")
                                if self._base == 2
                                else (
                                    red("0o0")
                                    if self._base == 8
                                    else (red("0") if self._base == 10 else red("0x0"))
                                )
                            )
                            + white(")")
                            if head.prev is None
                            else ""
                        ),
                        (
                            blue(f"{head.data}")
                            if not isinstance(head.data, str)
                            else (
                                blue(f"'{head.data}'")
                                if len(head.data) == 1
                                else (
                                    blue(f'"{head.data}"')
                                    if len(head.data) > 1
                                    else f"{head.data}"
                                )
                            )
                        ),
                        f"{red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}",
                        (
                            blue(
                                f"{helper}"
                                + f"{(green(' (') + red('NULL') + green(')')) if not helper else ''}"
                            )
                            if not isinstance(helper, str)
                            else (
                                blue(f"'{helper}'")
                                if len(head.next.data) == 1
                                else (
                                    blue(f'"{helper}"')
                                    if len(head.next.data) > 1
                                    else f"{helper}"
                                )
                            )
                        ),
                        (
                            f"{yellow(bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next)))} "
                            + (
                                white("(")
                                + red("nil")
                                + white("/")
                                + (
                                    red("0b0")
                                    if self._base == 2
                                    else (
                                        red("0o0")
                                        if self._base == 8
                                        else (
                                            red("0") if self._base == 10 else red("0x0")
                                        )
                                    )
                                )
                                + white(")")
                                if head.next is None
                                else ""
                            )
                        ),
                    ]
                )
                head: object | None = head.next
                while head and head.next != self._head:
                    first: str = (
                        f"{bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev))}"
                    )
                    second: str = (
                        f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                    )
                    last: str = (
                        f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        + (" " if head.next is None else "")
                    )
                    try:
                        after: str = (
                            blue(f"{head.next.data}")
                            if not isinstance(head.next.data, str)
                            else (
                                blue(f"'{head.next.data}'")
                                if len(head.next.data) == 1
                                else (
                                    blue(f'"{head.next.data}"')
                                    if len(head.next.data) > 1
                                    else f"{head.next.data}"
                                )
                            )
                        )
                    except AttributeError as e14:
                        after: str = (
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}"
                        )
                    linked_list.append(
                        [
                            (
                                blue(f"{head.prev.data}")
                                if not isinstance(head.prev.data, str)
                                else (
                                    blue(f"'{head.prev.data}'")
                                    if len(head.prev.data) == 1
                                    else (
                                        blue(f'"{head.prev.data}"')
                                        if len(head.prev.data) > 1
                                        else f"{head.prev.data}"
                                    )
                                )
                            ),
                            red(first) if counter % 2 == 0 else yellow(first),
                            (
                                blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            yellow(second) if counter % 2 == 0 else red(second),
                            after,
                            (
                                (
                                    red(last)
                                    + white("(")
                                    + yellow("nil")
                                    + white("/")
                                    + (
                                        yellow("0b0")
                                        if self._base == 2
                                        else (
                                            yellow("0o0")
                                            if self._base == 8
                                            else (
                                                yellow("0")
                                                if self._base == 10
                                                else yellow("0x0")
                                            )
                                        )
                                    )
                                    + white(")")
                                    if last.endswith(" ")
                                    else red(last)
                                )
                                if counter % 2 == 0
                                else (
                                    yellow(last)
                                    + white("(")
                                    + red("nil")
                                    + white("/")
                                    + (
                                        red("0b0")
                                        if self._base == 2
                                        else (
                                            red("0o0")
                                            if self._base == 8
                                            else (
                                                red("0")
                                                if self._base == 10
                                                else red("0x0")
                                            )
                                        )
                                    )
                                    + white(")")
                                    if last.endswith(" ")
                                    else yellow(last)
                                )
                            ),
                        ]
                    )
                    counter += 1
                    head: object | None = head.next
                if not self.circular:
                    linked_list.append(
                        [
                            BG_RED + " " * len("previous value") + RESET,
                            BG_RED + " " * len("previous value @ddress") + RESET,
                            f"{blue('None')} {green('(')}{red('NULL')}{green(')')}",
                            (
                                f"{yellow(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                + white("(")
                                + red("nil")
                                + white("/")
                                + (
                                    red("0b0")
                                    if self._base == 2
                                    else (
                                        red("0o0")
                                        if self._base == 8
                                        else (
                                            red("0") if self._base == 10 else red("0x0")
                                        )
                                    )
                                )
                                + white(")")
                                if counter % 2 == 0
                                else f"{red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                + white("(")
                                + yellow("nil")
                                + white("/")
                                + (
                                    yellow("0b0")
                                    if self._base == 2
                                    else (
                                        yellow("0o0")
                                        if self._base == 8
                                        else (
                                            yellow("0")
                                            if self._base == 10
                                            else yellow("0x0")
                                        )
                                    )
                                )
                                + white(")")
                            ),
                            BG_RED + " " * len("next value") + RESET,
                            BG_RED + " " * len("next value @ddress") + RESET,
                        ]
                    )
                else:
                    if self.len != 1:
                        first: str = (
                            f"{bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev))}"
                        )
                        second: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        last: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        )
                        after: str = (
                            blue(f"{head.next.data}")
                            if not isinstance(head.next.data, str)
                            else (
                                blue(f"'{head.next.data}'")
                                if len(head.next.data) == 1
                                else (
                                    blue(f'"{head.next.data}"')
                                    if len(head.next.data) > 1
                                    else f"{head.next.data}"
                                )
                            )
                        )
                        linked_list.append(
                            [
                                (
                                    blue(f"{head.prev.data}")
                                    if not isinstance(head.prev.data, str)
                                    else (
                                        blue(f"'{head.prev.data}'")
                                        if len(head.prev.data) == 1
                                        else (
                                            blue(f'"{head.prev.data}"')
                                            if len(head.prev.data) > 1
                                            else f"{head.prev.data}"
                                        )
                                    )
                                ),
                                red(first) if counter % 2 == 0 else yellow(first),
                                (
                                    blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                yellow(second) if counter % 2 == 0 else red(second),
                                after,
                                red(last) if counter % 2 == 0 else yellow(last),
                            ]
                        )
                return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    def copy(self: "doublyLinkedList") -> "doublyLinkedList":
        """Return a shallow copy of a non circular/circular doubly linked list."""
        return doublyLinkedList(
            self._head,
            detail=self.detail,
            circular=self.circular,
            base=self._base,
        )

    def __getitem__(
        self: "linkedList", index: int
    ) -> str | int | complex | float | list | tuple | set | dict | None:
        if not isinstance(index, slice):
            return self.node(index).data
        else:
            head: object | None = self._head
            new_list: list = []
            for _ in range(self.len):
                new_list.append(head.data)
                head: object | None = head.next
            try:
                new_list: list = new_list[index.start : index.stop : index.step]
                return doublyLinkedList(
                    new_list,
                    detail=self.detail,
                    circular=self.circular,
                    base=self._base,
                )
            except TypeError as e15:
                pass
            raise TypeError(
                "slice indices must be integers or None or have an __index__ method"
            )

    def insert(
        self: "doublyLinkedList",
        index: int,
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """Insert object before index."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            new_node: object = doublyLinkedListNode(data)
            self._head: object = new_node
            self._tail: object = new_node
            self.len: int = 1
            if self.circular:
                new_node.next = new_node
                new_node.prev = new_node
        else:
            if index >= self.len:
                new_node: object = doublyLinkedListNode(data)
                self._tail.next = new_node
                new_node.prev = self._tail
                self._tail: object = new_node
                if self.circular:
                    self._tail.next = self._head
                    self._head.prev = self._tail
                self.len += 1
            elif index <= -self.len or index == 0:
                new_node: object = doublyLinkedListNode(data)
                new_node.next = self._head
                self._head.prev = new_node
                self._head: object = new_node
                if self.circular:
                    self._head.prev = self._tail
                    self._tail.next = self._head
                self.len += 1
            else:
                current: object = self.node(index)
                new_node: object = doublyLinkedListNode(data)
                new_node.prev = current.prev
                new_node.next = current
                current.prev.next = new_node
                current.prev = new_node
                self.len += 1

    def pop(
        self: "doublyLinkedList", index: int = -1
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            if not self.circular:
                raise IndexError("pop from empty non circular doubly linked list")
            else:
                raise IndexError("pop from empty circular doubly linked list")
        else:
            if self.len > 1:
                if index == -1 or index == self.len - 1:
                    returned_value: (
                        int | float | complex | str | list | tuple | set | dict | None
                    ) = self._tail.data
                    removed_node = self._tail
                    self._tail: object = self._tail.prev
                    if self.circular:
                        self._tail.next = self._head
                        self._head.prev = self._tail
                    else:
                        self._tail.next = None
                    self.len -= 1
                    del removed_node
                    return returned_value
                elif index == 0 or index == -self.len:
                    returned_value: (
                        int | float | complex | str | list | tuple | set | dict | None
                    ) = self._head.data
                    removed_node = self._head
                    self._head: object = self._head.next
                    if self.circular:
                        self._head.prev = self._tail
                        self._tail.next = self._head
                    else:
                        self._head.prev = None
                    self.len -= 1
                    del removed_node
                    return returned_value
                elif index >= self.len or index < -self.len:
                    raise IndexError("pop index out of range")
                else:
                    current: object = self.node(index)
                    returned_value: (
                        int | float | complex | str | list | tuple | set | dict | None
                    ) = current.data
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.len -= 1
                    del current
                    return returned_value
            else:
                if index == 0 or index == -1:
                    returned_value: (
                        int | float | complex | str | list | tuple | set | dict | None
                    ) = self._head.data
                    removed_node = self._head
                    self._head: None = None
                    self._tail: None = None
                    self.len: int = 0
                    del removed_node
                    return returned_value
                else:
                    raise IndexError("pop index out of range")

    def extend(
        self: "doublyLinkedList",
        extended_object: (
            doublyLinkedListNode
            | int
            | float
            | complex
            | str
            | list
            | tuple
            | set
            | dict
            | None
        ),
    ) -> None:
        """Extend non circular/circular doubly linked list by appending elements from the iterable."""
        if isinstance(extended_object, doublyLinkedList):
            first_last_node: object | None = self._tail
            second_first_node: object | None = extended_object._head
            for _ in range(extended_object.len):
                new_node: object = doublyLinkedListNode(second_first_node.data)
                first_last_node.next = new_node
                new_node.prev = first_last_node
                first_last_node: object = first_last_node.next
                second_first_node: object | None = second_first_node.next
            self.len += extended_object.len
            if self.circular:
                first_last_node.next = self._head
                self._head.prev = first_last_node
        else:
            extended_linked_list: object = doublyLinkedList(extended_object)
            self.extend(extended_linked_list)

    def to_singly(self: "doublyLinkedList") -> object:
        return singlyLinkedList() + self

    def add(
        self: "doublyLinkedList",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        """To add in an organized manner"""
        if not self._head:
            self._head: doublyLinkedListNode = doublyLinkedListNode(data)
            self.len += 1
            self._tail = self._head
            if self.circular:
                self._head.next = self._head
                self._head.prev = self._head
        else:
            head: doublyLinkedListNode = self._head
            for i in range(self.len):
                if type(head.data) != type(data):
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(data).__name__}'"
                    )
                else:
                    if not self.rev:
                        if data < head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: doublyLinkedListNode = doublyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                new_node.prev = head.prev
                                head.prev.next = new_node
                                head.prev = new_node
                                self.len += 1
                                break
                        else:
                            head = head.next
                    else:
                        if data > head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: doublyLinkedListNode = doublyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                new_node.prev = head.prev
                                head.prev.next = new_node
                                head.prev = new_node
                                self.len += 1
                                break
                        else:
                            head = head.next
            else:
                self.insert(self.len, data)

    def to_dict(self: "linkedList", node: bool = False) -> dict:
        head: object | None = self._head
        new_dict: dict = {}
        for _ in range(self.len):
            try:
                next_value: (
                    int | float | complex | str | list | tuple | set | dict | None
                ) = head.next.data
            except AttributeError as e16:
                next_value: None = None
            new_dict[head.data] = {
                "prev value" if not node else "prev node value": (
                    (head.prev.data if head.prev is not None else None)
                    if not node
                    else head.prev.data if head.prev is not None else None
                ),
                "prev value @ddress" if not node else "prev node @ddress": (
                    (
                        bin(id(head.prev))
                        if self._base == 2
                        else (
                            oct(id(head.prev))
                            if self._base == 8
                            else (
                                id(head.prev)
                                if self._base == 10
                                else hex(id(head.prev))
                            )
                        )
                    )
                    if not node
                    else head.prev
                ),
                "current value @ddress" if not node else "current node": (
                    (
                        (
                            bin(id(head))
                            if self._base == 2
                            else (
                                oct(id(head))
                                if self._base == 8
                                else id(head) if self._base == 10 else hex(id(head))
                            )
                        )
                    )
                    if not node
                    else head
                ),
                "next value" if not node else "next node value": next_value,
                "next value @ddress" if not node else "next node": (
                    (
                        bin(id(head.next))
                        if self._base == 2
                        else (
                            oct(id(head.next))
                            if self._base == 8
                            else (
                                id(head.next)
                                if self._base == 10
                                else hex(id(head.next))
                            )
                        )
                    )
                    if not node
                    else head.next
                ),
            }
            head: object | None = head.next
        return new_dict


class dll(doublyLinkedList):
    pass


class orthogonalLinkedListNode:
    def __init__(
        self: "orthogonalLinkedListNode",
        data: int | float | complex | str | list | tuple | set | dict | None,
    ) -> object:
        self.prev = None
        self.next = None
        self.up = None
        self.down = None
        self.data = data

    def prev_node(self: "orthogonalLinkedListNode") -> object:
        return self.prev

    def next_node(self: "orthogonalLinkedListNode") -> object:
        return self.next

    def up_node(self: "orthogonalLinkedListNode") -> object:
        return self.up

    def down_node(self: "orthogonalLinkedListNode") -> object:
        return self.down

    def get_data(
        self: "orthogonalLinkedListNode",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        return self.data


class orthogonalLinkedList:
    def __init__(
        self: "orthogonalLinkedList",
        data: list,
        *,
        circular: bool = False,
        detail: bool = False,
    ) -> None:
        self.circular = circular
        self.detail = detail
        self.head = data

    @property
    def tail(
        self: "orthogonalLinkedList",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        return self._head[-1][-1]

    def __len__(self: "orthogonalLinkedList") -> int:
        return len(self._head) * len(self._head[0])

    @property
    def shape(self: "orthogonalLinkedList") -> tuple[int, int]:
        return (len(self._head), len(self._head[0]))

    def __getitem__(self, index):
        values = []
        for i in range(len(self._head[index])):
            values.append(self._head[index][i].data)
        return values

    def __setitem__(
        self: "orthogonalLinkedList",
        index: int,
        value: int | float | complex | str | list | tuple | set | dict | None,
    ) -> None:
        if len(value) == len(self._head[index]):
            for i in range(len(self._head[index])):
                self._head[index][i].data = value[i]
        else:
            raise TypeError("columns len not the same")

    @property
    def head(
        self: "orthogonalLinkedList",
    ) -> int | float | complex | str | list | tuple | set | dict | None:
        return self._head[0][0]

    @head.setter
    def head(self: "orthogonalLinkedList", data: list) -> None:
        if isinstance(data, list):
            som = 0
            for i in range(len(data)):
                try:
                    som += len(data[i])
                except TypeError as e17:
                    raise TypeError("just 2D array(list) allowed") from None
            if som % len(data):
                raise TypeError("2D array(list) columns is not with the same length")
            else:
                data[0][0] = orthogonalLinkedListNode(data[0][0])
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        if i == 0:
                            try:
                                data[i][j + 1] = orthogonalLinkedListNode(
                                    data[i][j + 1]
                                )
                            except IndexError as e18:
                                pass
                        try:
                            data[i + 1][j] = orthogonalLinkedListNode(data[i + 1][j])
                        except IndexError as e19:
                            pass
                        if i == 0:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e20:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            try:
                                data[i][j].down = data[i + 1][j]
                            except IndexError as e21:
                                pass
                        elif i == len(data) - 1:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e22:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            data[i][j].up = data[i - 1][j]
                        else:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e23:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            data[i][j].up = data[i - 1][j]
                            data[i][j].down = data[i + 1][j]
                if self.circular:
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            if data[i][j].prev is None:
                                data[i][j].prev = data[i][-1]
                            if data[i][j].next is None:
                                data[i][j].next = data[i][0]
                            if data[i][j].up is None:
                                data[i][j].up = data[-1][j]
                            if data[i][j].down is None:
                                data[i][j].down = data[0][j]
                self._head = data
        else:
            raise TypeError("just array(list) data type allowed")

    def __str__(self: "orthogonalLinkedList") -> str:
        linked_list = []
        if not self.detail:
            if not self.circular:
                linked_list.append(["None"] * (len(self._head[0]) + 2))
                linked_list[0][0], linked_list[0][-1] = "", ""
            for i in range(len(self._head)):
                helper = []
                if not self.circular:
                    helper.append("None")
                for j in range(len(self._head[i])):
                    if not isinstance(self._head[i][j].data, str):
                        helper.append(self._head[i][j].data)
                    else:
                        if len(self._head[i][j].data) == 0:
                            helper.append(self._head[i][j].data)
                        elif len(self._head[i][j].data) == 1:
                            helper.append(f"'{self._head[i][j].data}'")
                        else:
                            helper.append(f'"{self._head[i][j].data}"')
                if not self.circular:
                    helper.append("None")
                linked_list.append(helper)
            if not self.circular:
                linked_list.append(["None"] * (len(self._head[0]) + 2))
                linked_list[-1][0], linked_list[-1][-1] = "", ""
            return tabulate(linked_list, tablefmt="fancy_grid")
        else:
            counter = 0
            linked_list.append(
                [
                    white("up"),
                    white("up ") + green("@"),
                    white("previous"),
                    white("previous ") + green("@"),
                    white("current"),
                    white("current ") + green("@"),
                    white("down"),
                    white("down ") + green("@"),
                    white("next"),
                    white("next ") + green("@"),
                ]
            )
            for i in range(len(self._head)):
                for j in range(len(self._head[i])):
                    try:
                        if not isinstance(self._head[i][j].prev.data, str):
                            prev_data = blue(f"{self._head[i][j].prev.data}")
                        else:
                            if len(self._head[i][j].prev.data) == 0:
                                prev_data = self._head[i][j].prev.data
                            elif len(self._head[i][j].prev.data) == 1:
                                prev_data = blue(f"'{self._head[i][j].prev.data}'")
                            else:
                                prev_data = blue(f'"{self._head[i][j].prev.data}"')
                    except AttributeError as e24:
                        prev_data = blue("None")
                    try:
                        if not isinstance(self._head[i][j].next.data, str):
                            next_data = blue(f"{self._head[i][j].next.data}")
                        else:
                            if len(self._head[i][j].next.data) == 0:
                                next_data = self._head[i][j].next.data
                            elif len(self._head[i][j].next.data) == 1:
                                next_data = blue(f"'{self._head[i][j].next.data}'")
                            else:
                                next_data = blue(f'"{self._head[i][j].next.data}"')
                    except AttributeError as e25:
                        next_data = blue("None")
                    try:
                        if not isinstance(self._head[i][j].up.data, str):
                            up_data = blue(f"{self._head[i][j].up.data}")
                        else:
                            if len(self._head[i][j].up.data) == 0:
                                up_data = self._head[i][j].up.data
                            elif len(self._head[i][j].up.data) == 1:
                                up_data = blue(f"'{self._head[i][j].up.data}'")
                            else:
                                up_data = blue(f'"{self._head[i][j].up.data}"')
                    except AttributeError as e26:
                        up_data = blue("None")
                    try:
                        if not isinstance(self._head[i][j].down.data, str):
                            down_data = blue(f"{self._head[i][j].down.data}")
                        else:
                            if len(self._head[i][j].down.data) == 0:
                                down_data = self._head[i][j].down.data
                            elif len(self._head[i][j].down.data) == 1:
                                down_data = blue(f"'{self._head[i][j].down.data}'")
                            else:
                                down_data = blue(f'"{self._head[i][j].down.data}"')
                    except AttributeError as e27:
                        down_data = blue("None")
                    current_data = (
                        blue(f"{self._head[i][j].data}")
                        if not isinstance(self._head[i][j].data, str)
                        else (
                            self._head[i][j].data
                            if len(self._head[i][j].data) == 0
                            else (
                                blue(f"'{self._head[i][j].data}'")
                                if len(self._head[i][j].data) == 1
                                else blue(f'"{self._head[i][j].data}"')
                            )
                        )
                    )
                    up_add = (
                        (
                            yellow(f"{hex(id(self._head[i][j].up))}")
                            if counter % 2 == 0
                            else red(f"{hex(id(self._head[i][j].up))}")
                        )
                        if self._head[i][j].up is not None
                        else cyan(f"{hex(id(self._head[i][j].up))}")
                    )
                    counter += 1
                    prev_add = (
                        (
                            yellow(f"{hex(id(self._head[i][j].prev))}")
                            if counter % 2 == 0
                            else red(f"{hex(id(self._head[i][j].prev))}")
                        )
                        if self._head[i][j].prev is not None
                        else cyan(f"{hex(id(self._head[i][j].prev))}")
                    )
                    counter += 1
                    current_add = (
                        (
                            yellow(f"{hex(id(self._head[i][j]))}")
                            if counter % 2 == 0
                            else red(f"{hex(id(self._head[i][j]))}")
                        )
                        if self._head[i][j] is not None
                        else cyan(f"{hex(id(self._head[i][j]))}")
                    )
                    counter += 1
                    down_add = (
                        (
                            yellow(f"{hex(id(self._head[i][j].down))}")
                            if counter % 2 == 0
                            else red(f"{hex(id(self._head[i][j].down))}")
                        )
                        if self._head[i][j].down is not None
                        else cyan(f"{hex(id(self._head[i][j].down))}")
                    )
                    counter += 1
                    next_add = (
                        (
                            yellow(f"{hex(id(self._head[i][j].next))}")
                            if counter % 2 == 0
                            else red(f"{hex(id(self._head[i][j].next))}")
                        )
                        if self._head[i][j].next is not None
                        else cyan(f"{hex(id(self._head[i][j].next))}")
                    )
                    counter += 1
                    linked_list.append(
                        [
                            up_data,
                            up_add,
                            prev_data,
                            prev_add,
                            current_data,
                            current_add,
                            down_data,
                            down_add,
                            next_data,
                            next_add,
                        ]
                    )
            return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    @property
    def node(self: "orthogonalLinkedList") -> list:
        return self._head


class oll(orthogonalLinkedList):
    pass


def main() -> None:
    print("linkedit")


if __name__ == "__main__":
    main()
