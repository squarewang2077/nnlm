class DoublyListNode:
    def __init__(self):
        '''
        The attribution of the dll nodes are created more flexible, the dll node here is to store the info 
        '''
        self.next = None
        self.prev = None

    def __str__(self) -> str:
        # Get a list of attribute names excluding 'next' and 'prev'
        attrs = {k: v for k, v in self.__dict__.items() if k not in ['next', 'prev']}
        
        # Check if any attributes exist besides 'next' and 'prev'
        if attrs:
            # Join attribute names and values into a string representation
            return ', '.join(f"{key}: {value}" for key, value in attrs.items())
        else:
            return 'None'

class DoublyLinkedList:
    '''
    Note that all methods are worked on the defined dll nodes. The DLL will manage the dll nodes from a very high level without intervening the inside of the node 
    '''
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        """
        Make the DoublyLinkedList iterable.
        This method will return an iterator object (the list itself), 
        which starts iteration from the head.
        """
        self._current = self.head  # Start from the head
        return self  # Return the iterator object (self in this case)

    def __next__(self):
        """
        This method is called by the iterator to get the next item.
        """
        if self._current is None:  # If there are no more items
            raise StopIteration
        else:
            node = self._current  # Store current node
            self._current = self._current.next  # Move to the next node
            return node  # Return the current node

    def append(self, node):
        if self.head is not None: # if the linkedlist is not empty
            # establish the connection 
            self.tail.next = node 
            node.prev = self.tail
            # move the tail pointer
            self.tail = node
        else: # if the linkedlist is empty
            self.head = node
            self.tail = node

    def insert_after(self, node, new_node):
        # establish the connection from the new node
        new_node.prev = node
        new_node.next = node.next
        # establish the connection from prev and next nodes 
        node.next = new_node
        if node.next is not None: # if the node is not tail 
            node.next.prev = new_node
        else: # if the node is the tail node
            assert node == self.tail, "DoublyLinkedList->insert_after->The node needs to be the tail node"
            # move the tail pointer
            self.tail = new_node

    def delete(self, node):
        # short cut from the prev node
        if node.prev is not None: # if the node is not head
            # short cut the connect 
            node.prev.next = node.next
        else: # if the node is head
            assert node == self.head, "DoublyLinkedList->delete->The node needs to be the head node"
            # move the head pointer 
            self.head = node.next
            if self.head is not None: # if the delete node is not the only node
                self.head.prev = None # reset the head.prev to None

        # short cut to the next
        if node.next is not None: # if the node is not the tail 
            node.next.prev = node.prev # short cut the next connection
        else: # if the node is tail 
            assert node == self.tail, "DoublyLinkedList->delete->The node needs to be the tail node"
            # move the tail pointer
            self.tail = node.prev
            if self.tail is not None: # if the node is not the only one
                self.tail.next = None # reset the tail.next to None

    def traverse(self, action, backward=False):
        '''
            This method will traverse the linkedlist forward or backward,
            and put some action on each of the traversed nodes 
        '''
        assert backward in [True, False], "The parameter backward has to be True or False"
        
        if not backward: 
            current = self.head
            while current is not None:
                action(current)  
                current = current.next
        elif backward:
            current = self.tail
            while current is not None:
                action(current)
                current = current.prev

    def __len__(self):
        """
        Method to return the length of the doubly linked list using the traverse method.
        """
        count = 0

        def count_action(node):
            nonlocal count  # Use nonlocal to update count within the action function
            count += 1

        # Traverse the list and count the nodes
        self.traverse(count_action)

        return count

    def __str__(self):
        '''
            Print out the entire list of all elements using the traverse method
        '''
        
        result = [] # Define a list to collect node data during traversal

        
        def collect_data(node): # Function to append each node's data to the result list
            result.append(str(node))

        
        self.traverse(collect_data) # Traverse the list and collect all node data

        
        return " <-> ".join(result) if result else "Empty List" # Join the collected data into a single string, separated by arrows
    

class TreeNode:
    """The node in the tree"""
    def __init__(self):
        self.info = DoublyLinkedList()  # Linked list to store monitoring information
        self.children = []

    def __str__(self) -> str:
        '''
            Since the tree node store the DoublyLinkedList, 
            it only print out the first element of the Linkedlist 
        '''
        if self.info.head:
            return str(self.info.head.alias) if hasattr(self.info.head, 'alias') else str(self.info.head)
        else:
            return "Empty"

