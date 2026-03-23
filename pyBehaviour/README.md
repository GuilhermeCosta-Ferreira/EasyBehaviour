<div align="center">
    <img src="https://shields.io/badge/python-3.13-green?logo=python&style=flat" alt="Python">
    <img src="https://shields.io/badge/Package_Manager-poetry-green?logo=poetry&style=flat" alt="Poetry">
</div>

# pyBehaviour
This python package is responsible to provide all tools in python for easy behaviour analysis of mice data

## Reaching Pipeline
Here the is described all steps needed for an effective and rouble free data acquisition for the reaching behaviour

### 1. Data Acquisition
1. First the data needs to be acquired from the *mouse-bots*. These bots are in the animal-zone and can be handled by the *ReachingBot* software in the local machine there. Make sure the right handed mice are placed in the bots with the camera on the left side and the left-handed mice on the bots with the camera to your right.
2. Run sessions of about **20 min** for each mouse at each time point. If the context allows, you can parallelize multiple mice
3. Once it finishes, close the pop-up window and let it transfer all videos to the main computer. This is important, if you close the app before it will keep the videos inside the Bots and they will need to be extracted from there.
4. Now just upload the files to the server. The local machine has access to the server.

### 2. Labelling
1. Now that the we have some reaching videos we need to send them to DLC for labelling. For that create a folder with all the videos you want to label. Because *ReachingBot* stores also the date, you don't have to worry about merging different timepoints.
2. Copy that folder to an hard drive and connect it to the DALCO
3. Pick the DLC model and apply it to the videos. Because the videos are small and short this should run quite fast, no need for overnight runs.
4. Upload back to the server the DLC results that should have been stored in the drive.

### 3. Preprocessing
1. Before we get some cool plots we need to make sure we have all the **metadata** and that we remove all **noise**. This is where **EasyBehaviour** and **pyBehaviour** come to help.

## DLC Support
in this sub-module you can find a toolbox to help you with DLC file management, from filde conversion and file cleaning for ligher analysis
