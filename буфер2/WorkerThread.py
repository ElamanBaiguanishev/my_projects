import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import json
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QGridLayout, QPushButton
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tools import log_exception


class WorkerThread(QThread):
    # signal_error = pyqtSignal(str)
    # choice_error = pyqtSignal(str)
    # update_progress_signal = pyqtSignal(int, str)

    def __init__(self, service):
        super().__init__()
        self.current_test_name = None
        self.current_group = None
        self.current_lesson = None
        self.students = None
        self.dict_semestr_lesson = None
        self.tests = None
        self.test_url = None

        self.student_ids = None
        self.lessons = None
        self.current_semestr = None

    def run(self):
        try:
            pass
        except Exception as e:
            self.signal_error.emit(str(e))
