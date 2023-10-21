import tkinter.messagebox as tm  # Used to display messages to user

import sqlite3  # connecting sqlite3


class Database:

    def __init__(self):

        self.__conn = sqlite3.connect('GSU_Polling_System.db')
        self.__cur = self.__conn.cursor()
        self.__student_id = None

    @property
    def get_student_id(self):
        return self.__student_id

    def is_authorized(self, username, password):
        """ Authenticates login credentials for student"""

        user_found = self.__cur.execute(
            "SELECT username, password FROM Students WHERE username = :username AND password = :password",
            {'username': username, 'password': password}).fetchone()

        if user_found:

            # get the student id - the results are returned as a tuple
            get_student_id = self.__cur.execute("SELECT `student_id` FROM `Students` WHERE `username` = :username",
                                                {'username': username}).fetchone()[0]

            # get the student first-name and last-name to display welcome message
            get_student_name = list(self.__cur.execute(
                "SELECT firstname, lastname FROM Students WHERE `student_id` = :student_id",
                {'student_id': get_student_id}).fetchone())

            # get_student_name = list(get_student_name)
            tm.showinfo('Login success', f'Welcome {get_student_name[0]} {get_student_name[1]}')

            self.__student_id = get_student_id

        else:
            tm.showerror('Login Error', 'Incorrect username/password')

        return True if user_found is not None else False

    # ------------------------------------------ Candidates Section ------------------------------------------

    def get_candidate_by_position(self, position):
        # if the default option is selected
        if position == 'View All':
            return self.__cur.execute("""
                    SELECT
                    c.`firstname`,
                    c.`lastname`,
                    p.`position_name`
                FROM
                    Candidates c
                JOIN Positions p ON
                    c.`position_id` = p.`position_id`

                    """, ).fetchall()
        else:
            # Selecting Candidates and retrieving their positions from the position table by Position combo
            return self.__cur.execute("""
                        SELECT
                            c.firstname,
                            c.lastname,
                            p.position_name
                        FROM
                            Candidates c
                        JOIN Positions p ON
                            c.position_id = p.position_id
                        WHERE
                            p.position_id = :position
            """, {'position': self.get_candidate_position_id(position)}).fetchall()

    def get_candidate_positions(self):
        return self.__cur.execute("SELECT `position_name` FROM Positions").fetchall()

    def get_candidate_position_id(self, position):
        return self.__cur.execute("""
                SELECT position_id, position_name
                FROM Positions WHERE Positions.position_name = :position
                """, {'position': position}, ).fetchone()[0]

    def insert_candidate(self, firstname, lastname, position):

        with self.__conn:
            self.__cur.execute("""
            INSERT INTO Candidates (firstname, lastname, position_id)
            VALUES(:firstname, :lastname , :position)
            """, {'firstname': firstname, 'lastname': lastname, 'position': position})

    # ------------------------------------------ Votes Section ------------------------------------------

    def candidate_name(self, position):

        """ Selecting Candidates and retrieving their positions from the position table by Position combo"""
        return self.__cur.execute("""
                SELECT c.firstname
                FROM Candidates c
                JOIN Positions p ON c.position_id = p.position_id
                WHERE p.position_id = ?
                """, [self.get_candidate_position_id(position)], ).fetchall()

    def get_candidate_id(self, candidate_name):
        return self.__cur.execute("""
                    SELECT 
                        candidate_id, firstname
                    FROM Candidates
                    WHERE firstname = :firstname
                        """, {'firstname': candidate_name}).fetchone()[0]

    def check_duplicate_ranks(self, position):
        """This function checks if the user has already voted for a particular candidate position"""

        results_found = self.__cur.execute(
            "SELECT position_id, student_id FROM Votes WHERE position_id = :position_id AND student_id = student_id",
            {
                'position_id': self.get_candidate_position_id(position),
                'student_id': self.__student_id
            }
        ).fetchone()
        return True if results_found is not None else False

    def insert_vote(self, op1, op2, op3, op4, position):

        p1 = self.get_candidate_id(op1)
        p2 = self.get_candidate_id(op2)
        p3 = self.get_candidate_id(op3)
        p4 = self.get_candidate_id(op4)

        with self.__conn:
            self.__cur.execute("""
                        INSERT INTO `Votes`(`first_pref`, `second_pref`, `third_pref`, `fourth_pref`, `position_id`, `student_id`)
                        VALUES(:first, :second , :third, :fourth, :position,:student_id)""",
                               {'first': p1, 'second': p2, 'third': p3, 'fourth': p4,
                                'position': self.get_candidate_position_id(position),
                                'student_id': self.__student_id})
        return tm.showinfo("Voting details saved", "Your details has been saved")

    def __del__(self):
        self.__conn.close()
