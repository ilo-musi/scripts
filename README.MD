This repository contains scripts that facilitate working with custom file formats of Ilo Musi.

* iloMusiImageConverter.py is used for converting a specialized graphic description text file into the custom image file format that is compatible with Ilo Musi. Please refer to the [template game repository](https://github.com/ilo-musi/template-game/blob/master/assets/src/images.txt) for an example of graphic description file.
* iloMusiMidiFileToCommandConverter.py converts MIDI file into a music format that's compatible with Ilo Musi. Please refer to [the definition of "const uint8_t bgm[]" in this file](https://github.com/ilo-musi/template-game/blob/master/src/main.c) for how the generated output could be used
* iloMusiRomPacker.py is used for packing game ROMs based metadata provided. [An example of metadata can be found here](https://github.com/ilo-musi/template-game/blob/master/assets/src/metadata.csv)
* iloMusiGenerateFont.py is used for generating the font used for the game console based on font.txt

The exact usage of the Python scripts is, unfortunately, currently undocumented.

This repository is licensed under BSD 2-Clause License.
