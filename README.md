# Fit_box
This is a simple rasterization tool I made that converts vector-based SVG files into pixel coordinates and displays it with PyQt.

See below for sample rasterization. The SVG file is shown on the left(filled with green in the Inkscape application) and the rasterized product is shown on the right (red outline for the original vector data, blue for the rasterized pixel coordinates, and the green outline shows the outline of a container to be used later as part of the next phase.

<img src="https://github.com/StormPizza/Fit_box/blob/master/images/FitBoxRasterize.png" width="900" title="Door-Unlocker-Complete-Cycle" alt="Raspberry Pi Door Unlocker with RFID Reader" >

The end goal is for this script to take SVG images of polygons and an SVG image of a box, and possibly, competently fit the polygons into the 2D-box in a space-saving manner, as a demonstration of 2D Bin Packing.
