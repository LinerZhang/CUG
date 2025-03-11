import matplotlib.pyplot as plt
class Node:
    def __init__(self,char,value):
        self.char=char
        self.value=value
        self.left=None
        self.right=None
        self.code=None
        self.parent=None
    def __lt__(self, other):
        # Less-than comparison is needed for sorting in priority queue
        return self.value < other.value
    def left_child(self,node):
        self.left=node
    def right_child(self,node):
        self.right=node
    def set_parent(self,node):
        self.parent=node
    def get_left(self):
        return self.left
    def get_right(self):
        return self.right
    def get_parent(self):
        return self.parent
    def get_value(self):
        return self.value
    def get_char(self):
        return self.char
    def set_code(self,code):
        self.code=code

class min_queue:#minimum priority queue
    def __init__(self):
        self.queue=[]
    def enqueue(self, node):
        if not self.queue:
            self.queue.append(node)
        else:
            i = 0
            while i < len(self.queue) and self.queue[i].get_value() >= node.get_value():
                i += 1
            self.queue.insert(i, node)
    def dequeue(self):
        return self.queue.pop(-1)
    def length(self):
        return len(self.queue)
    
def parse_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        file = f.read() 
    return list(file)
def count(characters):#count the frequeny of each character and sort them
    counts={}        
    num=0
    for i in characters:
        if i not in counts:
            num+=1
            counts[i]=1
        else:
            counts[i]+=1
    sorted_counts = sorted(counts.items(), key=lambda x:x[1])
    return sorted_counts,num
def add_to_tree(queue):
    if queue.length()==1:
        root=queue.dequeue()
        # print(root.get_value())
        return root
    else:
      node1=queue.dequeue()#smaller node
      node2=queue.dequeue()#the last 2 nodes
      new_node=Node(None,node1.get_value()+node2.get_value())#char=None, value=sum of the two nodes
      new_node.left_child(node1)
      new_node.right_child(node2)
      node1.set_parent(new_node)
      node2.set_parent(new_node)
      queue.enqueue(new_node)
      return add_to_tree(queue) #add return !!!!!!!the problem is here!!!!!
      
def HuffmanTree(sorted_counts):
    queue=min_queue()
    for char,freq in sorted_counts:
        queue.enqueue(Node(char,freq))
    return add_to_tree(queue)

def draw_tree(root, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        def calculate_depth(node):
            if node is None:
                return 0
            left_depth = calculate_depth(node.get_left())
            right_depth = calculate_depth(node.get_right())
            return max(left_depth, right_depth) + 1 #dynamic programming
        def calculate_width(depth):
            return (2 **depth) # the bottom layer has the most nodes
        depth = calculate_depth(root)
        width = calculate_width(depth)
        # print("d:",depth)
        # print("w:",width)
        positions={}
        def get_positions(node, x, y, level, positions):
            positions[node] = [x, y]
            if node.get_left() is not None:
                l = node.get_left()
                level += 1

def draw_tree(root, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        def calculate_depth(node):
            if node is None:
                return 0
            left_depth = calculate_depth(node.get_left())
            right_depth = calculate_depth(node.get_right())
            return max(left_depth, right_depth) + 1
        depth = calculate_depth(root)
        f.write(f"Tree Depth: {depth}\n")
        def print_tree(node, level, f):
            if node is None:
                return
            else:
                f.write(f"{' ' * level}{node.get_char()}:{node.get_value()}(level {level})\n")
                print_tree(node.get_left(), level + 1, f)
                print_tree(node.get_right(), level + 1, f)
        print_tree(root, 0, f)
        
import matplotlib.pyplot as plt
def draw_binary_tree(root, file_name=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    def plot_tree(node, x, y, dx, dy, level, ax):
        if node is None:
            return
        ax.text(x, y, f'{node.get_char()}:{node.get_value()}', ha='center', va='center',
                fontsize=12, bbox=dict(facecolor='skyblue', edgecolor='black', boxstyle="round,pad=0.5"))
        if node.get_left() is not None:
            ax.plot([x, x - dx], [y, y - dy], color='black', lw=1)  # Line from parent to left child
            plot_tree(node.get_left(), x - dx, y - dy, dx / 2, dy, level + 1, ax)
        if node.get_right() is not None:
            ax.plot([x, x + dx], [y, y - dy], color='black', lw=1)  
            plot_tree(node.get_right(), x + dx, y - dy, dx / 2, dy, level + 1, ax)
    ax.set_xlim(-60, 60)   
    ax.set_ylim(-30, 0) 
    # ax.axis('off') 
    plot_tree(root, 0, 0, 30, 2, 0, ax)
    plt.savefig(file_name, bbox_inches='tight') 

def find_leaf(node, code,HuffDict):
    if node is None:
        return HuffDict#{char:code}
    if node.get_left() is None and node.get_right() is None: # It's a leaf node
        HuffDict[node.get_char()] = code
        return HuffDict
    if node.get_left() is not None:
        HuffDict = find_leaf(node.get_left(), code + "0", HuffDict)#until found the lefest node
    if node.get_right() is not None:
        HuffDict = find_leaf(node.get_right(), code + "1", HuffDict)
    return HuffDict      
def HuffmanDict(root):
    node=root
    HuffDict={}
    HuffDict=find_leaf(node,"",HuffDict)
    return HuffDict 

def encode(characters,HuffDict):
    encoded_text=""
    for char in  characters:
        encoded_text+=HuffDict[char]
    return encoded_text
def decode(encoded_text,HuffDict):
    decoded_text=""
    current_code=""
    for code in encoded_text:
        current_code+=code
        for char,char_code in HuffDict.items():
            if current_code==char_code:
                decoded_text+=char
                current_code=""
    return decoded_text

def encode(characters,HuffDict):
    encoded_text=""
    for char in  characters:
        encoded_text+=HuffDict[char]
    return encoded_text

def main():
    input_file='HUffmanCodes\MyOrigionalText.txt'
    characters=parse_file(input_file)
    # print(characters)
    sorted_counts,num=count(characters)
    # print(sorted_counts)
    # print(num)
    tree_root=HuffmanTree(sorted_counts)
    HuffDict=HuffmanDict(tree_root)
    # print(HuffDict)
    with open('HUffmanCodes/MyCodeWorkBk.txt', 'w',encoding='utf-8', errors='replace') as f:
        for char, code in HuffDict.items():
            f.write(f"{repr(char)}: {code}\n")
        f.close()
    encoded_text=encode(characters,HuffDict)
    print(len(encoded_text))
    with open('HUffmanCodes\MyEncodingFile.txt','w') as f:
        f.write(encoded_text)
        f.close()
    # print(encoded_text)
    decoded_text=decode(encoded_text,HuffDict)
    with open('HUffmanCodes\MyDecodingFile.txt', 'w', encoding='utf-8', errors='replace') as f:
        f.write(decoded_text)
    # print(decoded_text)
    draw_tree(tree_root,"HUffmanCodes\MyHuffmanFile.txt")
    draw_binary_tree(tree_root, "HUffmanCodes/MyHuffmanTree.png")
if __name__ == "__main__":
        main()
    