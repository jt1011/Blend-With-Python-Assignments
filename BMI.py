""" This Is A BMI Calculator, Used To Calculate body mass index and used to predict health risks """

print("This is a BMI Calculator")
Name  = str(input("Enter Your Name"))

mass = int(input("Enter Your Weight In KiloGrams"))

height = float(input("Enter Your Height In Metres"))

# Formula Starts Here

Bmi =  mass/(height*height)

print(f"Hey {Name}, Your height is {height} , Your Mass Is {mass}, Your Bmi is {Bmi}")