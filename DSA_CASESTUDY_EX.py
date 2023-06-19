# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:26:37 2023

@author: Naveen G
"""

import heapq
import datetime
from tabulate import tabulate
import math
import networkx as nx
import matplotlib.pyplot as plt

class Shipment:
    def __init__(self, id, sender, recipient, delivery_status, priority, product_name, delivery_time, distance, payment_method):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.delivery_status = delivery_status
        self.priority = priority
        self.product_name = product_name
        self.delivery_time = delivery_time
        self.distance = distance
        self.payment_method = payment_method

    def __lt__(self, other):
        return self.priority < other.priority

class ShipmentNode:
    def __init__(self, shipment):
        self.shipment = shipment
        self.left = None
        self.right = None

class ShipmentBinaryTree:
    def __init__(self):
        self.root = None

    def add_shipment(self, shipment):
        node = ShipmentNode(shipment)
        if self.root is None:
            self.root = node
        else:
            self._add_shipment_recursive(node, self.root)

    def _add_shipment_recursive(self, node, current):
        if node.shipment.id < current.shipment.id:
            if current.left is None:
                current.left = node
            else:
                self._add_shipment_recursive(node, current.left)
        elif node.shipment.id > current.shipment.id:
            if current.right is None:
                current.right = node
            else:
                self._add_shipment_recursive(node, current.right)

    def get_shipments_by_sender(self, sender):
        result = []
        if self.root:
            self._inorder_traversal(self.root, sender, result)
        return result

    def _inorder_traversal(self, node, sender, result):
        if node is not None:
            self._inorder_traversal(node.left, sender, result)
            if node.shipment.sender == sender:
                result.append(node.shipment)
            self._inorder_traversal(node.right, sender, result)

class ShipmentManager:
    def __init__(self):
        self.shipments_by_id = {}
        self.shipments_by_sender = {}
        self.shipments_by_recipient = {}
        self.priority_shipments = []
        self.binary_tree = ShipmentBinaryTree()

    def add_shipment(self, shipment):
        self.shipments_by_id[shipment.id] = shipment
        self.shipments_by_sender.setdefault(shipment.sender, []).append(shipment)
        self.shipments_by_recipient.setdefault(shipment.recipient, []).append(shipment)
        if shipment.priority:
            heapq.heappush(self.priority_shipments, shipment)
        self.binary_tree.add_shipment(shipment)

    def update_shipment_status(self, shipment_id, new_status):
        shipment = self.shipments_by_id.get(shipment_id)
        if shipment:
            shipment.delivery_status = new_status
            if shipment.priority:
                heapq.heapify(self.priority_shipments)
        else:
            print("Shipment not found!")

    def get_shipment_by_id(self, shipment_id):
        return self.shipments_by_id.get(shipment_id)

    def get_shipments_by_sender(self, sender):
        return self.binary_tree.get_shipments_by_sender(sender)

    def get_shipments_by_recipient(self, recipient):
        return self.shipments_by_recipient.get(recipient, [])

    def get_priority_shipments(self):
        return self.priority_shipments

    def get_all_shipments(self):
        return list(self.shipments_by_id.values())

manager = ShipmentManager()
# Add default shipments as they are on the list by default
default_shipments = [
    Shipment(
        id=1,
        sender='Ashok',
        recipient='Aswini',
        delivery_status='In Transit',
        priority=True,
        product_name='Shampoo',
        delivery_time='2 days',
        distance='10 km',
        payment_method='Credit Card'
    ),
    Shipment(
        id=2,
        sender='Dharma',
        recipient='Muthu',
        delivery_status='Delivered',
        priority=False,
        product_name='Hair Oil',
        delivery_time='3 days',
        distance='20 km',
        payment_method='Online'
    ),
    Shipment(
        id=3,
        sender='Raghaven',
        recipient='xxxxx',
        delivery_status='Pending',
        priority=False,
        product_name='Makeup-Kit',
        delivery_time='4 days',
        distance='15 km',
        payment_method='Cash on Delivery'
    )
]

for shipment in default_shipments:
    manager.add_shipment(shipment)

# Menu-driven code
while True:
    print("\n---- Shipment Management System ----")
    print("1. Add Shipment")
    print("2. Update Shipment Status")
    print("3. Retrieve Shipment by ID")
    print("4. Retrieve Shipments by Sender")
    print("5. Retrieve Shipments by Recipient")
    print("6. Retrieve Shipments by urgency")
    print("7. Retrieve All Shipments")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n---- Add Shipment ----")
        shipment_id = int(input("Enter shipment ID: "))
        sender = input("Enter sender name: ")
        recipient = input("Enter recipient name: ")
        delivery_status = input("Enter delivery status: In-Transit (or) Delivered (or) Pending ")
        priority = input("Is this a priority shipment? (y/n): ").lower() == 'y'
        product_name = input("Enter product name: ")
        delivery_time = None  
        distance = float(input("Enter delivery location distance: "))
        payment_method = input("Enter payment method: Credit Card (or) Online Payment (or) Cash On Delivery ")
        if delivery_status == 'delivered':
            delivery_time = datetime.datetime.now()  
        else:
            if priority:
                if distance <= 10:
                    delivery_time = datetime.datetime.now() + datetime.timedelta(days=1)  
                else:
                    delivery_time = datetime.datetime.now() + datetime.timedelta(days=2)  
            else:
                if distance <= 10:
                    delivery_time = datetime.datetime.now() + datetime.timedelta(days=3)  
                else:
                    delivery_time = datetime.datetime.now() + datetime.timedelta(days=5)  
        
        shipment = Shipment(
            id=shipment_id,
            sender=sender,
            recipient=recipient,
            delivery_status=delivery_status,
            priority=priority,
            product_name=product_name,
            delivery_time=delivery_time,
            distance=distance,
            payment_method=payment_method
        )
        manager.add_shipment(shipment)
        print("Shipment added successfully!")

    elif choice == "2":
        print("\n---- Update Shipment Status ----")
        shipment_id = int(input("Enter shipment ID to update: "))
        new_status = input("Enter new status: ")
        manager.update_shipment_status(shipment_id, new_status)
        print("Shipment status updated successfully!")

    elif choice == "3":
        print("\n---- Retrieve Shipment by ID ----")
        shipment_id = int(input("Enter shipment ID to retrieve: "))
        shipment = manager.get_shipment_by_id(shipment_id)
        if shipment:
            table_data = [
            ["ID", shipment.id],
            ["Sender", shipment.sender],
            ["Recipient", shipment.recipient],
            ["Delivery Status", shipment.delivery_status],
            ["Priority", shipment.priority],
            ["Product Name", shipment.product_name],
            ["Delivery Time", shipment.delivery_time],
            ["Distance", shipment.distance],
            ["Payment Method", shipment.payment_method]
        ]
            print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
        else:
            print("Shipment not found!")

    elif choice == "4":
        print("\n---- Retrieve Shipments by Sender ----")
        sender = input("Enter sender name to retrieve shipments: ")
        shipments = manager.get_shipments_by_sender(sender)
        if shipments:
            print("Shipments by Sender:")
            table_data = [
            ["ID", shipment.id],
            ["Sender", shipment.sender],
            ["Recipient", shipment.recipient],
            ["Delivery Status", shipment.delivery_status],
            ["Priority", shipment.priority],
            ["Product Name", shipment.product_name],
            ["Delivery Time", shipment.delivery_time],
            ["Distance", shipment.distance],
            ["Payment Method", shipment.payment_method]
        ]
            print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
        else:
            print("No shipments found for the given sender!")

    elif choice == "5":
        print("\n---- Retrieve Shipments by Recipient ----")
        recipient = input("Enter recipient name to retrieve shipments: ")
        shipments = manager.get_shipments_by_recipient(recipient)
        if shipments:
            print("Shipments by Recipient:")
            table_data = [
            ["ID", shipment.id],
            ["Sender", shipment.sender],
            ["Recipient", shipment.recipient],
            ["Delivery Status", shipment.delivery_status],
            ["Priority", shipment.priority],
            ["Product Name", shipment.product_name],
            ["Delivery Time", shipment.delivery_time],
            ["Distance", shipment.distance],
            ["Payment Method", shipment.payment_method]
        ]
            print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
        else:
            print("No shipments found for the given recipient!")

    elif choice == "6":
        print("\n---- Retrieve Shipments by Urgency ----")
        priority_shipments = manager.get_priority_shipments()
        if priority_shipments:
            print("Priority Shipments:")
            table_data = [
            ["ID", shipment.id],
            ["Sender", shipment.sender],
            ["Recipient", shipment.recipient],
            ["Delivery Status", shipment.delivery_status],
            ["Priority", shipment.priority],
            ["Product Name", shipment.product_name],
            ["Delivery Time", shipment.delivery_time],
            ["Distance", shipment.distance],
            ["Payment Method", shipment.payment_method]
        ]
            print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
        else:
            print("No priority shipments found!")

    elif choice == "7":
        print("\n---- Retrieve All Shipments ----")
        all_shipments = manager.get_all_shipments()
        if all_shipments:
            table_data = []
            for shipment in all_shipments:
                table_data.append([
                    shipment.id,
                    shipment.sender,
                    shipment.recipient,
                    shipment.delivery_status,
                    shipment.priority,
                    shipment.product_name,
                    shipment.delivery_time,
                    shipment.distance,
                    shipment.payment_method
                    ])

                headers = [
                    "ID",
                    "Sender",
                    "Recipient",
                    "Delivery Status",
                    "Priority",
                    "Product Name",
                    "Delivery Time",
                    "Distance",
                    "Payment Method"
                    ]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("No shipments found!")

    elif choice == "0":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")

print("Thank you for using the Shipment Management System!")

print("\n---- Visualizing Binary Tree ----")
# Function to calculate the height of the binary tree
def get_tree_height(node):
    if node is None:
        return 0
    left_height = get_tree_height(node.left)
    right_height = get_tree_height(node.right)
    return max(left_height, right_height) + 1

# Function to check if the binary tree is balanced
def is_balanced(node):
    if node is None:
        return True
    left_height = get_tree_height(node.left)
    right_height = get_tree_height(node.right)
    if abs(left_height - right_height) > 1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)

# Function to balance the binary tree
def balance_binary_tree(node):
    if node is None:
        return None
    node.left = balance_binary_tree(node.left)
    node.right = balance_binary_tree(node.right)
    balance_factor = get_tree_height(node.left) - get_tree_height(node.right)
    if balance_factor > 1:
        if get_tree_height(node.left.left) >= get_tree_height(node.left.right):
            node = rotate_right(node)
        else:
            node.left = rotate_left(node.left)
            node = rotate_right(node)
    elif balance_factor < -1:
        if get_tree_height(node.right.right) >= get_tree_height(node.right.left):
            node = rotate_left(node)
        else:
            node.right = rotate_right(node.right)
            node = rotate_left(node)
    return node

# Function to perform a right rotation
def rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    return new_root

# Function to perform a left rotation
def rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    return new_root

# Function to calculate the x-coordinate for each node postions 
def calculate_node_positions(node, x, y, level_height, node_positions):
    if node is not None:
        calculate_node_positions(node.left, x - level_height / 2, y - 1, level_height / 2, node_positions)
        node_positions[node] = (x, y)
        calculate_node_positions(node.right, x + level_height / 2, y - 1, level_height / 2, node_positions)


node_positions = {}

tree_height = get_tree_height(manager.binary_tree.root)

num_nodes = 2**tree_height - 1

tree_width = math.pow(2, tree_height - 1) * 2 - 1

level_height = tree_width / 2
y = tree_height
x = level_height / 2

# Check if the binary tree is balanced
if not is_balanced(manager.binary_tree.root):
    #It tries to balance the tree

    manager.binary_tree.root = balance_binary_tree(manager.binary_tree.root)


    calculate_node_positions(manager.binary_tree.root, x, y, level_height, node_positions)

    graph = nx.Graph()

    # Add nodes and edges to the graph
    for node, position in node_positions.items():
        graph.add_node(node.shipment.id, shipment=node.shipment)
        if node.left is not None:
            graph.add_edge(node.shipment.id, node.left.shipment.id)
        if node.right is not None:
            graph.add_edge(node.shipment.id, node.right.shipment.id)


    pos = nx.spring_layout(graph)
    labels = {node: f"ID: {graph.nodes[node]['shipment'].id}\nStatus: {graph.nodes[node]['shipment'].delivery_status}" for node in graph.nodes}
    nx.draw_networkx(graph, pos, with_labels=True, labels=labels)
    plt.show()
else:
    print("The binary tree is balanced.")
















