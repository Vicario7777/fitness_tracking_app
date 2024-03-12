import sqlite3
import os

# Create or update the database
def connect_to_database():
    try:
        # Check if the database file exists
        if os.path.exists('fitness_tracker.db'):
            return sqlite3.connect('fitness_tracker.db')
        else:
            db = sqlite3.connect('fitness_tracker.db')
            # Creates tables if the database is newly created
            create_tables(db)
            return db
        
    except Exception as e:
        print("Database connection failed:", e)
        return None

# Function to create tables if they don't exist
def create_tables(db):
    try:
        cursor = db.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS exercise_categories (
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE
                        )''')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        name TEXT,
                        muscle_group TEXT,
                        reps INTEGER,
                        sets INTEGER,
                        FOREIGN KEY (category) REFERENCES exercise_categories (name)
                       )
                ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS workouts (
                       id INTEGER PRIMARY KEY,
                       exercise_id INTEGER,
                       reps INTEGER,
                       sets INTEGER,
                       date DATE,
                       FOREIGN KEY (exercise_id) REFERENCES exercises (id)
                       )
                    ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY,
                category TEXT,
                goal_reps INTEGER,
                goal_sets INTEGER,
                FOREIGN KEY (category) REFERENCES exercise_categories (name)
                )
            ''')

        db.commit()

    except Exception as e:
        print("An error occurred while creating or updating the database:", e)
        return None
    
# Function to add predefined exercise categories
def add_prefined_categories(db):
    try:
        predefined_categories = [
            "Cardio",
            "Strength Training",
            "Flexibility",
            "Balance",
            "Core",
            "HIIT"
        ]

        cursor = db.cursor()
        cursor.execute("SELECT name FROM exercise_categories")
        existing_categories = cursor.fetchall()
        existing_categories = [row[0] for row in existing_categories]

        for category in predefined_categories:
            if category not in existing_categories:
                cursor.execute("INSERT INTO exercise_categories (name) VALUES (?)", (category,))
                # Update existing categories list
                existing_categories.append(category)
        db.commit()
    
    except Exception as e:
        print("An error occurred:", e)

# Function to add predefined workouts
def add_predefined_workouts(db):
    try:
        predefined_workouts = [
            # Cardio
            ("Cardio", "Running", "Legs", 30, 1),
            ("Cardio", "Cycling", "Legs", 45, 1),
            ("Cardio", "Jump Rope", "Full Body", 100, 3),
            # Strength Training
            ("Strength Training", "Push-ups", "Chest, Shoulders, Triceps", 15, 3),
            ("Strength Training", "Pull-ups", "Back, Biceps", 10, 3),
            ("Strength Training", "Squats", "Legs", 20, 3),
            ("Strength Training", "Deadlifts", "Full Body", 20, 3),
            # Flexibility
            ("Flexibility", "Stretching", "Full Body", 0, 0), # Reps and sets may vary for stretching
            # Balance
            ("Balance", "Single-leg Balance", "Legs, Core", 0, 0), # Reps and sets may vary for balancing
            # Core
            ("Core", "Plank", "Core", 60, 1),
            ("Core", "Crunches", "Core", 20, 3)
        ]

        cursor = db.cursor()
        for workout in predefined_workouts:
            category, name = workout[0], workout[1]
            cursor.execute("SELECT COUNT(*) FROM exercises WHERE category=? AND name=?", (category, name))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO exercises (category, name, muscle_group, reps, sets) VALUES (?, ?, ?, ?, ?)", workout)
        
        db.commit()
    except Exception as e:
        print("An error occurred:", e)

# Function to add new workout categories to the database
def add_exercise_category(db):
    try:
        category = input("Enter exercise category: ")
        cursor = db.cursor()
        cursor.execute("INSERT INTO exercises (category) VALUES (?)", (category,))
        db.commit()
        print("Exercise category added successfully.")

        # After adding the category, prompt for further actions
        while True:
            print("\nAdditional actions:")
            print("1. Update exercise category")
            print("2. Delete exercise category")
            print("3. Back to main menu")
            action_choice = input("Enter your choice: ")

            if action_choice == '1':
                update_exercise_category(db, category)
            elif action_choice == '2':
                delete_exercise_category(db, category)
            elif action_choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                
    except Exception as e:
        print("An error occurred:", e)

