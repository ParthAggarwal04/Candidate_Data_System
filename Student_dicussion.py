import sqlite3

connection = sqlite3.connect("exam.db")
cursor = connection.cursor()

'''cursor.execute("DROP TABLE IF EXISTS student")'''

cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    college_name TEXT NOT NULL,
    round1_marks REAL NOT NULL,
    round2_marks REAL NOT NULL,
    round3_marks REAL NOT NULL,
    technical_round_marks REAL NOT NULL,
    total_marks REAL NOT NULL,
    result TEXT NOT NULL,
    rank INTEGER
)
""")

connection.commit()


def get_text(message, max_len):
    while True:
        value = input(message).strip()

        if value == "":
            print("Field cannot be empty.")

        elif len(value) > max_len:
            print(f"Maximum allowed length is {max_len} characters.")

        elif not value.replace(" ", "").isalpha():
            print("Only alphabets and spaces are allowed.")

        else:
            return value


def get_marks(message, min_marks, max_marks):
    while True:
        try:
            marks = float(input(message))

            if marks < min_marks or marks > max_marks:
                print(f"Marks have to be between {min_marks} and {max_marks}.")
            else:
                return marks

        except ValueError:
            print("Kindly use valid numeric values.")


def cal_total_marks(round1, round2, round3, technical):
    total = round1 + round2 + round3 + technical
    return total


def cal_result(round1, round2, round3, technical,total_marks):
    round1_cutoff =  10 * 0.65
    round2_cutoff = 10 * 0.65
    round3_cutoff = 10 * 0.65
    technical_cutoff = 20 * 0.65
    if total_marks < 35:
        return "Rejected"
    elif round1 < round1_cutoff :
        return "Rejected"
    elif round2 < round2_cutoff :
        return "Rejected"
    elif round3 < round3_cutoff :
        return "Rejected"
    elif technical < technical_cutoff :
        return "Rejected"
    else:
        return "Selected"


def update_rank():
    cursor.execute("""
        SELECT id, total_marks
        FROM student
        ORDER BY total_marks DESC
    """)

    records = cursor.fetchall()

    current_rank = 0
    previous_marks = None
    actual_position = 0

    for record in records:
        actual_position += 1

        student_id = record[0]
        total_marks = record[1]

        if total_marks != previous_marks:
            current_rank += 1

        cursor.execute("""
            UPDATE student
            SET rank = ?
            WHERE id = ?
        """, (current_rank, student_id))

        previous_marks = total_marks

    connection.commit()


def add_student():
    print("\nAdd Candidate Details\n")

    student_name = get_text("Enter Student Name: ", 30)
    college_name = get_text("Enter College Name: ", 50)

    round1_marks = get_marks("Enter Round 1 Marks (0 to 10): ", 0, 10)
    round2_marks = get_marks("Enter Round 2 Marks (0 to 10): ", 0, 10)
    round3_marks = get_marks("Enter Round 3 Marks (0 to 10): ", 0, 10)
    technical_round_marks = get_marks("Enter Technical Round Marks (0 to 20): ", 0, 20)

    total_marks = cal_total_marks(
        round1_marks,
        round2_marks,
        round3_marks,
        technical_round_marks
    )

    result = cal_result(round1_marks,round2_marks,round3_marks,technical_round_marks,total_marks)

    cursor.execute("""
        INSERT INTO student (
            student_name,
            college_name,
            round1_marks,
            round2_marks,
            round3_marks,
            technical_round_marks,
            total_marks,
            result,
            rank
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        college_name,
        round1_marks,
        round2_marks,
        round3_marks,
        technical_round_marks,
        total_marks,
        result,
        None
    ))

    connection.commit()

    update_rank()

    print("\nRecord Saved Successfully")
    print("Total Marks:", total_marks)
    print("Result:", result)


def display_student():
    print("\nCandidate Records\n")

    cursor.execute("""
        SELECT
            rank,
            student_name,
            college_name,
            round1_marks,
            round2_marks,
            round3_marks,
            technical_round_marks,
            total_marks,
            result
        FROM student
        ORDER BY rank ASC
    """)

    records = cursor.fetchall()

    if len(records) == 0:
        print("No records found.")
        return

    print(
        f"{'Rank':<8}"
        f"{'Student Name':<20}"
        f"{'College Name':<25}"
        f"{'R1':<8}"
        f"{'R2':<8}"
        f"{'R3':<8}"
        f"{'Technical':<12}"
        f"{'Total':<10}"
        f"{'Result':<12}"
    )

    for record in records:
        print(
            f"{record[0]:<8}"
            f"{record[1]:<20}"
            f"{record[2]:<25}"
            f"{record[3]:<8.2f}"
            f"{record[4]:<8.2f}"
            f"{record[5]:<8.2f}"
            f"{record[6]:<12.2f}"
            f"{record[7]:<10.2f}"
            f"{record[8]:<12}"
        )


def main():
    while True:
        print("\nCandidate Data")
        print("1. Add Candidate")
        print("2. Display All Candidates")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            display_student()

        elif choice == "3":
            print("Program Ended")
            break

        else:
            print("Invalid Choice")


main()
connection.close()