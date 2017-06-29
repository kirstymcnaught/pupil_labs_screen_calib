import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PupilController import PupilController

# Main Function
if __name__ == '__main__':

    # Create main app
    myApp = QApplication(sys.argv)

    # Create a view and set its properties
    view = QQuickView()
    view.setSource(QUrl('layout.qml'))
    context = view.rootContext()
    root = view.rootObject()

    # Create a pupil controller, pass to QML
    pupil = PupilController()
    context.setContextProperty('pupil', pupil)

    pupil.ready.connect(root.onPupilReady)

    # Launch the app
    view.show()
    myApp.exec_()
    sys.exit()
