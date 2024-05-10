def get_car_order(
    model,
    spec,
    colour,
    interior,
    wheels,
    tow_hitch=False,
    enhanced=False,
    self_driving=False,
):

    order = {
        "model": model,
        "tow_hitch": tow_hitch,
        "enhanced": enhanced,
        "self_driving": self_driving,
    }

    if spec == "rear wheel drive":
        order["spec"] = "Rear-Wheel Drive"
    elif spec == "long range":
        order["spec"] = "Long Range All-Wheel Drive"
    elif spec == "performance":
        order["spec"] = "Performance All-Wheel Drive"

    if wheels == '20" Induction alloy wheels':
        order["wheels"] = "’’ Induction Wheels"
    elif wheels == '19" Gemini alloy wheels':
        order["wheels"] = "’’ Gemini Wheels"
    elif wheels == '18" Photon alloy wheels':
        order["wheels"] = "’’ Photon Wheels"
    elif wheels == '19" Nova alloy wheels':
        order["wheels"] = "’’ Nova Wheels"

    if interior == "black":
        order["interior"] = "Black"
    elif interior == "black and white":
        order["interior"] = "Black and White"
    elif interior == "All Black":
        order["interior"] = "All Black"

    if colour == "Pearl White Multi-Coat":
        order["colour"] = "Pearl White Multi-Coat"
    elif colour == "Deep Blue Metallic":
        order["colour"] = "Deep Blue Metallic"
    elif colour == "Solid Black":
        order["colour"] = "Solid Black"
    elif colour == "Ultra Red":
        order["colour"] = "Ultra Red"
    elif colour == "Stealth Grey":
        order["colour"] = "Stealth Grey"
    elif colour == "Quicksilver":
        order["colour"] = "Quicksilver"

    return order
