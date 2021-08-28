from logging import StringTemplateStyle
import streamlit as st
import pandas as pd
import extractor
import display
import plots
import stmoduls

def main():
    # Set the app
    file, clinic_file, all_trends, trend, color, color_plico = stmoduls.app_settings()
    if file is not None:
        # Read the input xlsx file
        header, measurements, plicometry = extractor.extract(file)
        # Set the header information
        stmoduls.client_details((header, measurements), clinic_file)
        
        if all_trends:
            # Weight plots
            stmoduls.weight(measurements, color)
            # Shoulders plots
            stmoduls.shoulders(measurements, color)
            # Chest plots
            stmoduls.chest(measurements, color)
            # Arm plots
            stmoduls.arm(measurements, color)
            # Waist plots
            stmoduls.waist(measurements, color)
            # Legs plots
            stmoduls.legs(measurements, color)
            # Calf plots
            stmoduls.calf(measurements, color)
            # Buttock plots
            stmoduls.buttock(measurements, color)
            # Plicometry plots
            stmoduls.plicometry(header, plicometry, measurements, color_plico)

        else:
            if trend == 'Weight':
                # Weight plots
                stmoduls.weight(measurements, color)
            elif trend == 'Shoulders':
                # Shoulders plots
                stmoduls.shoulders(measurements, color)
            elif trend == 'Chest':
                # Chest plots
                stmoduls.chest(measurements, color)
            elif trend == 'Arms':
                # Arm plots
                stmoduls.arm(measurements, color)
            elif trend == 'Waist':
                # Waist plots
                stmoduls.waist(measurements, color)
            elif trend == 'Legs':
                # Legs plots
                stmoduls.legs(measurements, color)
            elif trend == 'Calfs':
                # Calf plots
                stmoduls.calf(measurements, color)
            elif trend == 'Buttock':
                # Buttock plots
                stmoduls.buttock(measurements, color)
            else:
                # Plicometry plots
                stmoduls.plicometry(header, plicometry, color_plico)
            
            

if __name__ == '__main__':
    main()