# Function to update a workout category
def update_exercise_category(db, category):
    try:
        category = input("Enter old workout category: ")
        new_category = input("Enter new workout category: ")
        cursor = db.cursor()
        cursor.execute("UPDATE exercises SET category=? WHERE category=?", (new_category, category))
        db.commit()
        print("Workout category updated successfully.")

    except Exception as e:
        print("An error occurred:", e)

# Function to delete exercises by category
def delete_exercise_category(db, category):
    try:
        cursor = db.cursor
        cursor.execute("DELETE FROM exercises WHERE category=?", (category,))
        db.commit()
        print("Exercise category '{}' deleted successfully.".format(category))
    
    except Exception as e:
        print("An error occurred", e)

# Function to add new exercises
def add_new_exercise(db):
    try:
            category = input("Enter workout category: ")
            name = input("Enter exercise name: ")
            muscle_group = input("Enter muscle group: ")
            reps = int(input("Enter number of reps: "))
            sets = int(input("Enter number of sets: "))

            cursor = db.cursor()
            cursor.execute("INSERT INTO exercises (category, name, muscle_group, reps, sets) VALUES (?, ?, ?, ?, ?)",
                        (category, name, muscle_group, reps, sets))
            db.commit()
            print("Exercise added successfully.")

    except Exception as e:
        print("An error occurred:", e)

# Function to view exercises by category
def view_exercises_by_category(db):
    try:
        category = input("Enter workout category to view exercises: ")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM exercises WHERE category=?", (category,))
        exercises = cursor.fetchall()
        if exercises:
            for exercise in exercises:
                print(exercise)

            add_new_exercise(db)
        else:
            print("\nNo exercises found in this category.")
            main_menu(db)

    except Exception as e:
        print("An error occurred:", e)

# Function to delete an exercise by category
def delete_exercise_by_category(db):
    try:
        category_name = input("Enter workout category to delete exercises from: ")
        cursor = db.cursor()
        cursor.execute("SELECT id FROM exercises WHERE name=?", (category_name,))
        category_id = cursor.fetchone()

        if category_id:
            cursor.execute("DELETE FROM exercises WHERE category_id=?", (category_id[0],))
            db.commit()
            print("Exercises deleted successfully from category '{}'.".format(category_name))
        else:
            print("\mCategory '{}' does not exist.".format(category_name))
    except Exception as e:
        print("An error occurred:", e)

# Function to create workout routine
def create_workout_routine(db):
    try:
        category = input("Enter workout category to create routine: ")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM exercises WHERE category=?", (category,))
        exercises = cursor.fetchall()

        if exercises:
            print("Available exercises in category '{}':".format(category))
            for i, exercise in enumerate(exercises, 1):
                print("{}. {}".format(i, exercise[0]))
            selected_exercises = input("Enter the numbers of exercises to add to the routine (comma-separated): ")
            selected_exercises_numbers = [int(x.strip()) for x in selected_exercises.split(",")]
            routine = [exercises[num - 1][0] for num in selected_exercises_numbers if 0 < num <= len(exercises)]
            print("Workout routine for Category '{}':".format(category))
            for exercise in routine:
                print("- " + exercise)
        else:
            print("No exercises found in this category.")
    except Exception as e:
        print("An error occurred:", e)

# Function to view workout routine
def view_workout_routine(db):
    try:
        category = input("Enter workout category to view routine: ")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM exercises WHERE category=?", (category,))
        exercises = cursor.fetchall()
        if exercises:
            print("Workout Routine for Category '{}':".format(category))
            for exercise in exercises:
                print("- " + exercise[0])
        else:
            print("No exercises found in this category.")
    except Exception as e:
        print("An error occurred:", e)

