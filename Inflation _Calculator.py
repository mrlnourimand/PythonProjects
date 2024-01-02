"""
COMP.CS.100
Week 03, the 1st Python project. Inflation Calculator.

(You will implement a program which can be used
    to figure out the maximum inflation increase
     from the values the user entered.)

Creator: Maral Nourimand
Student id number: 151749113
"""
def main():
    # to initialize the flag key
    key = True
    # to initialize the counter variable
    month_number = 1
    while key:
        current_inflation_str = input(f"Enter inflation rate for month {month_number}: ")
        if current_inflation_str == "" and month_number <=2:
            print("Error: at least 2 monthly inflation rates must be entered.")
            # if the error occurs, it ends the loop
            key = False
        elif current_inflation_str == "" and month_number > 2:
            # if operator press Enter, it ends the loop
            break
        elif month_number == 1:
            previous_inflation = float(current_inflation_str)
        elif month_number == 2:
            maximum_irc = float(current_inflation_str) - previous_inflation
            previous_inflation = float(current_inflation_str)
        # all the other inputs after 2 would be processed here:
        else:
            current_inflation = float(current_inflation_str)
            inflation_rate_change = current_inflation - previous_inflation
            if inflation_rate_change > maximum_irc:
                maximum_irc = inflation_rate_change
            previous_inflation = current_inflation
        month_number += 1
    if key == True:
        print(f"Maximum inflation rate change was {maximum_irc:.1f} points.")

if __name__ == "__main__":
    main()