class Tree:
    """The basic tree structure"""
    def __init__(self, tag: str):
        self.root = TreeNode()
        self.tag = tag  # Tag to distinguish between different trees

    def add_child(self, parent_node):
        """Adds a child node to a specified parent node as the last child"""
        child_node = TreeNode()
        parent_node.children.append(child_node) # [].append
        return child_node

    def _find_parent_node(self, target_node: TreeNode):
        """
        Finds the parent of the given target node in the tree.

        Args:
            target_node (TreeNode): The node whose parent needs to be found.

        Returns:
            TreeNode: The parent node of the target node, or None if the target node is not found in the tree.
        """
        parent_node = None

        def search_for_parent(current_node):
            nonlocal parent_node
            if target_node in current_node.children:
                parent_node = current_node

        # Traverse the tree to find the parent of the target_node
        self.traverse(self.root, search_for_parent)

        return parent_node


    def traverse(self, node=None, action=None):
        """
        Performs pre-order traversal on the tree, applying an action (function) to each node.
        """
        if node is None:  # Start at the root if no node is provided
            node = self.root

        assert action is not None, "Lack of the action function for traverse"

        action(node) # Apply the action to the current node

        for child in node.children: # Recursively traverse each child node
            self.traverse(child, action)

    def sync_traverse(self, start_node=None, aggregate_action=None):
        """
        Synchronize the traversal of each node in the DoublyLinkedList (DLL) across all tree nodes.
        Apply an aggregate function on the nodes at the same positions.

        Args:
            aggregate_action(nodes_at_position): A function that aggregates the node info 
                                                 at the same position across the tree nodes' DLLs.
                                                 The nodes_at_position is a list of nodes    
            start_node (TreeNode, optional): The starting node for the traversal. 
                                             If None, the traversal starts from the root.
        """
        # make sure that the aggregate_action is not None 
        assert aggregate_action is not None, "Lack of the aggregate_action for sync_traverse"

        if start_node is None:
            start_node = self.root  # Start from the root if no starting node is provided

        position_map = {}  # Map to store DLL nodes by position, position_map = {0:[...], 1:[...]}

        # First Traverse: Traverse the tree and within each node, traverse the DLL
        def tree_action(node):
            current_position = 0 # enclosing variable to pass the info through the function

            # Function to apply on each node of the doubly linked list
            def dll_action(dll_node):
                nonlocal current_position # enclosing variable or it cannot be modified 
                if current_position not in position_map:
                    position_map[current_position] = [] # initilize the position for the map 
                position_map[current_position].append(dll_node) # append node info for the given position 
                current_position += 1

            # Traverse the DoublyLinkedList for each TreeNode
            node.info.traverse(dll_action)

        # Start the tree traversal, beginning from the specified start node
        self.traverse(start_node, tree_action)

        # Second Traverse: Process the nodes at each position in the map
        for nodes_at_position in position_map.values(): # iterate over the nodes   
            aggregate_action(nodes_at_position)


    def __str__(self):
        """
        Prints out the entire tree structure in a tree-like format using the traverse method.
        """
        result = []
        depth_map = {self.root: 0}  # Track the depth of each node
        last_child_map = {}  # Track if a node is the last child

        # helper function to collect depth and last child information
        def collect_data(node):
            depth = depth_map[node] # depth of the parent node, default for root is 0
            for i, child in enumerate(node.children): 
                depth_map[child] = depth + 1 # collect the depth of the child nodes 
                last_child_map[child] = (i == len(node.children) - 1) # collect the last node of the child nodes 

        # first pass to collect depth and last child information
        self.traverse(self.root, collect_data)

        # helper function to colect property prefix for printing node in a tree-like structure
        def get_prefix(node):
            depth = depth_map[node]
            is_last = last_child_map.get(node, True) # {}.get

            if depth == 0:
                prefix = "" # the prefix for the root node
            else:
                prefix = "" # initialize the prefix for the current node, it has to be defined before use

                current_node = node
                # the update for the prefix also depends on the parent nodes
                for _ in range(depth - 1): # go through the depth of the tree 
                    # parent_node = [
                    #     n for n, c in depth_map.items() if c == depth - 1 - d and current_node in n.children
                    # ][0] # set up for the parent nodes that belongs to the current node for given depth of the tree  
                    parent_node = self._find_parent_node(current_node)
                    if last_child_map[parent_node]:
                        prefix = "    " + prefix
                    else:
                        prefix = "│   " + prefix

                    current_node = parent_node

                if is_last:
                    prefix += "└── "
                else:
                    prefix += "├── "

            result.append(f"{prefix}{str(node)}")

        # Use the traverse method to print the tree structure
        self.traverse(self.root, get_prefix)

        return "\n".join(result)
