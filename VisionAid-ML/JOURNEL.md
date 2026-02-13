26th jan, 2026
objective : make a program which detects objects and movements in the centre

hurdles : the entropy was not exceeding the threshold even once
solution : normalized , add obstacle detection and did a trial and error method to manually input the most optimal threshold

status : centre detection works right now.



29th jan, 2026
objective : make a program which detects objects and movements in the centre,left and right

hurdles : the left and right entropy did not compare as it needed to
solution : had to properly use dictionary functions sinc ei put centre left and right in a dictionary rather than a list initally.

status : the left and right entropy  detection works 


Date: January 30, 2026
objective : implement calibraiton and beep delay

hurdle :  nothing today

status : able to implement calibraiton to find optimal threshold entropy and proper beep delay .



Date: January 31, 2026 
Objective: Optimize detection for small objects (pens) and fix spatial orientation/aspect ratio issues.

Hurdles: * Thin or low-contrast objects (like a pen) weren't moving the entropy needle enough to trigger the alarm.

created a blind spot at the bottom of the screen.

Solution:  Dilation: Created a 3x3 kernel to "thicken" the edges of thin objects, increasing their pixel footprint and entropy score.

Gaussian Blur: Added a small blur to filter out digital sensor noise that was causing "fake" entropy on a white screen.

 Forced the camera to 1280x720 using cap.set to fill the frame and eliminate black bars.


 5th feb,2026
 Hurdles:program couldn't distinguish between standing near a mess and walking into one.
 Low-light conditions caused "digital noise," leading to false-positive alarms in dark rooms


 solution :-
 Optical Flow: Implemented Farneback’s algorithm to calculate a motion_mag and an expansion_multiplier. This scales the danger score based on how fast the user is moving

 13th feb , 2026
goal today : make the program more accurate so that when the counter see's a clean floor before the counter passes 5 counter it dosent directly reset the ocunter to 0 but sloewl decreases counter so it has a shrot term memory and the bpm increases when the object comes near.

solution : 
used severity to slowely increase bpm by a multiplier and the counter decreases when it sees a clear floor  by this code line- counter = max(0, counter - 1) 

