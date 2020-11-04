# ------PROBLEM : DRAW A PINE TREE ------
# For this problem I want you to draw a pine tree after asking the user
# for the number of rows. Here is the sample program

"""

How tall is the tree : 5

"""

'''
Patterns:
4 spaces : 1 hash
3 spaces : 3 hash
2 spaces : 5 hash
1 spaces : 7 hash
0 spaces : 9 hash
4 spaces : 1 hash
loop times = tree_height
spaces decrement by 1
hashs increment by 2
spaces before stump =4
'''
m = int(input("please input your tree height: "))
i = m
while i>0:
    print(' ' * (i-1) + '#' * (2*(m-i+1)-1) )
    i = i-1
print(' ' * (m - 1) + '#')

# Get the number of rows for the tree
tree_height = input("How tall is the tree: ")

# Convert into an integer
tree_height = int(tree_height)

# initiate the spaces
spaces = tree_height - 1

# initiate the hashes
hashes = 1

# stump_spaces
stump_sapces = tree_height - 1

# while loop times eaqual to tree_height
while tree_height != 0:

    # print the sapces
    for i in range(spaces):
        print(' ', end='')

    # print the hashes
    for i in range(hashes):
        print('#', end='')

    # Newline after each row is printed
    print()
    # spaces decremented by 1
    spaces -= 1

    # hashes incremented by 2
    hashes += 2

    # tree_height decremented by 1
    tree_height -= 1

# print the spaces before stump
for i in range(stump_sapces):
    print(' ', end='')
# print the hash
print('#')