# Function to calculate fitness progress
def view_exercise_progress(db):
    try:
        category = input("Enter workout category to view progress: ")
        exercise_name = input("Enter exercise name: ")

        # Retrieve completed reps and sets for the exercise
        cursor = db.cursor()
        cursor.execute("SELECT reps, sets FROM exercises WHERE category=? AND name=?", (category, exercise_name))
        completed_reps, completed_sets = cursor.fetchall()
            
        # Retrieve goal reps and sets for the exercise
        cursor.execute("SELECT goal_reps, goal_sets FROM goals WHERE category=?", (category,))
        goal_reps, goal_sets = cursor.fetchone()

        if completed_reps is None or completed_sets is None:
            print("No goals found for this exercise.")
            return

        # Calculate progress percentage
        progress_reps = (completed_reps / goal_reps) * 100 if goal_reps != 0 else 0
        progress_sets = (completed_sets / goal_sets) * 100 if goal_sets != 0 else 0

        print("Exercise progress for category '{}' based on reps: {:.2f}%".format(category, progress_reps))
        print("Exercise progress for category '{}' based on sets: {:.2f}%",format(category, progress_sets))
        
    except Exception as e:
        print("An error occurred:", e)

# Function to set fitness goals
def set_fitness_goals(db):
    try:
        category = input("Enter goal category: ")
        goal_reps = int(input("Enter goal reps: "))
        goal_sets = int(input("Enter goal sets: "))
        cursor = db.cursor()
        cursor.execute("INSERT INTO goals (category, goal_reps, goal_sets) VALUES (?, ?, ?)", (category, goal_reps, goal_sets))
        db.commit()
        print("Fitness goals set successfully.")
    except Exception as e:
        print("An error occurred:", e)

# Function to view progress towards fitness goals
def view_progress_towards_fitness_goals(db):
    try:
        category = input("Enter goal category to view progress: ")
        cursor = db.cursor()

        # Retrieve workout data
        cursor = db.cursor
        cursor.execute("SELECT SUM(reps), SUM(sets) FROM exercises WHERE category=?", (category,))
        total_completed_reps, total_completed_sets = cursor.fetchone()
            
        # Retrieve goal data
        cursor.execute("SELECT SUM(goal_reps), SUM(goal_sets) FROM goals WHERE category=?", (category,))
        total_goal_reps, total_goal_sets = cursor.fetchone()

        if total_goal_reps is None or total_goal_sets is None:
            print("No goals found for this category.")
            return

        # Calculate progress percentage
        progress_reps = (total_completed_reps / total_goal_reps) * 100 if total_goal_reps != 0 else 0
        progress_sets = (total_completed_sets / total_goal_sets) * 100 if total_goal_sets != 0 else 0

        print("Fitness progress for category '{}' based on reps: {:.2f}%".format(category, progress_reps))
        print("Fitness progress for category '{}' based on sets: {:.2f}%",format(category, progress_sets))
        
    except Exception as e:
        print("An error occurred:", e)

# Main menu function
def main_menu(db):
    while True:
        print("\nFitness Tracker Menu:")
        print("1. Add exercise category")
        print("2. View exercise by category")
        print("3. Delete exercise by category")
        print("4. Add new exercise")
        print("5. Create Workout Routine")
        print("6. View Workout Routine")
        print("7. View Exercise Progress")
        print("8. Set Fitness Goals")
        print("9. View Progress towards Fitness Goals")
        print("10. Quit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_exercise_category(db)
        elif choice == '2':
            view_exercises_by_category(db)
        elif choice == '3':
            delete_exercise_by_category(db)
        elif choice == '4':
            add_new_exercise(db)
        elif choice == '5':
            create_workout_routine(db)
        elif choice == '6':
            view_workout_routine(db)
        elif choice == '7':
            view_exercise_progress(db)
        elif choice == '8':
            set_fitness_goals(db)
        elif choice == '9':
            view_progress_towards_fitness_goals(db)
        elif choice == '10':
            db.close()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    db = connect_to_database()
    if db:
        create_tables(db)
        add_predefined_workouts(db)
        add_prefined_categories(db)
        main_menu(db)
    else:
        print("Database connection failed.")