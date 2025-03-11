import sys
from PyQt5.QtGui import QColor, QBrush, QPen, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from functools import partial
import random

class Stack():
    def __init__(self):
        self.data = []
        self.top = -1
    def is_empty(self):
        return self.top < 0
    def size(self):
        return self.top + 1
    def top_value(self):
        if self.is_empty():
            raise KeyError("Stack is empty")
        else:
            return self.data[self.top]
    def push(self, value):
        self.top += 1
        self.data.append(value)
    def pop(self):
        if self.is_empty():
            raise KeyError("Stack is empty")
        else:
            value = self.data.pop()
            self.top -= 1
            return value

class MazeSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maze Solver")
        self.resize(1000, 1500) 

        # Create labels and line edits            
        self.label_0 = QLabel("Please design your maze here:", self)
        self.label_0.setGeometry(50, 30, 500, 30)

        self.label_1 = QLabel("Size", self)
        self.label_1.setGeometry(50, 80, 200, 20)

        self.edit_1 = QLineEdit(self)
        self.edit_1.setPlaceholderText("n*m")
        self.edit_1.setGeometry(200, 75, 500, 30)

        self.label_2 = QLabel("Exit", self)
        self.label_2.setGeometry(50, 130, 200, 20)

        self.edit_2 = QLineEdit(self)
        self.edit_2.setPlaceholderText("x,y")
        self.edit_2.setGeometry(200, 125, 500, 30)

        self.label_3 = QLabel("Entrance", self)
        self.label_3.setGeometry(50, 180, 200, 20)
        
        self.edit_3 = QLineEdit(self)
        self.edit_3.setPlaceholderText("x,y")
        self.edit_3.setGeometry(200, 175, 500, 30)

        self.label_4 = QLabel("Maze", self)
        self.label_4.setGeometry(50, 230, 500, 20) 

        self.edit_4 = QTextEdit(self)
        self.edit_4.setPlaceholderText("0 for paths and 1 for walls")  
        self.edit_4.setGeometry(200, 225, 700, 300)  
        self.edit_4.setFixedWidth(700)  
        self.edit_4.setFixedHeight(300)
        
        # Create a button
        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setGeometry(800, 555, 100, 30)
        self.solve_button.clicked.connect(self.solve)
        
        # Create "Over" button
        self.over_button = QPushButton("Over", self)
        self.over_button.setGeometry(450, 1400, 100, 30)
        self.over_button.clicked.connect(self.over)
        
        # Create "Random" button
        self.random_button = QPushButton("Random", self)
        self.random_button.setGeometry(600, 30, 100, 30)
        self.random_button.clicked.connect(self.random)
        
        # Create the drawing area
        self.label_5 = QLabel("Output:", self)
        self.label_5.setGeometry(50, 585, 200, 20)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 700, 700)  
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(100, 630, 800, 700) 

    def random(self):
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
        st = Stack()
        done = []
        st.push(exit)
        done.append(exit)
        while st.top_value() != entr:
            next_coordinations = Stack()
            if st.top_value()[0] - 1 >= 0 and Maze[st.top_value()[0] - 1][st.top_value()[1]] == '0' and [st.top_value()[0] - 1, st.top_value()[1]] not in done:
                next_coordinations.push([st.top_value()[0] - 1, st.top_value()[1]])  # upper
            if st.top_value()[0] + 1 < n and Maze[st.top_value()[0] + 1][st.top_value()[1]] == '0' and [st.top_value()[0] + 1, st.top_value()[1]] not in done:
                next_coordinations.push([st.top_value()[0] + 1, st.top_value()[1]])  # under
            if st.top_value()[1] - 1 >= 0 and Maze[st.top_value()[0]][st.top_value()[1] - 1] == '0' and [st.top_value()[0], st.top_value()[1] - 1] not in done:
                next_coordinations.push([st.top_value()[0], st.top_value()[1] - 1])  # left
            if st.top_value()[1] + 1 < m and Maze[st.top_value()[0]][st.top_value()[1] + 1] == '0' and [st.top_value()[0], st.top_value()[1] + 1] not in done:
                next_coordinations.push([st.top_value()[0], st.top_value()[1] + 1])  # right
            if next_coordinations.is_empty() and st.top_value() == exit:
                break
            elif next_coordinations.is_empty() and st.top_value() != exit:
                st.pop()
            else:
                next = next_coordinations.pop()
                done.append(next)
                st.push(next)
            
        if st.top_value() == entr:
            hello=True
            self.access(Maze,st,hello)
        else:
            hello=False
            self.noaccess(Maze,st,hello)
    def solve(self):
        st = Stack()
        done = [] 
        input_1 = self.edit_1.text()
        input_2 = self.edit_2.text()
        input_3 = self.edit_3.text()
        input_4 = self.edit_4.toPlainText().strip() 

        n, m = map(int, input_1.split("*"))
        x, y = map(int, input_2.split(","))
        exit = [x - 1, y - 1]  
        x, y = map(int, input_3.split(","))
        entr = [x - 1, y - 1]  
        Maze = [i.split() for i in input_4.split('\n')]
        
        st.push(exit)
        done.append(exit)
        while st.top_value() != entr:
            next_coordinations = Stack()
            if st.top_value()[0] - 1 >= 0 and Maze[st.top_value()[0] - 1][st.top_value()[1]] == '0' and [st.top_value()[0] - 1, st.top_value()[1]] not in done:
                next_coordinations.push([st.top_value()[0] - 1, st.top_value()[1]])  # upper
            if st.top_value()[0] + 1 < n and Maze[st.top_value()[0] + 1][st.top_value()[1]] == '0' and [st.top_value()[0] + 1, st.top_value()[1]] not in done:
                next_coordinations.push([st.top_value()[0] + 1, st.top_value()[1]])  # under
            if st.top_value()[1] - 1 >= 0 and Maze[st.top_value()[0]][st.top_value()[1] - 1] == '0' and [st.top_value()[0], st.top_value()[1] - 1] not in done:
                next_coordinations.push([st.top_value()[0], st.top_value()[1] - 1])  # left
            if st.top_value()[1] + 1 < m and Maze[st.top_value()[0]][st.top_value()[1] + 1] == '0' and [st.top_value()[0], st.top_value()[1] + 1] not in done:
                next_coordinations.push([st.top_value()[0], st.top_value()[1] + 1])  # right
            if next_coordinations.is_empty() and st.top_value() == exit:
                break
            elif next_coordinations.is_empty() and st.top_value() != exit:
                st.pop()
            else:
                next = next_coordinations.pop()
                done.append(next)
                st.push(next)
            
        if st.top_value() == entr:
            hello=True
            self.access(Maze,st,hello)
        else:
            hello=False
            self.noaccess(Maze,st,hello)

    def noaccess(self,Maze,st,Hello):
        self.drawMaze(Maze)
        self.next_button = QPushButton("Next", self)
        self.next_button.setGeometry(800, 1300, 100, 30)
        self.next_button.clicked.connect(partial(self.next,Maze, st,Hello))
        self.next_button.show()

    def access(self, st, Maze,Hello):
        self.drawMaze(Maze)
        self.next_button = QPushButton("Next", self)
        self.next_button.setGeometry(800, 1300, 100, 30)
        self.next_button.clicked.connect(partial(self.next,Maze, st,Hello))
        self.next_button.show()
    
    def next(self,Maze, st,Hello):
        if st.is_empty() and Hello ==True:
            text = "Out of maze!"
            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(QColor(255, 0, 0))
            text_item.setPos(200,650.0)
            self.scene.addItem(text_item)
        elif st.top_value()==[len(Maze)-1,len(Maze[0])-1] and Hello==False:
            text = "The maze has no access!"
            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(QColor(255, 0, 0)) 
            text_item.setPos(200,650.0)
            self.scene.addItem(text_item)
        else:
            current_position = st.pop()
            self.drawPath(Maze,current_position)  


    def drawMaze(self, Maze):
        cell_size = 600//max(len(Maze),len(Maze[0]))
        wall_color = QColor(0, 0, 0)   
        for i in range(len(Maze)):
            for j in range(len(Maze[i])):
                if Maze[i][j] == '1':
                    rect_item = QGraphicsRectItem(j * cell_size, i * cell_size, cell_size, cell_size) 
                    rect_item.setBrush(wall_color)
                    self.scene.addItem(rect_item)  
        self.scene.update()

    def drawPath(self, Maze,position):
        cell_size = 600//max(len(Maze),len(Maze[0]))
        path_color = QColor(255, 0, 0) 
        rect_item = QGraphicsRectItem(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)
        rect_item.setBrush(path_color)
        self.scene.addItem(rect_item)  
        
    def over(self):
        self.scene.clear()
        self.edit_1.clear()
        self.edit_2.clear()
        self.edit_3.clear()
        self.edit_4.clear()
        self.solve_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    maze_solver = MazeSolver()
    maze_solver.show()
    sys.exit(app.exec_())
