def age_message(age):
    if age <= 6:
        print("幼児ですね！可愛い時期！")
    elif age <= 12:
        print("小学生ですね！")
    elif age <= 15:
        print("中学生ですね！")
    elif age <= 64:
        print("大人だね！")
    else :
        print("シニアだね！")

age_input = input("あなたの年齢を教えて！：")
age = int(age_input)
age_message(age)