from django.shortcuts import render
import requests
import json
import os

def currency_data():
    """ All countries currency data"""
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies.json')
    with open(file_path, "r") as f:
        currency_data = json.loads(f.read())
    return currency_data

def index(request):
    if request.method == "POST":
        amount_str = request.POST.get('amount', '')
        currency_from = request.POST.get("currency_from")
        currency_to = request.POST.get("currency_to")

        # Check if the amount is a valid float
        try:
            amount = float(amount_str)
        except ValueError:
            error_message = "Please enter a valid amount."
            return render(request, "index.html", {"error_message": error_message, "currency_data": currency_data()})

        # Get currency exchange rates
        url = f"https://open.er-api.com/v6/latest/{currency_from}"
        response = requests.get(url)
        if response.status_code == 200:
            d = response.json()

            # Check if the conversion was successful
            if d["result"] == "success":
                # Get currency exchange of the target
                ex_target = d["rates"].get(currency_to)

                if ex_target is not None:
                    # Multiply by the amount
                    result = ex_target * amount

                    # Set 2 decimal places
                    result = "{:.2f}".format(result)

                    context = {
                        "result": result,
                        "currency_to": currency_to,
                        "currency_data": currency_data()
                    }

                    return render(request, "index.html", context)
                else:
                    error_message = f"Currency '{currency_to}' not found."
            else:
                error_message = "Failed to retrieve currency exchange rates."
        else:
            error_message = "Failed to retrieve data from API."

        return render(request, "index.html", {"error_message": error_message, "currency_data": currency_data()})

    return render(request, "index.html", {"currency_data": currency_data()})
