import os
import csv

from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Initializes the Logic class, sets up UI
        """
        super().__init__()
        self.setupUi(self)

        self.label_score_1.setVisible(False)
        self.label_score_2.setVisible(False)
        self.label_score_3.setVisible(False)
        self.label_score_4.setVisible(False)
        self.lineEdit_score_1.setVisible(False)
        self.lineEdit_score_2.setVisible(False)
        self.lineEdit_score_3.setVisible(False)
        self.lineEdit_score_4.setVisible(False)
        self.pushButton_submit.setVisible(False)
        self.label_confirm.setVisible(False)
        self.pushButton_new.setVisible(False)

        self.pushButton_validate.clicked.connect(self.validate)
        self.pushButton_submit.clicked.connect(self.submit)
        self.pushButton_new.clicked.connect(self.new_vote)

    def name_info(self) -> bool:
        """
        This function is responsible for getting the name of the student
        -If the input isn't an alphabetical letter or is empty, an error is displayed
        -Depending on the error, the message box will be critical or simply a warning
        :return: True if the input is correct
        """
        try:
            name_input = self.lineEdit_name.text()
            if not name_input:
                raise ValueError('Box Is Empty.')
            if not name_input.isalpha():
                raise ValueError('Use Only Alphabetical Letters.')

            return True

        except ValueError as e:
            name_error_message = str(e)
            if 'Box Is' in name_error_message:
                QMessageBox.warning(self, 'Error', str(e))
                return False
            elif 'Use Only' in name_error_message:
                QMessageBox.critical(self, 'Error', str(e))
                return False


    def attempts_info(self) -> bool:
        """
        This function is responsible for getting the number of attempts from the student
        -If the input isn't a numerical value or is greater than 4 or less than 1, an error is displayed
        -Depending on the input by the user, the number of attempts will be displayed
        :return: True if the input is correct
        """
        try:
            attempts_input = self.lineEdit_attempts.text()
            if not attempts_input.isdigit():
                raise ValueError('Use Only Numerical Values.')

            attempts = int(attempts_input)
            if attempts > 4 or attempts < 1:
                raise ValueError('Only Enter 1-4 Scores.')

            self.lineEdit_score_1.setVisible(False)
            self.lineEdit_score_2.setVisible(False)
            self.lineEdit_score_3.setVisible(False)
            self.lineEdit_score_4.setVisible(False)

            if attempts >= 1:
                self.label_score_1.setVisible(True)
                self.lineEdit_score_1.setVisible(True)
            if attempts >= 2:
                self.label_score_2.setVisible(True)
                self.lineEdit_score_2.setVisible(True)
            if attempts >= 3:
                self.label_score_3.setVisible(True)
                self.lineEdit_score_3.setVisible(True)
            if attempts >= 4:
                self.label_score_4.setVisible(True)
                self.lineEdit_score_4.setVisible(True)
            self.pushButton_submit.setVisible(True)
            return True

        except ValueError as e:
            name_error_message = str(e)
            if 'Numerical Values' in name_error_message:
                QMessageBox.critical(self, 'Error', str(e))
                return False
            elif '1-4 Scores' in name_error_message:
                QMessageBox.warning(self, 'Error', str(e))
                return False


    def validate(self) -> None:
        """
        Responsible for checking if the name and attempt information is correct
        -Calls on both the name_info function and attempts_info
        -If the check passes without issue, the validate button will disappear
        :return: None
        """
        if self.name_info() and self.attempts_info():
            self.pushButton_validate.setVisible(False)
        else:
            self.pushButton_validate.setVisible(True)


    def check_scores(self):
        """
        Checks the scores entered by the user
        -Checks to ensure the score is between 1 and 100
        -If the score is invalid, an error message will be displayed
        :return: List of scores if they are valid
        """
        try:
            scores =[]

            score1 = self.lineEdit_score_1.text()
            if score1:
                score1 =int(score1)
                if not (0 <= score1 <= 100):
                    raise ValueError('Score 1 Must Be 0-100')
                scores.append(score1)
            score2 = self.lineEdit_score_2.text()
            if score2:
                score2 = int(score2)
                if not (0 <= score2 <= 100):
                    raise ValueError('Score 2 Must Be 0-100')
                scores.append(score2)
            score3 = self.lineEdit_score_3.text()
            if score3:
                score3 = int(score3)
                if not (0 <= score3 <= 100):
                    raise ValueError('Score 3 Must Be 0-100')
                scores.append(score3)
            score4 = self.lineEdit_score_4.text()
            if score4:
                score4 = int(score4)
                if not (0 <= score4 <= 100):
                    raise ValueError('Score 4 Must Be 0-100')
                scores.append(score4)
            return scores

        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
            return None


    def average(self, scores):
        """
        Calculates the average of the scores
        -Divides the sum of the scores list by the length of the scores list
        :param scores: The list of integers(student's scores)
        :return: The average of the list of scores
        """
        if scores:
            return sum(scores) / len(scores)


    def store_csv(self, scores, average):
        """
        Store the name of the student, the scores, and the average in a csv file
        -Appends the information to 'grades.csv'
        -If 'grades.csv' is empty, the header row is added
        :param scores: The list of scores
        :param average: The average of the list of scores
        :return: None
        """
        student_name = self.lineEdit_name.text()
        file_exists = os.path.exists('grades.csv')

        with open('grades.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Student Name', 'Scores', 'Average'])
            writer.writerow([student_name] + scores + [average])


    def submit(self) -> None:
        """
        Submits the name of the student, the scores, and the grade
        -Calls on check_scores to validate input and calls on calc_grade to get grade
        -Depending on the grade, a certain message will be shown
        -Doing so also shows the 'See Results' button
        :return: None
        """
        if self.name_info() and self.attempts_info():
            if self.check_scores():
                avg = self.average(self.check_scores())
                self.store_csv(self.check_scores(), avg)
                student_name = self.lineEdit_name.text()
                grade = self.calc_grade(avg)
                self.label_message.setVisible(True)
                if grade == 'A':
                    self.label_message.setStyleSheet('color: blue')
                    self.label_message.setText(f'{student_name}\'s grade is an A!\nGreat Work!')
                    self.pushButton_new.setVisible(True)
                elif grade == 'B':
                    self.label_message.setStyleSheet('color: green')
                    self.label_message.setText(f'{student_name}\'s grade is a B!\nYou can do better than that!')
                    self.pushButton_new.setVisible(True)
                elif grade == 'C':
                    self.label_message.setStyleSheet('color: yellow')
                    self.label_message.setText(f'{student_name}\'s grade is a C!\nYou did okay.')
                    self.pushButton_new.setVisible(True)
                elif grade == 'D':
                    self.label_message.setStyleSheet('color: orange')
                    self.label_message.setText(f'{student_name}\'s grade is a D!\nNot great!')
                    self.pushButton_new.setVisible(True)
                elif grade == 'F':
                    self.label_message.setStyleSheet('color: red')
                    self.label_message.setText(f'{student_name}\'s grade is a F!\nDid you try your best?')
                    self.pushButton_new.setVisible(True)
                self.label_confirm.setVisible(True)
            else:
                self.label_confirm.setVisible(False)

    def calc_grade(self, average: float) -> str:
        """
        Calculates the grade depending on the average score of the student
        :param average: The average of the student's scores
        :return: The grade associated with the average score of the student
        """
        max_score = 100
        if average >= max_score - 10:
            return 'A'
        elif average >= max_score - 20:
            return 'B'
        elif average >= max_score - 30:
            return 'C'
        elif average >= max_score - 40:
            return 'D'
        else:
            return 'F'


    def new_vote(self) -> None:
        """
        Resets the UI for a new set of student scores
        -Clears all input boxes and hides dynamic components
        :return: None
        """
        if self.pushButton_new:
            self.label_score_1.setVisible(False)
            self.label_score_2.setVisible(False)
            self.label_score_3.setVisible(False)
            self.label_score_4.setVisible(False)
            self.lineEdit_score_1.setVisible(False)
            self.lineEdit_score_2.setVisible(False)
            self.lineEdit_score_3.setVisible(False)
            self.lineEdit_score_4.setVisible(False)
            self.pushButton_submit.setVisible(False)
            self.label_confirm.setVisible(False)
            self.pushButton_new.setVisible(False)
            self.label_message.setVisible(False)
            self.lineEdit_name.clear()
            self.lineEdit_attempts.clear()
            self.lineEdit_score_1.clear()
            self.lineEdit_score_2.clear()
            self.lineEdit_score_3.clear()
            self.lineEdit_score_4.clear()
            self.pushButton_validate.setVisible(True)