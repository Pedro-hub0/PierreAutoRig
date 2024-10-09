# PierreAutoRig
 MayaAutorig
Auto rig Maya par Pierre Lippens

How to install :
- Put the Folder PierreAutoRig in ...\Documents\maya\2024\prefs\scripts
- copy the line in install.py in maya (don't forget to put Python)

  Let me know if there is any issue

*Ctrls = Controllers

How to use it :
Spine:
1- Create Locs : Create 2 Locators.
  ->Place the root one at the root of your character, a bit upper than the hips
  ->Place the shoulder one at the shoulder right ahead the 1st one
2- Create Ik/Fk Spine thanks to the 2 locs. You can shose the number of fk Ctrl and ik joints.

Arm/Leg :
- Create 3 joints where the Arm/Elbow/Wrist need to be. Be carreful to not have 2 joints with the same name.
  --> Name the parent joint : Arm_L or  Arm_R or Leg_L or Leg_R
0- Select your join which was Rename
1- Freeze and orient to clean and orient everything
2- Ik_Fk_Arm/Leg --> Create automatically everything to have an ik/fk switch
3- Permit to create the other sidr Arm or Leg

Clavicle :
0- Select the Ik/Fk Controller of the side where you want to create the clavicle
1- Create Loc --> Once created, place it where you want the clavicle in the location of the clavicle
2- Create Clavicles --> Create the clavicle and the Ctrl
3- Mirror --> With create mirror the joint and create the clavicle. Without 'create',it  just mirror the loc

Foot: (the Leg need to be created)
0- Select the Ik/Fk Controller of the side where you want to create the foot
1- Create Locs : Place the locators at the good place
2- Organise Locs: it will organise your hierarchy
3- Nodale: it's creating all the nodale connexion for the Foot Roll, Bank etc.
4- Mirror = mirror les locs et dossier, Mirror + Organise + Nodale

Hand:(the Arm need to be created)
0- Select the Ik/Fk Controller of the side where you want to create the foot
1- Create Locators: Create some locators, put it at the right place. Be carreful to have all the locs of a finger in the same axe.
2- Create Hand: Create and orient the joint. You can check the orient if that looks weird
3- Create Controllers: Create the Ctrl

Hips:(The 2 Legs need to be created plus the Spine)
1- Create Hips: Create the joint and link them
2- Create CTRL Hips: Create the Ctrls and the links/parents

Attach Ribbon: 
0- Check the elements where you want a Ribbon.
1- Attach : It will import, rename and attach the Ribbon where you check it

Lock Attribute:
0- Check the one that you want to lock and the one that you want to unlock. If Translate or rotate is uncheck, it will do nothing on the X/Y/Z.
If Translate or rotate is check, it will considere everything check is lock, everything uncheck is unlock.

Replace Ctrl:
If you have a Ctrl Shape that you prefer. Take the Ctrl that you like and the other that you want to replace.
Click on Replace Ctrl and it will replace the shape

Match Ik/Fk:
For animator. Permit to do a match Ik Fk with that rig

