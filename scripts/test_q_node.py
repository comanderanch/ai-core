# test_q_node.py

from q_node import QNode

# Create primary node with type 'logic'
node_a = QNode(node_type="logic", base_color=(0, 255, 0))

# Apply fluorescence and Q-state
node_a.apply_fluorescence("reflex")
node_a.shift_conscious_state(+1)
node_a.update_field(frequency=19.7, amplitude=0.81)

# Create a second node and connect
node_b = QNode(node_type="memory", base_color=(0, 0, 255))
node_a.connect_node(node_b)

# Print description of node A
print("Node A:")
print(node_a.describe_node())

# Print description of node B
print("\nNode B:")
print(node_b.describe_node())
