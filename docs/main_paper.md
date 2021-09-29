## Introduction
* Global trash issues
* How does urban waste affect this?
* How are streets cleaned now?
    * Volunteer
    * Government
* Issues this can address:
    * Garbage next to a recepticle
    * Large dumpsites
* Describe the advantages of Google Street View
    * Is it a proxy for future self driving car datasets?

* Explain the structure of the paper?

## Related works
* GIS inventory management [2] [3]
    * Triangulation [3]
    * Manually labelling GSV using Amazon Turk [7]
* Street cleaning robots [4] [6]
    * Images are generally close up
* Smart city trash monitoring [5]
    * TrashNet based on YOLOv3 for live video trash monitoring
    * Dataset:
        * Trained on Google Images Download
        * Labelled using LabImg
        * > The dataset is composed of 2714 images containing objects of the four different classes (Garbage Bag, Garbage Dumpster, Garbage Bin and Blob) and 1260 images of negative examples representing landscapes without objects of interest, for a total of 5535 labels
        * Runs at 20 FPS
* Categorizing trash and recycling [1]
    * Works well on trash with a white background and with the camera up close


## Framework and model
* Dataset
    * GSV
    * TACO
* Choosing an Object Recognition model

## Evaluate accuracy

## Discussion and future work


[1] R. Sultana, R. D. Adams, Y. Yan, P. M. Yanik, and M. L. Tanaka, “Trash and Recycled Material Identification using Convolutional Neural Networks (CNN),” in 2020 SoutheastCon, Raleigh, NC, USA, Mar. 2020, pp. 1–8. doi: 10.1109/SoutheastCon44009.2020.9249739.

[2] R. Hebbalaguppe, G. Garg, E. Hassan, H. Ghosh, and A. Verma, “Telecom Inventory Management via Object Recognition and Localisation on Google Street View Images,” in 2017 IEEE Winter Conference on Applications of Computer Vision (WACV), Santa Rosa, CA, USA, Mar. 2017, pp. 725–733. doi: 10.1109/WACV.2017.86.

[3] A. Campbell, A. Both, and Q. (Chayn) Sun, “Detecting and mapping traffic signs from Google Street View images using deep learning and GIS,” Computers, Environment and Urban Systems, vol. 77, p. 101350, Sep. 2019, doi: 10.1016/j.compenvurbsys.2019.101350.


[4] L. Donati, T. Fontanini, F. Tagliaferri, and A. Prati, “An Energy Saving Road Sweeper Using Deep Vision for Garbage Detection,” Applied Sciences, vol. 10, no. 22, p. 8146, Nov. 2020, doi: 10.3390/app10228146.

[5] B. D. Carolis, F. Ladogana, and N. Macchiarulo, “YOLO TrashNet: Garbage Detection in Video Streams,” in 2020 IEEE Conference on Evolving and Adaptive Intelligent Systems (EAIS), Bari, Italy, May 2020, pp. 1–7. doi: 10.1109/EAIS48028.2020.9122693.

[6] J. Bai, S. Lian, Z. Liu, K. Wang, and D. Liu, “Deep Learning Based Robot for Automatically Picking Up Garbage on the Grass,” IEEE Trans. Consumer Electron., vol. 64, no. 3, pp. 382–389, Aug. 2018, doi: 10.1109/TCE.2018.2859629.

[7] K. Hara, V. Le, and J. Froehlich, “Combining crowdsourcing and google street view to identify street-level accessibility problems,” in Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, Paris France, Apr. 2013, pp. 631–640. doi: 10.1145/2470654.2470744.
