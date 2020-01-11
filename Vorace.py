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
        self.width = 600
        self.height = 600

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
        btn.move(500, 500)
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
        color_map = ['green']
        labels = nwx.get_edge_attributes(G, "weight")
        layout = nwx.spring_layout(G)
        nwx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        respath = []
        cout = 0
        for start in range(row):
            path = [start]
            visited = [False] * row
            visited[start] = True
            respath = hamiltonian_path(G, start, visited, row, path)
        for i in range(len(respath) - 1):
            cout = cout + G[respath[i]][respath[i + 1]]['weight']
        cout += G[respath[0]][respath[len(respath) - 1]]['weight']
        print('Le cycle le plus optimal est :')
        for vertex in respath:
            print(vertex)
        print(respath[0])
        print('Son cout est = ', cout, "\n")
        H = list()
        for i in range(len(respath) - 1):
            H.append((respath[i], respath[i + 1]))
            H.append((respath[i + 1], respath[i]))
        H.append((respath[0], respath[len(respath) - 1]))
        edge_colors = ['orange' if e in H else 'black' for e in G.edges]
        nwx.draw(G, layout, node_color=color_map, edge_color=edge_colors, width=4, with_labels=True)

        self.resultat = QLabel("Le cycle de la méthode exhaustive est : " + str(respath) + "\n" + "Son cout est : "
                               + "\n" + str(cout))
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


def hamiltonian_path(G, v, visited, N, path=[], couts=[], respath=[]):
    if len(path) == N:
        cout = 0
        for i in range(len(path) - 1):
            cout = cout + G[path[i]][path[i + 1]]['weight']
        cout += G[path[0]][path[len(path) - 1]]['weight']
        for i in couts:
            if i == cout:
                return
        couts.append(cout)
        if min(couts) == cout:
            respath.clear()
            for i in range(len(path)):
                respath.insert(i, path[i])
        print('Cycle:')
        for vertex in path:
            print(vertex)
        print(path[0])
        print('cout = ', cout, "\n")
        return
    for w in G[v]:
        if not visited[w]:
            visited[w] = True
            path.append(w)
            hamiltonian_path(G, w, visited, N, path)
            visited[w] = False
            path.remove(path[len(path) - 1])
    return respath


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
