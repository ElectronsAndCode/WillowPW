Password Generator/Decoder for NES Willow game

This is not exactly a professional quality generator; it does the bare minimum.  To generate a password, assemble the list of bitmaps representing the feats completed, weapons, shields, magics, and items that you want.  You can reference the arrays of strings in each category.  They are ordered from lowest significant bit to most significant bit.  So for instance, if you want to have the wooden shield and the gold shield, the shield value would be 00000101b.

Level is allowed to be any value between 0 and 15.  The game will reject anything higher.

Using these values, call create_password(0, feats, swords, shields, magics, items, 0, level, 0)
