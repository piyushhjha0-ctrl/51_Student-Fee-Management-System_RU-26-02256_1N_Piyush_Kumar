"""Student Fee Management System (PS No. 51)"""

FILE_NAME = "fees.txt"

COURSE_FEES = {
    "BCA": 45000,
    "BTECH": 60000,
    "MBA": 80000,
}

COURSE_NAMES = {
    "BCA": "BCA",
    "BTECH": "BTech",
    "MBA": "MBA",
}


def get_total(student):
    return COURSE_FEES[student['course'].upper()]


def get_due(student):
    return get_total(student) - student["paid"]


def get_status(student):
    due = get_due(student)
    if due == 0:
        return "Paid"
    elif student["paid"] > 0:   
        return "Partial"
    else:
        return "Unpaid"


def load_records():
    student = []
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                roll, name, course, paid = parts
                if course.upper() not in COURSE_FEES or not paid.isdigit():
                    continue
                student.append({
                    "roll": roll,
                    "name": name,
                    "course": COURSE_NAMES[course.upper()],
                    "paid": int(paid),
                })
    except FileNotFoundError:
        pass
    return student


def save_records(students):
    with open(FILE_NAME, "w") as f:
        for s in students:
            f.write(f"{s['roll']},{s['name']},{s['course']},{s['paid']}\n")


def find_student(students, roll):
    for s in students:
        if s["roll"] == roll:
            return s
    return None   


def add_student(students):
    roll = input("Roll: ").strip()
    if roll == "":
        print("Roll number cannot be empty.")
        return
    if find_student(students, roll) is not None:
        print("Roll number already exists, Student not added.")
        return

    name = input("Name: ").strip()
    if name == "" or "," in name:
        print("Invalid name. It must not be empty or contain a comma.")
        return

    course = input("Course (BCA/BTech/MBA): ").strip()
    if course.upper() not in COURSE_FEES:
        print("Invalid course. Choose from BCA, BTech, MBA.")
        return

    student = {"roll": roll, "name": name,
               "course": COURSE_NAMES[course.upper()], "paid": 0}
    students.append(student)
    save_records(students)
    print(f"Student added: {roll} | {name} | {student['course']} | "
          f"Total Fee: {get_total(student)} | Paid: 0 | "
          f"Due: {get_due(student)} | Status: {get_status(student)}")


def pay_fee(students):
    roll = input("Roll: ").strip()
    student = find_student(students, roll)
    if student is None:
        print("Student not found.")
        return

    try:
        amount = int(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Enter a whole number.")
        return

    due = get_due(student)
    if due == 0:
        print("No dues pending. Fee already fully paid.")
    elif amount <= 0:
        print("Amount must be greater than zero. Payment rejected.")
    elif amount > due:
        print(f"Amount exceeds due ({due}). Payment rejected.")
    else:
        student["paid"] += amount
        save_records(students)
        print(f"Payment received. Paid: {student['paid']} | "
              f"Due: {get_due(student)} | Status: {get_status(student)}")


def search_student(students):
    roll = input("Roll: ").strip()
    student = find_student(students, roll)
    if student is None:
        print("Student not found.")
        return
    print(f"{student['roll']} | {student['name']} | {student['course']} | "
          f"Total Fee: {get_total(student)} | Paid: {student['paid']} | "
          f"Due: {get_due(student)} | Status: {get_status(student)}")


def pending_dues(students):
    found = False
    for s in students:
        due = get_due(s)
        if due > 0:
            print(f"{s['roll']} | {s['name']} | Due: {due}")
            found = True
    if not found:
        print("No pending dues.")


def main():
    students = load_records()
    while True:
        print("\n===== Student Fee Management System =====")
        print("1. Add student")
        print("2. Pay fee")
        print("3. Search by roll number")
        print("4. Pending dues")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            pay_fee(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            pending_dues(students)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()