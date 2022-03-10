
def schedule_charging():

    current_dict = {"car1": 20, "car2": 8, "car3": 16, "car4": 5}
    sorted_current_dict = {k: v for k, v in sorted(current_dict.items(), key=lambda item:item[1])}
    return sorted_current_dict

