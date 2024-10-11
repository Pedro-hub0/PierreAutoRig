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
- Create Locs : Create 2 Locators.
  ->Place the root one at the root of your character, a bit upper than the hips
  ->Place the shoulder one at the shoulder right ahead the 1st one
- Create Ik/Fk Spine thanks to the 2 locs. You can shose the number of fk Ctrl and ik joints.

Arm/Leg :
- Create 3 joints where the Arm/Elbow/Wrist need to be. Be carreful to not have 2 joints with the same name.
  --> Name the parent joint : Arm_L or  Arm_R or Leg_L or Leg_R
- Select your join which was Rename
- Freeze and orient to clean and orient everything
- Ik_Fk_Arm/Leg --> Create automatically everything to have an ik/fk switch
- Permit to create the other sidr Arm or Leg

Clavicle :
- Select the Ik/Fk Controller of the side where you want to create the clavicle
- Create Loc --> Once created, place it where you want the clavicle in the location of the clavicle
- Create Clavicles --> Create the clavicle and the Ctrl
- Mirror --> With create mirror the joint and create the clavicle. Without 'create',it  just mirror the loc

Foot: (the Leg need to be created)
- Select the Ik/Fk Controller of the side where you want to create the foot
- Create Locs : Place the locators at the good place
- Organise Locs: it will organise your hierarchy
- Nodale: it's creating all the nodale connexion for the Foot Roll, Bank etc.
- Mirror = mirror les locs et dossier, Mirror + Organise + Nodale

Hand:(the Arm need to be created)
- Select the Ik/Fk Controller of the side where you want to create the foot
- Create Locators: Create some locators, put it at the right place. Be carreful to have all the locs of a finger in the same axe.
- Create Hand: Create and orient the joint. You can check the orient if that looks weird
- Create Controllers: Create the Ctrl

Hips:(The 2 Legs need to be created plus the Spine)
- Create Hips: Create the joint and link them
- Create CTRL Hips: Create the Ctrls and the links/parents

Attach Ribbon: 
 - You need to have a Ribbon already created with a good nomenclature: Ribbon_MatX.ma /Ribbon_01 //Ctrl_Global_Ribbon_01// Bind_Ribbon_A01 //Bind_Ribbon_B01 //CTRL_Ribbon_Mid_01
 - You need tu load the plugin quatNodes.mll
- Check the elements where you want a Ribbon.
- Attach : It will import, rename and attach the Ribbon where you check it

Lock Attribute:
- Check the one that you want to lock and the one that you want to unlock. If Translate or rotate is uncheck, it will do nothing on the X/Y/Z.
If Translate or rotate is check, it will considere everything check is lock, everything uncheck is unlock.

Replace Ctrl:
- If you have a Ctrl Shape that you prefer. Take the Ctrl that you like and the other that you want to replace.
- Click on Replace Ctrl and it will replace the shape

Match Ik/Fk:
- For animator. Permit to do a match Ik Fk with that rig

