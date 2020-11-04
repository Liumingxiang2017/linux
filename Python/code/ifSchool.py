# -----------PROBLEM : DETERMINE GRADE---------
# According to your age and birth month print out your grade

# Ask for the age
age, birthMonth = input('Enter age and birth month(num): ').split()
age = int(age)
birthMonth = int(birthMonth)

# Handle if kindergarden
if age < 7 or (age == 7 and birthMonth >= 9):
    print('Too young for school')
# if primary school
elif (age < 13) or (age == 13 and birthMonth >= 9):
    if birthMonth>=9:
        grade = age-7
    else:
        grade = age-6
    print("Go to {} grade of primary school".format(grade))

# Handle secondary school

elif (age < 16) or (age == 16 and birthMonth >= 9):
    if birthMonth >= 9:
        grade = age-13
    else:
        grade = age-12
    print("Go to {} grade of secondary school".format(grade))

# Handle high school

elif (age < 19) or (age == 19 and birthMonth >= 9):
    if birthMonth >= 9:
        grade = age-16
    else:
        grade = age-15
    print("Go to {} grade of high school".format(grade))
# University

else:
    print("Now maybe you go to university")
