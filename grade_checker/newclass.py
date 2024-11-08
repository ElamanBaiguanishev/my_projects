# from PyQt5.QtWidgets import QPushButton
#
#
# class YourMainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # ... (your existing code)
#
#         # Create an instance of WorkerThread
#         self.worker_thread = WorkerThread(service=self.service)
#
#         # Connect the signal to a slot
#         self.worker_thread.signal_error_with_response.connect(self.handle_error_with_response)
#
#         # ... (the rest of your code)
#
#     def handle_error_with_response(self, error_message):
#         # Show a custom QMessageBox with "ДА" (Yes) and "НЕТ" (No) buttons
#         reply_widget = self.create_custom_message_box()
#         reply = reply_widget.exec_()
#
#         # Respond to user input
#         if reply == QMessageBox.Yes:
#             # Continue the thread
#             self.worker_thread.resume()  # You need to implement a resume method in your WorkerThread
#         else:
#             # Stop or handle accordingly
#             self.worker_thread.stop()  # You need to implement a stop method in your WorkerThread
#
#     def create_custom_message_box(self):
#         reply_widget = QWidget()
#         layout = QGridLayout(reply_widget)
#         reply_widget.setWindowTitle('Config DataBase')
#         reply_widget.setGeometry(600, 200, 568, 300)
#         reply_widget.setStyleSheet("background: #f7f7f7")
#         icon = QIcon('resources/favicon.ico')
#         reply_widget.setWindowIcon(icon)
#         reply_widget.setStyleSheet(open("resources/styles.qss").read())
#
#         # Add "ДА" (Yes) and "НЕТ" (No) buttons to the layout
#         layout.addWidget(QPushButton("ДА", clicked=self.handle_yes), 0, 0)
#         layout.addWidget(QPushButton("НЕТ", clicked=self.handle_no), 0, 1)
#
#         return reply_widget
#
#     def handle_yes(self):
#         # Handle "ДА" (Yes) button click
#         print("Yes clicked")
#
#     def handle_no(self):
#         # Handle "НЕТ" (No) button click
#         print("No clicked")