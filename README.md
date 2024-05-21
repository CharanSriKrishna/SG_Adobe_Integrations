# Note 
This integration has been made with the help of various community integration availabe, and this integration includes Adobe Animate, Adobe Illustrator, Adobe Premiere all these three softwares are integrated into Flow Production Tracking(Shotgrid) and tested with windows system only. 

# Step 1
Setup the Project through the SG desktop

# Step 2
Create a copy pipeline to test the code on 
- Goto the Shotgun website.
- Goto the pipeline in the specific project 
- Create a clone configuration from the options present after right-clicking the primary pipeline configurations

# Step 3
Use the clone configuration to make the changes mentioned below 

# Step 4
Copy the details in the config folder to appropriate files. 
- Don't paste the file as it is just paste the code inside the files in appropriate locations 
- Only paste the files "tk-animate.yml", "tk-illustrator.yml", "tk-premiere.yml" which are present in config\env\includes\settings as it is 

# Step 5
Add the tk-engines to the appstore or specify the path of the engine.
- Add all the engine folders tk-animate, tk-illustrator, tk-premiere as it is in install\app_store 
- In the tk-framework-adobe manifest.xml file in install\app_store\tk-framework-adobe\v1.1.8\cep\CSXS only line no 15-20 should be copied and pasted in the original file location 
- In the tk-framework-adobe dhx folder in install\app_store\tk-framework-adobe\v1.1.8\cep\js should be completely copy pasted
- The files in the path install\app_store\tk-framework-adobe\v1.1.8\cep\js\shotgun should be changed by searching for the "//added this for integration support" everything between this should be copied and pasted in the originals (only this codes)

# Step 6 
Build the plugin zxp file using the dev folder of the adobe framework and sign the extension (refer readme file of tk-framework-adobe)

# Step 7 
if Step 6 doesn't work you can paste the com.sg.basic.adobe.zxp file in this folder to  install\app_store\tk-framework-adobe\v1.1.8 (this is not recommended) or if the error is due to cant copy then Delete test from shotgunutil 5.90 and resources from desktop server.

# Step 8 
Run the shotgun desktop and check if the engines works fine, test all the functions.

# Step 9
If the engine is working properly and after testing it, add the copy pipeline to the primary pipeline 
- navigate to the configuration folder and open command promp and enter cmd - "tank push_configuration" to push the changes in clone to primary pipeline 

# Note 
You can use this configuration as a base for other projects while setting up the projects 

# Reference - Documentations
- Shotgrid Documentation - https://help.autodesk.com/view/SGDEV/ENU/
- Illustrator Documentation - https://readthedocs.org/projects/illustrator-scripting-guide/downloads/pdf/latest/
- Animate Documentation - https://help.adobe.com/archive/en_US/flash/cs5/flash_cs5_extending.pdf
- premiere Documentation - https://readthedocs.org/projects/premiere-scripting-guide/downloads/pdf/latest/
- premiere Integration - https://github.com/Vintata/tk-premiere


# Develop new Publish Hooks 
- Refer - https://developers.shotgridsoftware.com/tk-multi-publish2/index.html