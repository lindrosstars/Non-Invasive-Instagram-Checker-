# Non-Invasive-Instagram-Checker-
this python script cross checks followers and following to give you a list of users who don't follow you back , users you don't follow back , and mutual followers without invading Instagram's terms of service.

Step by Step instructions -

Step 1: Log into your account , go to settings , Account Center.

Step 2: Go to Your information and permissions , Export your information

Step 3: Create export , Export to device 

Step 4: Customise Information , untick everything except followers and following inside Connections.

Step 5: Date range - All time , Format JSON

Step 6: Wait for a confirmation mail that indicates that the file is ready to download , Download and Extract the zip file

Step 7: After extracting the zip file , go to connections , followers_and_following .

Step 8: Make sure there are two files followers_1.json and following.json (You will be required to rename the files to followers_1.json and following.json if they are under a different name)

Step 9: Paste analyse_insta.py inside the folder and run it , it will create an instagram_analysis.txt file.
