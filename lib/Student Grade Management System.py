import json

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.courses = {}  # course: grade

    def add_course(self, course_name, grade):
        self.courses[course_name] = grade

    def update_grade(self, course_name, new_grade):
        if course_name in self.courses:
            self.courses[course_name] = new_grade
        else:
            print(f"Course '{course_name}' not found.")

    def calculate_gpa(self):
        if not self.courses:
            return 0
        total = sum(self.courses.values())
        return round(total / len(self.courses), 2)

    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "courses": self.courses
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["student_id"])
        student.courses = data["courses"]
        return student

    def __str__(self):
        courses_str = "\n  ".join([f"{c}: {g}" for c, g in self.courses.items()])
        return f"Name: {self.name}\nID: {self.student_id}\nCourses:\n  {courses_str}\nGPA: {self.calculate_gpa()}"


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self):
        name = input("Enter student name: ")
        student_id = input("Enter student ID: ")
        student = Student(name, student_id)

        while True:
            course = input("Enter course name (or 'done' to finish): ")
            if course.lower() == 'done':
                break
            try:
                grade = float(input(f"Enter grade for {course}: "))
                student.add_course(course, grade)
            except ValueError:
                print("Invalid grade. Please enter a number.")

        self.students.append(student)
        print("✅ Student added successfully!\n")

    def view_all_students(self):
        if not self.students:
            print("No students available.")
            return
        for student in self.students:
            print("=" * 40)
            print(student)
            print("=" * 40)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_student_grade(self):
        student_id = input("Enter student ID: ")
        student = self.find_student(student_id)
        if student:
            course = input("Enter course name to update: ")
            try:
                new_grade = float(input("Enter new grade: "))
                student.update_grade(course, new_grade)
                print("✅ Grade updated.")
            except ValueError:
                print("Invalid grade input.")
        else:
            print("❌ Student not found.")

    def save_to_file(self, filename="students.json"):
        with open(filename, "w") as f:
            data = [student.to_dict() for student in self.students]
            json.dump(data, f)
        print("💾 Data saved to file.")

    def load_from_file(self, filename="students.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
            print("📂 Data loaded from file.")
        except FileNotFoundError:
            print("❌ File not found. Starting with an empty list.")


def main():
    manager = StudentManager()
    manager.load_from_file()

    while True:
        print("\n===== Student Grade Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student Grade")
        print("4. Save Data")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            manager.add_student()
        elif choice == '2':
            manager.view_all_students()
        elif choice == '3':
            manager.update_student_grade()
        elif choice == '4':
            manager.save_to_file()
        elif choice == '5':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
