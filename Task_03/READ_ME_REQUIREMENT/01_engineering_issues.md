# &#x20;\*\*things That Was Broken in system\*\*

# 

# \*\*1. The checker thing only worked half the time\*\*

# In `navnet-core/src/compat.rs` — the code that checks if system works together was only blocking bad singals when set to V2. If you picked V1 it just let everything through. Like a door that only locks on one side.

# 

# \*\*2. whitespaces issues\*\*

# In `navnet-core/src/registry.rs` — it checked if the name was empty, but `"   "` (just spaces) isn't empty so the computer went "yeah thats a good name" even though its literally blank. Not cool.

# 

# \*\*3. Nothing got saved\*\*

# In `navnet-core/src/registry.rs` — the program could remember stuff while it was running, but once you closed it, poof, everything gone. No save button basically.

# 

# \*\*4. The main program was basically fake\*\*

# In `east-blue/src/main.rs` — it was supposed to do a whole bunch of steps (move stuff, check it, register it, save it) but instead it just put in one fake thing and stopped.

# \*\*5. The program got lost if you ran it from the wrong place\*\*

# In `archives/reverse-mountain` — if you ran it from the main folder it broke because it couldnt find its settings file. But if you went into the small folder first and ran it there, it worked. 

# 

# \*\*6. A missing empty folder broke the tests\*\*

# In `archives/reverse-mountain/config/assets/` — there was supposed to be a folder but it was empty, and the thing that saves code doesnt keep empty folders. So when you downloaded the code fresh, the folder wasnt there and tests just failed. The code was fine, the folder just ghosted everyone.

# 

# \*\*7. Leftover junk code in Alabasta\*\*

# In `alabasta/src/coordinator.rs` and the test file — there was some code that wasnt doing anything, just sitting there. 

