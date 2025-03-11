from collections import defaultdict
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

class min_queue:
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
    return file
def count(file):
    counts = defaultdict(int)   
    for i in range(len(file)):
        counts[file[i]] += 1
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts
def count_1(file,k):
    counts_three = defaultdict(int)  
    for i in range(len(file)):
        if i + k <= len(file): 
            counts_three[file[i:i+k]] += 1
    sorted_3 = sorted(counts_three.items(), key=lambda x: x[1], reverse=True)
    return sorted_3

def add_to_tree(queue):
    if queue.length()==1:
        root=queue.dequeue()
        return root
    else:
        node1=queue.dequeue()
        node2=queue.dequeue()
        new_node=Node(None,node1.get_value()+node2.get_value())
        new_node.left_child(node1)
        new_node.right_child(node2)
        node1.set_parent(new_node)
        node2.set_parent(new_node)
        queue.enqueue(new_node)
        return add_to_tree(queue) 
        #add return !!!!!!!the problem is here!!!!!
          
def HuffmanTree_1(sorted_counts):
    queue=min_queue()
    for char,freq in sorted_counts:
        queue.enqueue(Node(char,freq))
    return add_to_tree(queue)
def HuffmanTree_2(sorted_counts,sorted_3,n):
    queue=min_queue()
    for char,freq in sorted_counts:
        queue.enqueue(Node(char,freq))
    for i in range(n):
        queue.enqueue(Node(sorted_3[i][0],sorted_3[i][1]))
    return add_to_tree(queue)

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
def encode(file,HuffDict,k):
    encoded_text=""
    i=0
    while i<len(file):
        if file[i:i+k] in HuffDict:
            char=file[i:i+k]
            i+=k
        else:
            char=file[i]
            i+=1
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

def compare(file):
    ZLE=1   
    sorted_counts=count(file)
    root_1=HuffmanTree_1(sorted_counts)
    dic1=HuffmanDict(root_1)
    encoded_1=encode(file,dic1,0)
    l1=len(encoded_1)
    info={}
    for k in range(1,20):
        sorted_3=count_1(file,k)
        for n in range(1,50):
            root_2=HuffmanTree_2(sorted_counts,sorted_3,n)
            dic2=HuffmanDict(root_2)
            encoded_2=encode(file,dic2,k)
            l2=len(encoded_2)
            info[(k, n)] = [l2, encoded_2, dic2, root_2]
    L=l1
    for par,inf in info.items():
        if inf[0]<L:
            ZLE=0
            P=par
            L=inf[0]
            encoded_final=inf[1]
            D=inf[2]
            R=inf[3]
    if ZLE:
        print("The shortest code: n=k=0 ,",l1)
        return encoded_1,dic1,root_1
    else:
        print(f"The shortest code: k={P[0]},n={P[1]},",L)
        return encoded_final,D,R
        
def main():
    input_file='HUffmanCodes\MyOrigionalText.txt'
    file=parse_file(input_file)
    encoded_text,HuffDict,tree_root=compare(file)
    with open('HUffmanCodes/MyCodeWorkBk.txt', 'w',encoding='utf-8', errors='replace') as f:
        for char, code in HuffDict.items():
            f.write(f"{repr(char)}: {code}\n")
        f.close()
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
    