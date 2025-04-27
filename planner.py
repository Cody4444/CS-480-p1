
import sys

class DFS_Node:
    def __init__(self, cords):
        self.cords = cords
        self.left = (cords[0]-1, cords[1])
        self.right = (cords[0]+1, cords[1])
        self.up = (cords[0], cords[1]-1)
        self.down = (cords[0], cords[1]+1)

class UCS_Node:
    def __init__(self, dirty, dcords, world, cords, move, visited):
        self.dirty = dirty
        self.cords = cords
        self.world = world
        self.dcords = dcords
        self.move = move
        self.visited = visited
        self.left = (cords[0]-1, cords[1])
        self.right = (cords[0]+1, cords[1])
        self.up = (cords[0], cords[1]-1)
        self.down = (cords[0], cords[1]+1)


def parse(file):
    with open(file, 'r') as fp:
        line = fp.readline()
        line = line.rstrip()
        n = int(line)

        line = fp.readline()
        line = line.rstrip()
        world = [None] * int(line)

        line = fp.readline()
        line = line.rstrip()
        count = 0
        while line: 
            if n != len(line):
                print("world reading error")
            world[count] = line
            line = fp.readline()
            line = line.rstrip()
            count = count + 1

    return world

def real_cords(world, cords):
    xmax = len(world[0])
    ymax = len(world)

    valid = True
    if  cords[0] < 0 or cords[0] >= xmax:
        valid = False
    if  cords[1] < 0 or cords[1] >= ymax:
        valid = False
    if valid:
        if map(world, cords) == "#":
            valid = False
    return valid

def map(world, cords):
    return world[cords[1]][cords[0]]

def clean(world, cords):
    world[cords[1]] = world[cords[1]][:cords[0]] + "_" + world[cords[1]][cords[0]+1:]
    return world

expanded = 1
generated = 1
dirty = 0
nodes = []


def dfs(world, cords, parent):
    global expanded
    global generated
    global nodes
    global dirty

    if map(world, cords) == "*":
        print("V")
        world = clean(world, cords)
        dirty = dirty - 1
    if dirty == 0:
        return 0
    node = DFS_Node(cords)
    left = False
    right = False
    up = False
    down = False

    if real_cords(world, node.left):
        if not (node.left in nodes):
            generated = generated + 1
            left = True
    if real_cords(world, node.right):
        if not (node.right in nodes):
            generated = generated + 1
            right = True
    if real_cords(world, node.up):
        if not (node.up in nodes):
            generated = generated + 1
            up = True
    if real_cords(world, node.down):
        if not (node.down in nodes):
            generated = generated + 1
            down = True

    if left:
        if node.left != parent:
            print("W")
            expanded = expanded + 1
            nodes.append(node.left)
            backtrack = dfs(world, node.left, parent)
            if (backtrack):
                print("E")
            else: 
                return 0
    if right:
        if node.right != parent:
            print("E")
            expanded = expanded + 1
            nodes.append(node.right)
            backtrack = dfs(world, node.right, parent)
            if (backtrack):
                print("W")
            else: 
                return 0
    if up:
        if node.up != parent:
            print("N")
            expanded = expanded + 1
            nodes.append(node.up)
            backtrack = dfs(world, node.up, parent)
            if (backtrack):
                print("S")
            else: 
                return 0
    if down:
        if node.down != parent:
            print("S")
            expanded = expanded + 1
            nodes.append(node.down)
            backtrack = dfs(world, node.down, parent)
            if (backtrack):
                print("N")
            else: 
                return 0
    return 1

queue = 0


def ucs(node):
    global expanded
    global generated
    global nodes
    global queue
    queue = queue + 1


    if node.cords in node.dcords:
        node.move = node.move + "\nV"
        node.dcords.remove(node.cords)
        node.dirty = node.dirty - 1
        node.visited = []
    if node.dirty == 0:
        print(node.move)
        print("%d nodes generated", generated)
        print("%d node expanded", expanded)
        exit()
    node.visited.append(node.cords)
    

    if real_cords(node.world, node.left):
        if not node.left in node.visited:
            generated = generated + 1
            node1 = UCS_Node(node.dirty, node.dcords.copy(), node.world, node.left,  node.move + "\nW", node.visited.copy())
            nodes.append(node1)
    if real_cords(node.world, node.right):
        if not node.right in node.visited:
            generated = generated + 1
            node1 = UCS_Node(node.dirty, node.dcords.copy(), node.world, node.right, node.move + "\nE", node.visited.copy())
            nodes.append(node1)
    if real_cords(node.world, node.up):
        if not node.up in node.visited:
            generated = generated + 1
            node1 = UCS_Node(node.dirty, node.dcords.copy(), node.world, node.up, node.move + "\nN", node.visited.copy())
            nodes.append(node1)
    if real_cords(node.world, node.down):
        if not node.down in node.visited:
            generated = generated + 1
            node1 = UCS_Node(node.dirty, node.dcords.copy(), node.world, node.down, node.move + "\nS", node.visited.copy())
            nodes.append(node1)

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 3:
        print("incorrect number of arguments")
        exit()
    if sys.argv[1] != "uniform-cost" and sys.argv[1] != "depth-first":
        print("incorrect algorithm try uniform-cost or depth-first")
    

    world = parse(sys.argv[2])
    start = [0,0]
    dcords = []

    dirty = 0
    for i in range(len(world[0])):
        for j in range(len(world)):
            if world[j][i] == "@":
                start[0] = i
                start[1] = j
            if world[j][i] == "*":
                dirty = dirty + 1
                dcords.append((i, j))
    
    

    if sys.argv[1] == "depth-first":
        nodes.append(start)
        dfs(world, start, (-1, -1))
        print("%d nodes generated", generated)
        print("%d node expanded", expanded)

    elif sys.argv[1] == "uniform-cost":
        node = UCS_Node(dirty, dcords, world, (start[0], start[1]), "", [])
        nodes.append(node)
        while 1:
            ucs(nodes[queue])
            expanded = expanded + 1 
