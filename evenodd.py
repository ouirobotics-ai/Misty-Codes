from mistyPy.Robot import Robot

misty = Robot("10.1.14.125")

misty.speak("Hello, I am Misty. Today I will tell you whether a number is even or not?")

num = int(input("Enter a number: "))

if num % 2 == 0:
    misty.speak(f"{num} is an even number.")
else:
    misty.speak(f"{num} is an odd number.")