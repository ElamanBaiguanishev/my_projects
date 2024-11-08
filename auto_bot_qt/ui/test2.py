from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel

app = QApplication([])
window = QWidget()

tab_widget = QTabWidget()
tab1 = QLabel('This is tab 1')
tab2 = QLabel('This is tab 2')

tab_widget.addTab(tab1, 'Tab 1')
tab_widget.addTab(tab2, 'Tab 2')

layout = QVBoxLayout()
layout.addWidget(tab_widget)
window.setLayout(layout)

window.show()
app.exec_()
