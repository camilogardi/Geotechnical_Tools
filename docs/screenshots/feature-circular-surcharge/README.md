# Feature: Circular Surcharge - Screenshots

This directory contains screenshots demonstrating the implementation of the circular surcharge feature.

## Screenshots

### 01_title_icon.png
**Caption**: Application showing the new title "Calculo de Esfuerzos" in the browser tab and sidebar. The page icon has been updated to use IMG_2224.jpeg.

**Relevance**: Confirms the title and icon requirements have been implemented as specified.

### 02_tabs_overview.png  
**Caption**: Complete navigation showing all five tabs: "Esfuerzo Vertical Rectangular", "Esfuerzo Vertical Continua", "Esfuerzo Vertical Circular" (selected), "Esfuerzo Vertical Anular", and "Esfuerzo Vertical Terraplén".

**Relevance**: Demonstrates that the circular surcharge tab has been added while maintaining all existing tabs.

### 03_circular_inputs.png
**Caption**: The "Esfuerzo Vertical Circular" tab showing input parameters: q (sobrecarga), radio, calculation point coordinates (x, y), and depth range (z_min, z_max, number of points).

**Relevance**: Shows the input interface structure matches the requirement to follow the same pattern as the rectangular tab.

### 04_circular_results_plot.png
**Caption**: Plot showing vertical stress (σz) versus depth (z) for a circular load at r=0.00m from center. The graph displays the characteristic stress distribution curve.

**Relevance**: Demonstrates the calculation results visualization with the sigma_z vs z plot as required.

### 05_circular_results_table.png
**Caption**: Results table displaying depth and stress values for 50 calculation points, with download CSV button available.

**Relevance**: Shows the tabular results output matching the requirement for a data table display.

### 06_streamlit_console.txt
**Caption**: Terminal output showing `streamlit run app.py` executing without errors. Health check returns OK, and all features are verified.

**Relevance**: Confirms the application starts successfully with no console errors.

### 07_pytest_ok.txt
**Caption**: Pytest output showing all 25 tests passing, including 3 new tests for circular surcharge calculations (on-axis case, zero load, and input validation).

**Relevance**: Demonstrates that basic tests have been added for the circular surcharge function and all existing tests continue to pass.

## Summary

All required screenshots have been captured demonstrating:
- ✓ Title changed to "Calculo de Esfuerzos"
- ✓ Icon updated to IMG_2224.jpeg
- ✓ New "Esfuerzo Vertical Circular" tab added
- ✓ Input interface implemented
- ✓ Calculation and plotting working
- ✓ Results table displayed
- ✓ No console errors
- ✓ Tests passing
