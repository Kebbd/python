class Student:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name


class Teacher:
    def __init__(self, first_name, last_name, subject, class_names=None):
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject
        self.class_names = []


class Tutor:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name


class School:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.tutors = []
        self.classes = set()

    def create_student(self):
        student_first_name = input("Podaj imie ucznia: ")
        student_last_name = input("Podaj nazwisko ucznia: ")
        student_class_name = input("Podaj klase ucznia: ")
        student = Student(student_first_name, student_last_name, student_class_name)
        self.students.append(student)
        self.classes.add(student_class_name)

    def create_teacher(self):
        teacher_first_name = input("Podaj imie nauczyciela: ")
        teacher_last_name = input("Podaj nazwisko nauczyciela: ")
        teacher_subject = input("Podaj przedmiot nauczyciela: ")
        teacher = Teacher(teacher_first_name, teacher_last_name, teacher_subject)
        while True:
            class_name = input("Podaj klase uczona przez nauczyciela: ")
            if class_name:
                teacher.class_names.append(class_name)
                self.classes.add(class_name)
            else:
                self.teachers.append(teacher)
                break

    def create_tutor(self):
        tutor_first_name = input("Podaj imie wychowacy: ")
        tutor_last_name = input("Podaj nazwisko wychowawcy: ")
        tutor_class_name = input("Podaj klase wychowawcy: ")
        tutor = Tutor(tutor_first_name, tutor_last_name, tutor_class_name)
        self.tutors.append(tutor)
        self.classes.add(tutor_class_name)

    def show_class(self):
        search_class = input("Podaj klase: ")
        if search_class in self.classes:
            find_tutor = False
            find_student = False
            for tutor in self.tutors:
                if tutor.class_name == search_class:
                    find_tutor = True
                    print(f"Wychowawca: {tutor.first_name} {tutor.last_name}")
            if not find_tutor:
                print("Klasa nie ma wychowawcy")
            for student in self.students:
                if student.class_name == search_class:
                    find_student = True
                    print(f"Uczen: {student.first_name} {student.last_name}")
            if not find_student:
                print("Klasa nie ma uczniow.")
        else:
            print("Nie ma takiej klasy.")

    def show_student(self):
        student_first_name = input("Podaj Imie ucznia: ")
        student_last_name = input("Podaj nazwisko ucznia: ")
        find_student = False
        for student in self.students:
            if (student.first_name == student_first_name and student.last_name == student_last_name):
                find_student = True
                print("Zajecia ucznia to: ")
                find_subject = False
                for teacher in self.teachers:
                    if student.class_name in teacher.class_names:
                        print(f"Przedmiot: {teacher.subject}, Nauczyciel: {teacher.first_name} {teacher.last_name}")
                        find_subject = True
                if not find_subject:
                    print("Uczen nie ma przypisanych zajec.")
        if not find_student:
            print("Nie ma takiego ucznia.")

    def show_teacher(self):
        teacher_first_name = input("Podaj Imie nauczyciela: ")
        teacher_last_name = input("Podaj nazwisko nauczyciela: ")
        find_teacher = False
        for teacher in self.teachers:
            if (teacher.first_name == teacher_first_name and teacher.last_name == teacher_last_name):
                find_teacher = True
                for class_name in teacher.class_names:
                    print(class_name)
        if not find_teacher:
            print("Nie ma takiego nauczyciela.")

    def show_tutor(self):
        tutor_first_name = input("Podaj Imie wychowawcy: ")
        tutor_last_name = input("Podaj nazwisko wychowawcy: ")
        find_tutor = False
        for tutor in self.tutors:
            if (
                tutor.first_name == tutor_first_name
                and tutor.last_name == tutor_last_name
            ):
                find_tutor = True
                find_student = False
                for student in self.students:
                    if student.class_name == tutor.class_name:
                        find_student = True
                        print(f"Uczen: {student}")
                if not find_student:
                    print("Wychowawca nie ma uczniow.")
        if not find_tutor:
            print("Nie ma takiego wychowacy.")


school = School()

while True:
    print("MENU")
    print("1.Utworz")
    print("2.Zarzadzaj")
    print("3.Koniec")
    choice = input("Wybierz numer:\n")

    if choice == "1":
        while True:
            print("Panel tworzenia urzytkownikow:")
            print("1.Uczen")
            print("2.Nauczyciel")
            print("3.Wychowawca")
            print("4.Koniec")
            second_choice = input("Wybierz numer:\n")
            if second_choice == "1":
                school.create_student()
            elif second_choice == "2":
                school.create_teacher()
            elif second_choice == "3":
                school.create_tutor()
            elif second_choice == "4":
                break
            else:
                print("Bledna wartosc.")

    elif choice == "2":
        while True:
            print("Panel zarzadzania:")
            print("1.Klasa")
            print("2.Uczen")
            print("3.Nauczyciel")
            print("4.Wychowawca")
            print("5.Koniec")
            second_choice = input("Wybierz numer:\n")

            if second_choice == "1":
                school.show_class()
            elif second_choice == "2":
                school.show_student()
            elif second_choice == "3":
                school.show_teacher()
            elif second_choice == "4":
                school.show_tutor()
            elif second_choice == "5":
                break
            else:
                print("Bledna wartosc")

    elif choice == "3":
        break
    else:
        print("Bledna wartosc")
