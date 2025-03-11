#design a maze
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

#find the way
done=[]
bingo=False
def judge(coordination,Maze,done) :
    global bingo
    done.append(coordination)
    if coordination==entr:
        return True
    else:
        next_coordinations=[]
        if coordination[0]-1>=0 and Maze[coordination[0]-1][coordination[1]]=="0" and [coordination[0]-1,coordination[1]] not in done:
            next_coordinations.append([coordination[0]-1,coordination[1]])#upper
        if coordination[0]+1<n and Maze[coordination[0]+1][coordination[1]]=="0" and [coordination[0]+1,coordination[1]] not in done:
            next_coordinations.append([coordination[0]+1,coordination[1]])#under
        if coordination[1]-1>=0 and Maze[coordination[0]][coordination[1]-1]=="0" and [coordination[0],coordination[1]-1] not in done:
            next_coordinations.append([coordination[0],coordination[1]-1])#left
        if coordination[1]+1<m and Maze[coordination[0]][coordination[1]+1]=="0" and [coordination[0],coordination[1]+1] not in done:
            next_coordinations.append([coordination[0],coordination[1]+1])#right
        if len(next_coordinations)!=0:
            for i in next_coordinations:
                bingo=judge(i,Maze,done)
                if bingo:
                    if coordination==exit:
                        i.append(coordination)
                        print(i,"->",coordination)
                        break
                    else:
                        i.append(coordination)
                        print(i,end="->")
                        break
        return bingo
if judge(exit,Maze,done)==False:
    print("The maze has no access!")
                
            