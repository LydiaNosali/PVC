import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import networkx as nwx
import numpy as np
import time


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget()
        self.layout = QVBoxLayout()
        self.title = 'Création du graphe'
        self.left = 100
        self.top = 100
        self.width = 880
        self.height = 700

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon("c.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        btn = QPushButton('Suivant', self)
        btn.setToolTip('Cliquez pour afficher le graphe')
        btn.resize(btn.sizeHint())
        btn.move(350, 500)
        btn.clicked.connect(self.on_click)
        # Show widget
        self.show()

    def createTable(self):
        # Create table
        i, okPressed = QInputDialog.getInt(self, "Nombre de sommets", "Nombre de sommets:", 5, 0, 100, 1)
        if okPressed:
            self.tableWidget.setRowCount(i)
            self.tableWidget.setColumnCount(i)
            for j in range(i):
                for k in range(i):
                    self.tableWidget.setItem(k, j, QTableWidgetItem("0"))
                    self.tableWidget.setItem(j, k, QTableWidgetItem("0"))
            self.tableWidget.move(0, 0)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        row = self.tableWidget.rowCount()
        column = self.tableWidget.columnCount()
        text = ''
        for r in range(row):
            for c in range(column):
                text = text + ' ' + self.tableWidget.item(r, c).text()
        entries = list(map(int, text.split()))
        A = np.array(entries).reshape(row, column)
        G = nwx.from_numpy_matrix(np.matrix(A), create_using=nwx.Graph)
        color_map = ['orange']
        labels = nwx.get_edge_attributes(G, "weight")
        layout = nwx.spring_layout(G)
        nwx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        start_time = time.time()
        edges = sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1))
        PVC = []
        for e in edges:
            if e[1] not in PVC:
                PVC.append(e[1])
            if e[0] not in PVC:
                PVC.append(e[0])
        print('le cycle est :')
        for vertex in PVC:
            print(vertex)
        print(PVC[0])
        cout = 0
        for i in range(len(PVC) - 1):
            try:
                cout += G[PVC[i]][PVC[i + 1]]['weight']
            except:
                print("pas de cycle3")
                raise

        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        cout += G[PVC[0]][PVC[len(PVC) - 1]]['weight']
        print('Son cout :')
        print(cout)
        H = list()
        for i in range(len(PVC) - 1):
            H.append((PVC[i], PVC[i + 1]))
        H.append((PVC[1], PVC[0]))
        H.append((PVC[0], PVC[len(PVC) - 1]))
        edge_colors = ['orange' if e in H else 'black' for e in G.edges]
        nwx.draw(G, layout, node_color=color_map, edge_color=edge_colors, width=4, with_labels=True)

        self.resultat = QLabel("Le cycle de la méthode vorace est : " + str(PVC) + "\n" + "Son cout est : " + "\n" +
                               str(cout))
        self.resultat.setWindowIcon(QtGui.QIcon("c.png"))
        self.resultat.setWindowTitle(self.title)
        self.resultat.setGeometry(self.left, self.top, self.width, self.height)

        self.resultat.setAlignment(Qt.AlignCenter)

        p = self.resultat.palette()
        p.setColor(self.resultat.backgroundRole(), Qt.darkGray)
        self.resultat.setPalette(p)

        newfont = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.resultat.setFont(newfont)

        self.resultat.show()
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
