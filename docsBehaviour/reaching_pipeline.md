---
title: Reaching Pipeline
toc: true
---
Here are described all steps needed for an effective and trouble free data acquisition for the reaching behaviour.

## 1. Data Acquisition
1. First the data needs to be acquired from the *mouse-bots*. These bots are in the animal-zone and can be handled by the *ReachingBot* software in the local machine there. Make sure the right handed mice are placed in the bots with the camera on the left side and the left-handed mice on the bots with the camera to your right.
2. Run sessions of about **20 min** for each mouse at each time point. If the context allows, you can parallelize multiple mice
3. Once it finishes, close the pop-up window and let it transfer all videos to the main computer. This is important, if you close the app before it will keep the videos inside the Bots and they will need to be extracted from there.
4. Now just upload the files to the server. The local machine has access to the server.

---

## 2. Labelling
1. Now that the we have some reaching videos we need to send them to DLC for labelling. For that create a folder with all the videos you want to label. Because *ReachingBot* stores also the date, you don't have to worry about merging different timepoints.
2. Copy that folder to an hard drive and connect it to the DALCO
3. Pick the DLC model and apply it to the videos. Because the videos are small and short this should run quite fast, no need for overnight runs.
4. Upload back to the server the DLC results that should have been stored in the drive.

---

## 3. Preprocessing
> Do all these steps both for the study group and for the control group

1. Before we get some cool plots we need to make sure we have all the **metadata** and that we remove all **noise**. This is where **EasyBehaviour** and **pyBehaviour** come to help.
2. First let's download from the server the data we need.
    1. The `.csv` files should go `data/reaching/study/raw` 
    2. The `.mp4`/`.avi`/`.mov` unlabeled at `data/reaching/study/videos`
    3. The `.mp4`/`.avi`/`.mov` labeled at `data/reaching/study/videos_labeled`
3. Now open another terminal window
4. Activate a conda environment with *napari* installed
5. Navigate back to **pyBehaviour**
6. Run `scripts/reaching/napari_manual.py`, this will prompt *napari*, there pick one or two frames that have the paw in the closest position, and add a dot where you think the wrist is. Add more frame/points if you don't feel confident that is the closest point.

> Napari will open in the best frame according to DLC (this hopefully will reduce time needed)

7. Close *napari* in the cross, this will save a csv file in `data/reaching/study/processed`.
8. The next video will open automatically.

---

## 4. Visualization
1. To visualize the plots just run `scripts/reaching/multi_group_distance.py`
