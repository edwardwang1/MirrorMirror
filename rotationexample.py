import sys
from PyQt4 import QtGui, QtCore

class myApplication(QtGui.QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        #---- Prepare a Pixmap ----

        
        pixmap = QtGui.QPixmap("icons/clockFace.png")

        #---- Embed Pixmap in a QLabel ----

        diag = (pixmap.width()**2 + pixmap.height()**2)**0.5

        self.label = QtGui.QLabel()
        self.label.setMinimumSize(diag, diag)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(pixmap)

        #---- Prepare a Layout ----

        grid = QtGui.QGridLayout()

        button = QtGui.QPushButton('Rotate 15 degrees')
        button.clicked.connect(self.rotate_pixmap)

        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

        self.setLayout(grid)

        self.rotation = 0
        #self.setFixedSize(760, 520)

    def rotate_pixmap(self):

        #---- rotate ----

        # Rotate from initial image to avoid cumulative deformation from
        # transformation

        pixmap = QtGui.QPixmap("icons/clockFace.png")
        self.rotation += 15

        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----

        self.label.setPixmap(pixmap)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    instance = myApplication()  
    instance.show()    

    sys.exit(app.exec_())
