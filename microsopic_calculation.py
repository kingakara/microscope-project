def CalrealLifeSize(microscope_size, magnification):
    microscope_size_um = microscope_size * 1000

    # Formula to calculate the real-life size in micrometers
    real_life_size_um = microscope_size_um / magnification
    return real_life_size_um

def main():
    microscope_size = float(input("Enter the microscope size of the specimen (in micrometers): "))
    magnification = float(input("Enter the magnification factor: "))
    realLifeSize = CalrealLifeSize(microscope_size, magnification)

    print(f"The real-life size of the specimen is: {realLifeSize} micrometers.")

if __name__ == "__main__":
    main()
