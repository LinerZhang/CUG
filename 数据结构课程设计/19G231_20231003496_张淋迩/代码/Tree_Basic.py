import math
import copy
class Stack():
    def __init__(self):
        self.data=[]
        self.top=-1
    def is_empty(self):
        return self.top<0
    def size(self):
        return self.top+1
    def top_value(self):
        if self.is_empty():
            raise KeyError("Stack is empty")
        else:
            return self.data[self.top]
    def push(self,value):
        self.top+=1
        self.data.append(value)
    def pop(self):
        if self.is_empty():
            raise KeyError("Stack is empty")
        else:
            value=self.data.pop()
            self.top-=1
            return value
        
class BinaryTree:
    def __init__(self):
        self.data = []
        self.last_leaf_idx = -1
    
    def value(self, idx):
        if idx >= len(self.data):
            return None
        return self.data[idx]
    
    def change_value(self, idx, value):
        if idx < len(self.data):
            self.data[idx] = value
        else:
            raise IndexError("Index out of range")
    
    def left_idx(self, idx):
        return 2 * idx + 1
    
    def right_idx(self, idx):
        return 2 * idx + 2
    
    def parent_idx(self, idx):
        return (idx - 1) // 2
    
    def get_last_leaf_idx(self):
        return self.last_leaf_idx
    
    def insert(self, idx, value):
        while idx >= len(self.data):
            self.data.append(None)
        self.data[idx] = value
        self.last_leaf_idx = max(self.last_leaf_idx, idx)
    
    def print_tree(self):
        n=self.last_leaf_idx
        high=math.ceil(math.log((n+1),2))
        max_num=2**(high-1)
        for i in range(1,high):
            num=2**(i-1)
            for k in range((max_num-num)//2):
                print("     ",end="")
            for j in range(2**(i-1)-1,2**i-1):
                if self.data[j]==None:
                    print(self.data[j],end=" ") 
                else:
                    print(self.data[j],end="    ")
            print("\n",end="")   
        for i in range(2**(high-1)-1,n+1): 
            if self.data[i]==None:
                print(self.data[i],end=" ") 
            else:
                print(self.data[i],end="    ")   
    def preorder_traversal(self):
        def traverse(idx):
            if idx >= len(self.data) or self.data[idx] is None:
                return []
            result = [self.data[idx]]
            result += traverse(self.left_idx(idx))
            result += traverse(self.right_idx(idx))
            return result
        
        return traverse(0)

    def inorder_traversal(self):
        def traverse(idx):
            if idx >= len(self.data) or self.data[idx] is None:
                return []
            result = traverse(self.left_idx(idx))
            result.append(self.data[idx])
            result += traverse(self.right_idx(idx))
            return result
        return traverse(0)
    
    def postorder_traversal(self):
        def traverse(idx):
            if idx >= len(self.data) or self.data[idx] is None:
                return []
            result = traverse(self.left_idx(idx))
            result += traverse(self.right_idx(idx))
            result.append(self.data[idx])
            return result
        
        return traverse(0)
#Legitimacy verification
#check if the parentheses are complete
def check(sen_list):
    sign1=False
    veri=Stack()
    bra=["(",")"]
    sign=["+","-","*","/"]
    num=["0","1","2","3","4","5","6","7","8","9"]
    para=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for i in range(len(sen_list)):
        if len(sen_list)<=2:
            sign1=True
            break
        elif sen_list[i] not in sign and sen_list[i] not in num and sen_list[i] not in para and sen_list[i] not in bra:
            sign1=True
            break
        else:
            if sen_list[i]=="(":
                if i+1>=len(sen_list)-1:
                    sign1=True
                    break
                if i-1>=0 and  sen_list[i-1] not in sign:
                    sign1=True
                    break
                if i+1<len(sen_list) and sen_list[i+1] in sign:
                    sign1=True
                    break
                veri.push(sen_list[i])
            elif sen_list[i]==")":
                if i-1<0:
                    sign1=True
                    break
                if i+1<len(sen_list) and sen_list[i+1] not in sign:
                    sign1=True
                    break
                if i-1>=0 and sen_list[i-1] in sign:
                    sign1=True
                    break
                if veri.is_empty():
                    sign1=True
                    break
                else:
                    veri.pop()
            elif sen_list[i] in sign:
                if i<=0 or i>=len(sen_list)-1:
                    sign1=True
                    break
                if sen_list[i-1] in sign or sen_list[i-1]=="(" or sen_list[i-1]==" ":
                    sign1=True
                    break
                if sen_list[i+1] in sign or sen_list[i+1]==")" or sen_list[i+1]==" ":
                    sign1=True
                    break
            elif sen_list[i] in para or sen_list[i] in num:
                if i>=2:
                    if sen_list[i-1] in num or sen_list[i-1] in para or sen_list[i-1]==")": 
                        sign1=True
                        break
                if i<=len(sen_list)-3:
                    if sen_list[i+1] in num or sen_list[i+1] in para or sen_list[i+1]=="(":
                        sign1=True
                        break 
                else:
                    continue
    if veri.is_empty()==False:
        sign1=True
    if sign1==True:
        print("The expression is not legitimate!")
    return sign1
    
#convert the expression to the postfix expression
def convert(sen_list):
    num=["0","1","2","3","4","5","6","7","8","9"]
    para=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    prec={"*":2,"/":2,"+":1,"-":1}
    s=Stack()
    suffix_list=[]
    for i in range(len(sen_list)):
        if sen_list[i] in num:#if the current element is a number,turn it into an int form element here,which is convenient for subsequent calculations
            val=int(sen_list[i])
            suffix_list.append(val)
            continue
        elif sen_list[i] in para:
            suffix_list.append(sen_list[i])
            continue
        else:
            if sen_list[i] in prec:  
                if s.is_empty()==True:
                    s.push(sen_list[i])
                else:
                    j=s.top_value()
                    if j=="(":
                        s.push(sen_list[i])
                    else:
                        if prec[sen_list[i]]>prec[j]:
                            s.push(sen_list[i])
                        elif prec[sen_list[i]]<=prec[j]:
                            s.pop()
                            suffix_list.append(j)
                            s.push(sen_list[i])
            elif sen_list[i]=="(":
                 s.push(sen_list[i])
            elif sen_list[i]==")":
                j=s.pop()
                while j!="(":
                    suffix_list.append(j)
                    j=s.pop()
    while not s.is_empty():
        j=s.pop()
        suffix_list.append(j)
    return suffix_list

def build_tree(suffix):
    print("\nThe process of building a binary tree is as follows:")
    sign=["+","-","*","/",]
    tree = BinaryTree()
    done=[]
    current_idx=0
    current_value=suffix.pop(-1)
    tree.insert(current_idx,current_value)
    print(f"Add {current_value} to the tree at index {current_idx} as the root node. ")
    done.append(current_idx)
    while len(suffix)>0:
        current_value=suffix.pop(-1)
        if current_value in sign:
            left_child_idx=tree.left_idx(current_idx)
            right_child_idx=tree.right_idx(current_idx)
            if left_child_idx not in done:
                current_idx=left_child_idx
            else:
                if right_child_idx not in done:
                    current_idx=right_child_idx           
            done.append(current_idx) 
            tree.insert(current_idx,current_value)
            print(f"Add {current_value} to the tree at index {current_idx} as the child node of the parent node at index {tree.parent_idx(current_idx)}.")
        else:
            left_child_idx=tree.left_idx(current_idx)
            right_child_idx=tree.right_idx(current_idx)
            if left_child_idx not in done:
                next_idx=left_child_idx
            else:
                if right_child_idx not in done:
                    next_idx=right_child_idx
                    current_idx=tree.parent_idx(current_idx)
                else:
                    while right_child_idx in done:
                        next_idx=tree.parent_idx(next_idx)
                        right_child_idx=tree.right_idx(next_idx)
                    next_idx=right_child_idx
            done.append(next_idx) 
            tree.insert(next_idx,current_value)
            print(f"Add {current_value} to the tree at index {next_idx} as one leaf node of the tree.")
    return tree

def sub_evaluate(tree,current_idx):
    sign=["+","-","*","/",]
    current=tree.value(current_idx)
    left=tree.value(tree.left_idx(current_idx))
    right=tree.value(tree.right_idx(current_idx))
    if left in sign:
        sub_evaluate(tree,tree.left_idx(current_idx))
    if right in sign:
        sub_evaluate(tree,tree.right_idx(current_idx))
    if current=="+":
        tree.change_value(current_idx,left+right)
        print(f"{right}+{left}={left+right}")
    elif current=="-":
        tree.change_value(current_idx,right-left)
        print(f"{right}-{left}={right-left}")
    elif current=="*":
        tree.change_value(current_idx,left*right)
        print(f"{right}*{left}={left*right}")
    elif current=="/":
        tree.change_value(current_idx,right/left)
        print(f"{right}/{left}={right/left}")
def evaluate(tree1):
    tree = copy.deepcopy(tree1)
    sign=["+","-","*","/",]
    para=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    print("\nPlease assign values to the unknown variables:")
    k=0
    assign={}
    while k<tree.get_last_leaf_idx()+1:
        if tree.value(k) in para and tree.value(k) not in assign.keys():
            info=input(f"{tree.value(k)}=")
            assign[tree.value(k)]=info
        k+=1
    j=0
    n=tree.get_last_leaf_idx()
    while j<=n:
        if tree.value(j) in assign.keys():
            tree.change_value(j,int(assign[tree.value(j)]))
        j+=1
    #find the index of the last leaf
    print("The calculation process is as follows:")
    current_idx=tree.get_last_leaf_idx()
    while current_idx>=0:
        if tree.value(current_idx) not in sign:#not a operator
            if tree.value(current_idx)==None:
                current_idx=-1
            else:
                current_idx=tree.parent_idx(current_idx)#find the next one 
        else:#a operator
            left=tree.value(tree.left_idx(current_idx))
            right=tree.value(tree.right_idx(current_idx))
            current=tree.value(current_idx)
            if left in assign.keys():
                left=int(assign[left])
            elif left in sign:
                sub_evaluate(tree,tree.left_idx(current_idx))
            else:
                left=int(left)
            if right in assign.keys():
                right=int(assign[right])
            elif right in sign:
                sub_evaluate(tree,tree.right_idx(current_idx))
            else:
                right=int(right)
            sub_evaluate(tree,current_idx)
            current_idx=current_idx-1
            current=tree.value(current_idx)
            while current==None:
                current_idx=current_idx-1#find the next one
                current=tree.value(current_idx)#find the next one
    print("The result of the expression is :",tree.value(0))
           
if __name__=="__main__":
    get=2
    while get==2:
        sen=str(input("Please input the arithmetic expression:"))
        sen_list=[]
        for i in sen:
            sen_list.append(str(i))
        if not check(sen_list):
            suffix = convert(sen_list)
            print("\nThe suffix of this arithmetic expression is as follows:")
            print(" ".join(map(str, suffix)))
            tree = build_tree(suffix)
            print("\nThe constructed binary tree structure is as follows:")
            tree.print_tree()
            print("\nThe binary tree preorder traversal result is as follows:")
            preorder_result = tree.preorder_traversal()
            print(" ".join(map(str, preorder_result)))
            print("\nThe binary tree inorder traversal result is as follows:")
            inorder_result = tree.inorder_traversal()
            print(" ".join(map(str, inorder_result)))
            print("\nThe binary tree postorder traversal result is as follows:")
            postorder_result = tree.postorder_traversal()
            print(" ".join(map(str, postorder_result)))
            evaluate(tree)
            print("If you want to reassign a value to this binary tree, please press 1\nIf you want to re-enter the infix arithmetic expression, please press 2\nIf you want to end the program, please press 3")
            choose=int(input("Your choice:"))
            while choose==1:
                evaluate(tree)
            get=choose

            
            
