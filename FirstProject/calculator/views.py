from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def calculator_view(request):
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.POST.get("num1"))
            num2 = float(request.POST.get("num2"))
            operation = request.POST.get("operation")

            if operation == "addition":
                result = num1 + num2
            elif operation == "subtraction":
                result = num1 - num2
            elif operation == "multiplication":
                result = num1 * num2
            elif operation == "division":
                if num2 != 0:
                    result = num1 / num2
                else:
                    result = "Error: Division by zero"
        except ValueError:
            result = "Error: Invalid input"

    return render(request, "calculator/calculator.html", {"result": result})
