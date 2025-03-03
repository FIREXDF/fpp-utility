# FightPlannerPackage Utility (FPP Utility)

FPP Utility is a program for making FightPlannerPackage file used for making mods pack or backup all mods to transfer into an another PC etc...

# How to Use
You only need fpputility.py that get his own GUI, for right now it's experimental and latest release build of FightPlanner will not supports FPP files. You need to wait the next update for getting a final good version.



First of all i recommend to put the extension to .pyw

![image](https://github.com/user-attachments/assets/55a63a3a-715b-499b-9ae2-8942c86cab58)

The GUI is really simple you got 3 button, one to create FPP one to extract FPP and one to list all files stored in the FPP.

![image](https://github.com/user-attachments/assets/0f8d6d02-15c4-4268-ac6e-127658b5ff23)

## Creating FPP

Create an empty folder and create a "manifest.json" that will got all GameBanana link that FightPlanner can install.

Your manifest.json will need to look like this
```
{
    "links": [
      "https://gamebanana.com/mods/download/579113#FileInfo_1393043",
      "https://gamebanana.com/mods/download/579050#FileInfo_1392854"
      // Add more links
        ]
  }
```

Now you can create a folder called `mods` and `plugin` pretty simple there in the plugin foldezr you put .nro files for skyline plugins, and mods folder put all the mods.

When you finish everything your folder should look like this

![image](https://github.com/user-attachments/assets/f15a8be8-4e0a-48d1-b724-e7df8a55c800)

Now open up fpputility.py (or .pyw) and click on `Create FightPlannerPackage (.fpp)` and select the folder you created

Now you just need to wait until it's finish (it's can take a while depending how many files you putted). When it's finish you should see you .fpp file !

## Extract your FPP file

This one is pretty easy on fpputility you just need to click on `Extract FightPlannerPackage (.fpp)` and you just select your .fpp file and it's will extract it for you.

## List the FPP file

You have multiple solutions for this, you can use 7-Zip and see what's is in the file or in fpputility.py (or pyw) you got `List files in a FightPlannerPackage` and you just select you FPP file and it's will list what's in the FPP file.

![image](https://github.com/user-attachments/assets/529dd33b-f2e3-4643-8ae1-82c33f3bcd22)

(It can be wrong it's only experimental)
