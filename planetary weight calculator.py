# Define gravitational constants as a constant dictionary
GRAVITY_FACTORS: dict[str, float] = {
    "mercury": 0.376,
    "venus": 0.889,
    "mars": 0.378,
    "jupiter": 2.36,
    "saturn": 1.081,
    "uranus": 0.815,
    "neptune": 1.14
}

def get_planet_weight(earth_weight: float, planet: str) -> float:
    """
    Calculate and return the weight on a given planet based on Earth's weight.
    
    Parameters:
    earth_weight (float): The weight of the person on Earth in kg.
    planet (str): The name of the planet in any case format.
    
    Returns:
    float: The equivalent weight on the specified planet, rounded to two decimal places.
    """
    # Normalize input to lowercase to match dictionary keys
    planet_key = planet.lower()
    return round(earth_weight * GRAVITY_FACTORS[planet_key], 2)

# Program logic with error handling for weight and planet name
while True:
    try:
        # Get user input for weight and ensure it's a valid float
        earth_weight_input = input("Enter your weight on Earth (in kg): ")

        # Check if the input is a valid number
        if earth_weight_input.replace(".", "", 1).isdigit() and earth_weight_input.count(".") <= 1:
            earth_weight = float(earth_weight_input)  # Convert to float if it's valid
        else:
            raise ValueError("Weight must be a positive number greater than zero.")

        if earth_weight <= 0:
            raise ValueError("Weight must be greater than zero.")

        # Get user input for planet name
        planet = input("Enter the name of a planet in our solar system: ")

        # Get the weight on the selected planet
        planet_weight = get_planet_weight(earth_weight, planet)

        # Output the result
        print(f"Your weight on {planet.capitalize()} would be: {planet_weight} kg")
        input("Press Enter to exit the program.")
        break  # Exit loop after successful calculation
        
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except KeyError:
        print("Error: The planet name you entered is not recognized. Please enter a valid planet name.")
