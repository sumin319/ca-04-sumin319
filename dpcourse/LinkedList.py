class Node:
    """A node of a linked list"""

    def __init__(self, node_data):
        self._data = node_data
        self._next = None

    def get_data(self):
        """Get node data"""
        return self._data

    def set_data(self, node_data):
        """Set node data"""
        self._data = node_data

    data = property(get_data, set_data)

    def get_next(self):
        """Get next node"""
        return self._next

    def set_next(self, node_next):
        """Set next node"""
        self._next = node_next

    next = property(get_next, set_next)

    def __str__(self):
        """String"""
        return str(self._data)


class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
        element = self.head
        while element is not None:
            yield element
            element = element.next

    def __str__(self):
        result = "["
        element = self.head
        if element != None:
            result += str(element.data)
            element = element.next
            for i in range(self.size() - 1):
                result += ", " + str(element.data)
                element = element.next
        result += "]"
        return result

    def printlist(self):
        element = self.head
        while element is not None:
            print(element.data)
            element = element.next

    def is_empty(self):
        return self.head == None

    def add(self, item):
        temp = Node(item)
        temp.set_next(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.next

        return count

    def search(self, item):
        current = self.head
        while current is not None:
            if current.data == item:
                return True
            current = current.next

        return False

    def remove(self, item):
        current = self.head
        previous = None

        while current is not None:
            if current.data == item:
                break
            previous = current
            current = current.next

        if current is None:
            raise ValueError("{} is not in the list".format(item))
        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

    def append(self, item):
        current = self.head
        if self.head == None:
            self.head = Node(item)
        else:
            while current.next != None:
                current = current.next
            current.next = Node(item)