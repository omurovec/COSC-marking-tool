# COSC-marking-tool

## What does this tool do?

I built this tool so that I could extract and move all my students Java project submissions into my IDE with just one command. This tool takes the submissions.zip file, extracts and sorts by lab section using the gradebook CSV file and extracts only the inner Java files and moves them to your IDE. The tool also changes the package name in each Java file to match the new directory or adds one if the file was missing it.

## Setup Instructions

1. Make sure you have python 3 installed on your machine
2. Download your class list using the export option under actions on the Grades page
3. Go to the assignments page and click on an assignment to download the submissions.zip
4. Create a project in Eclipse/Intellij and locate the path of the src folder
5. Set the paths from steps 2-4 in the python script
6. Run the script by navigating to this folder and running `py exports-to-eclipse.py`
7. You will find all of your submissions in your IDE separated by project name, lab section and student ID

### Notes

- Does not work with alternate archive formats (.rar/.7z/etc...)
