# Note 
This integration has been made with the help of various community integration availabe, and this integration includes Adobe Animate, Adobe Illustrator, Adobe Premiere all these three softwares are integrated into Flow Production Tracking(Shotgrid) and tested with windows system only. 

# Step 1
Setup the Project through the SG desktop

# Step 2
Create a clone configuration to test the code on 

# Step 3
Use the clone configuration to make the changes mentioned below 

# Step 4
Add the engine to your project clone config from the files mentioned here

# Step 5
Add the tk-engines to the appstore or specify the path of the engine.

# Step 6 
Update the adobe framework with the mentioned updates
Changes
- In the tk-framework-adobe manifest.xml file in "install\app_store\tk-framework-adobe\v1.1.8\cep\CSXS" line no 15-20 are changed.
- Added a folder dhx in "install\app_store\tk-framework-adobe\v1.1.8\cep\js".
- The files in "install\app_store\tk-framework-adobe\v1.1.8\cep\js\shotgun" are changed, search for "//added this for integration support" to identify changes.

# Step 6 
Build the plugin zxp file using the dev folder of the adobe framework and sign the extension (refer readme file of tk-framework-adobe)

# Step 7 
Run the shotgun desktop and check if the engines works fine, test all the functions.

# Step 8
If the engine is working properly and after testing it, add the copy pipeline to the primary pipeline

# Note 
You can use this configuration as a base for other projects while setting up the projects 

# Reference - Documentations
- [Shotgrid Documentation](https://help.autodesk.com/view/SGDEV/ENU/)
- [Illustrator Documentation](https://readthedocs.org/projects/illustrator-scripting-guide/downloads/pdf/latest/)
- [Animate Documentation](https://help.adobe.com/archive/en_US/flash/cs5/flash_cs5_extending.pdf)
- [Animate Integration](https://github.com/dhxstudios/tk-animatecc)
- [premiere Documentation](https://readthedocs.org/projects/premiere-scripting-guide/downloads/pdf/latest/)
- [premiere Integration](https://github.com/Vintata/tk-premiere)


# Develop new Publish Hooks 
- [Publish Hooks](https://developers.shotgridsoftware.com/tk-multi-publish2/index.html)