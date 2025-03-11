import random
#design the database-stack
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
        
#design a maze
print("If you want to design a maze by yourself,please enter 1;")
print("If you want to input a amaze by random,please enter 2;")
choice=int(input("Your choice:"))
if choice==1:
    n,m=map(int,input("Please Enter The Size Of Your Maxe(n*m):").split("*"))#n rows with each row m items
    print("Please Design Your Maze:")
    Maze=[]
    for i in range(n):
        row=input(f"row_{i}({m} itmes):").split()
        Maze.append(row)
    a,b=map(int,input("Please Enter The Coordinates Of The Exit(a,b):").split(","))
    exit=[a-1,b-1]
    a,b=map(int,input("Please Enter The Coordinates Of The Entrance(a,b):").split(","))
    entr=[a-1,b-1]
elif choice==2:
    Maze=[]
    m=random.randint(2,10)
    n=random.randint(2,10)
    weights=[0.7,0.3]
    numbers=[0,1]
    for i in range(n):
        row=[]
        for j in range(m):
            row.append(str(random.choices(numbers,weights,k=1)[0]))
        Maze.append(row)
    exit=[n-1,m-1]
    entr=[0,0]
    print("The maze is as follows:")
    for i in range(n):
        for j in range(m):
            print(Maze[i][j],end="")
        print("\n",end="")
    print("The coordinates of the entrance is:",entr)
    print("The coordinates of the exit is:",exit)
else:
    print("Wrong Input!")

#find the way
st=Stack()#the right way 
exit.append("exit")
st.push(exit)
done=[]#the place already passed
done.append([exit[0],exit[1]])
next_coordinations=Stack()
while [st.top_value()[0],st.top_value()[1]]!=entr:
    next_coordinations=[]
    #find the possibiltis of the next coordination first:1.still valid 2.is "0" 3.have not passed
    if st.top_value()[0]-1>=0 and Maze[st.top_value()[0]-1][st.top_value()[1]]=="0" and [st.top_value()[0]-1,st.top_value()[1]] not in done:
        next_coordinations.append([st.top_value()[0]-1,st.top_value()[1],"upper"])#upper
    if st.top_value()[0]+1<n and Maze[st.top_value()[0]+1][st.top_value()[1]]=="0" and [st.top_value()[0]+1,st.top_value()[1]] not in done:
        next_coordinations.append([st.top_value()[0]+1,st.top_value()[1],"under"])#under
    if st.top_value()[1]-1>=0 and Maze[st.top_value()[0]][st.top_value()[1]-1]=="0" and [st.top_value()[0],st.top_value()[1]-1] not in done:
        next_coordinations.append([st.top_value()[0],st.top_value()[1]-1,"left"])#left
    if st.top_value()[1]+1<m and Maze[st.top_value()[0]][st.top_value()[1]+1]=="0" and [st.top_value()[0],st.top_value()[1]+1] not in done:
        next_coordinations.append([st.top_value()[0],st.top_value()[1]+1,"right"])#right
    #consider a fork:if one comes to an end,we need to back and find another,until we back to the start,taht means there is really no way
    if len(next_coordinations)==0 and [st.top_value()[0],st.top_value()[1]]==[exit[0],exit[1]]:
        break
    elif len(next_coordinations)==0 and [st.top_value()[0],st.top_value()[1]]!=[exit[0],exit[1]]:
        k=st.pop()
    else:
        next=next_coordinations.pop(-1)
        done.append([next[0],next[1]])
        st.push(next)
    
#output
if [st.top_value()[0],st.top_value()[1]]==entr:
    print("The coordinate path out of the maze is as follows:")
    for i in range(st.size()):
        now=st.pop()
        if [now[0],now[1]]!=[exit[0],exit[1]]:
            output=[]
            way=now[2]
            if way=="upper":
                output=[now[0],now[1],"under"]
            if way=="under":
                output=[now[0],now[1],"upper"]
            if way=="left":
                output=[now[0],now[1],"right"]
            if way=="right":
                output=[now[0],now[1],"left"]
            print(output,end="->")
        else:
            print([now[0],now[1]])
else:
    print("The maze has no access!")
    
