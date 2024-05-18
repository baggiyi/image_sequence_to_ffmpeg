# image_sequence_to_ffmpeg

### !!!!!! ATTENTION !!!!!!!!!!!!!

MAKE SURE NOTHING IS IN YOUR BLENDER OUTPUT FOLDER. BECAUSE IT WILL DELETE THE RENDERED IMAGE FILES AFTERWARDS!!!

![final_py_script_image](https://github.com/baggiyi/image_sequence_to_ffmpeg/assets/49596447/687cd522-ec18-44ce-9449-c43e61b766b2)

### Quick Video Example: [youtube/link](https://youtu.be/D0fIHGQfnMM)
### Quick Setup:

what you need:

    -blender (i used 3.6)  
    -ff-mpeg binaries (i used 6.1.1)

installing the addon:

    -in blender go into the preferences under the Add-ons tab and install the .py file.  
    -make sure you enable the addon via the checkbox.  
    -put your path to your ffmpeg.exe in there.  
    -save your preferences and restart blender.  

using the addon:

    -before rendering make sure you saved your file once because the addon will look for the .blend name to name the video file.  
    -also please use PNG or TIFF as output file formate. (others can work but makes not really sense to me)  
    -happy rendering/converting!  

(by default it will convert it into prores 422 in mov cantainer. feel free to change it to whatever you like under the addon preferences.)  
[ff-mpeg doc/link](https://ffmpeg.org/ffmpeg-codecs.html) ff-mpeg codecs documentation  

### Addition:

-im not a programmer.  
-this isn't by any means a stable or finished addon/script. it was sort of a expedient for me and my current workflow.  
-i hope it works with new blender versions aswell / i did not tested it.  
-you can ofc modify it, or change it up if you want.  
-thought it can help others too, that's why im sharing it.  


-have a wonderful day.  




