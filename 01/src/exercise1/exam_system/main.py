from controllers.exam_controller import ExamController

if __name__ == "__main__":
    controller = ExamController()
    controller.load_students()
    controller.load_examiners()
    controller.start_exam()

# сперва в терминале ввести "python -m main.py",
# затем запустить с помощью F5
