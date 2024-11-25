# Define a function to input grades
def input_grades(grades):
    while True:
        print("\nMenu:")
        print("1. Add Grade")
        print("2. Remove Grade")
        print("3. View Grades")
        print("4. Calculate Average")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            subject = input("Enter subject: ")
            try:
                grade = float(input(f"Enter grade for {subject}: "))
                grades[subject] = grade
                print(f"Grade added for {subject}.")
            except ValueError:
                print("Invalid grade. Please enter a numerical value.")
        elif choice == '2':
            subject = input("Enter subject to remove: ")
            if subject in grades:
                del grades[subject]
                print(f"Grade removed for {subject}.")
            else:
                print("Subject not found.")
        elif choice == '3':
            print("\nGrades:")
            for subject, grade in grades.items():
                print(f"{subject}: {grade}")
        elif choice == '4':
            average_grade = calculate_average(grades)
            print(f"\nAverage Grade: {average_grade:.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Define a function to calculate the average grade
def calculate_average(grades):
    if not grades:
        return 0.0
    total = sum(grades.values())
    return total / len(grades)

# Main function
def main():
    print("Student Grade Tracker")
    student_grades = {}
    input_grades(student_grades)

    print("\nFinal Grades:")
    for subject, grade in student_grades.items():
        print(f"{subject}: {grade}")

    average_grade = calculate_average(student_grades)
    print(f"\nFinal Average Grade: {average_grade:.2f}")

if __name__ == "__main__":
    main()
