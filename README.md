# blender-hdri-gen
Blender add-on to generate HDRI environmental maps using World Shading nodes.
# Installation
Download the `blender-hdri-gen.zip` from [Releases](https://github.com/Alythea/blender-hdri-gen/releases) and install it using Blender's built-in add-on installer, located in Edit > Preferences > Add-ons > Install... and select the .zip archive. Afterwards enable the newly installed add-on.
# Usage
Once installed, the add-on can be accessed in the World Shader tab in the Shading environment. The add-on adds a new category containing nodes into the drop down menu Add used to generate HDRIs. 

Each node contains its own user interface with properties that can be edited by the user and a render operator that renders the scene with the inputted properties and sets the rendered .exr file as the output of the node.
