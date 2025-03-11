import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QListWidget, QLabel, QWidget, QFileDialog
)
from algorithm import find_min_cost, write_output,process_and_combine_lines


class PriceOptimizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Optimal Price Shopping System")
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        display_layout = QHBoxLayout()

        # Widgets
        self.input_text = QTextEdit() 
        self.input_text.setPlaceholderText('anually enter the contents of `input.txt` or click the "Read File" button.')
        input_layout.addWidget(QLabel("input.txt:"))
        input_layout.addWidget(self.input_text)

        self.price_list = QListWidget() 
        display_layout.addWidget(QLabel("price.txt:"))
        display_layout.addWidget(self.price_list)

        self.promo_list = QListWidget()  
        display_layout.addWidget(QLabel("promotions.txt:"))
        display_layout.addWidget(self.promo_list)

        self.output_text = QTextEdit()  # 输出框
        self.output_text.setPlaceholderText("Output")
        input_layout.addWidget(QLabel("Optimal Method"))
        input_layout.addWidget(self.output_text)

        # Buttons
        self.load_input_btn = QPushButton("Read input.txt file")
        self.load_input_btn.clicked.connect(self.load_input_file)
        button_layout.addWidget(self.load_input_btn)

        self.load_prices_btn = QPushButton("Read price.txt file")
        self.load_prices_btn.clicked.connect(self.load_price_file)
        button_layout.addWidget(self.load_prices_btn)

        self.load_promos_btn = QPushButton("Read promotions.txt file")
        self.load_promos_btn.clicked.connect(self.load_promotions_file)
        button_layout.addWidget(self.load_promos_btn)

        self.calculate_btn = QPushButton("Caculate min price")
        self.calculate_btn.clicked.connect(self.calculate_min_cost)
        button_layout.addWidget(self.calculate_btn)

        # Main Layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(display_layout)
        main_layout.addLayout(button_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Data
        self.items = []
        self.promotions = []
        self.prices = {}

    def load_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "open input.txt file", "", "Text Files (*.txt)")
        encodings = ['utf-8', 'utf-16', 'ISO-8859-1']
        for encoding in encodings:
            try:
                with open(file_name, "r", encoding=encoding) as f:
                    content = f.read()
                    self.input_text.setText(content)
                break
            except UnicodeDecodeError:
                self.statusBar().showWarningMessage(f"Error: {encoding}")

    def load_price_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "open price.txt file", "", "Text Files (*.txt)")
        encodings = ['utf-8', 'utf-16', 'ISO-8859-1']
        for encoding in encodings:
            try:
                with open(file_name, "r", encoding=encoding) as f:
                    lines = f.readlines()
                self.prices = {int(line.split()[0]): float(line.split()[1]) for line in lines}
                self.price_list.clear()
                for item_id, price in self.prices.items():
                    self.price_list.addItem(f"ID: {item_id}, Price: {price}")
                break
            except UnicodeDecodeError:
                self.statusBar().showWarningMessage(f"Error: {encoding}")


    def load_promotions_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "open promotions.txt 文件", "", "Text Files (*.txt)")
        encodings = ['utf-8', 'utf-16', 'ISO-8859-1']
        for encoding in encodings:
            try:
                with open(file_name, "r", encoding=encoding) as f:
                    lines = f.readlines()
                promo_count = int(lines[0].strip())
                self.promotions = []
                for line in lines[1:]:
                    data = line.strip().split()
                    item_types = int(data[0])
                    promo_items = []
                    for i in range(item_types):
                        promo_items.append({"id": int(data[1 + i * 2]), "qty": int(data[2 + i * 2])})
                    promo_price = float(data[-1])
                    self.promotions.append({"items": promo_items, "price": promo_price})
                self.promo_list.clear()
                for promo in self.promotions:
                    self.promo_list.addItem(f"Promo: {promo['items']} -> ${promo['price']}")
                break
            except UnicodeDecodeError:
                self.statusBar().showWarningMessage(f"Error: {encoding}")

    def calculate_min_cost(self):
        try:
            # Parse input from the text box
            input_data = self.input_text.toPlainText().strip().split("\n")
            item_count = int(input_data[0])
            self.items = []
            for line in input_data[1:]:
                id_, qty, price = line.strip().split()
                self.items.append({"id": int(id_), "qty": int(qty), "price": float(price)})

            # Update prices in items
            for item in self.items:
                if item["id"] in self.prices:
                    item["price"] = self.prices[item["id"]]

            # Calculate minimum cost
            min_cost, plan = find_min_cost(self.items, self.promotions)
            output_plan = process_and_combine_lines(plan,self.prices)
            # Write and display output
            if write_output("output.txt", min_cost, output_plan) == True:
                self.statusBar().showMessage('output.txt success inputing', 3000)
            self.output_text.setText(f"min: {min_cost:.2f}\n" +"method: \n"+"\n".join(f"- {step}" for step in output_plan))
        except Exception as e:
            self.output_text.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PriceOptimizerApp()
    main_window.show()
    sys.exit(app.exec_())
