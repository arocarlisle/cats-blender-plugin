import tools.common
import tools.atlas

from bpy.types import Scene, Material
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, CollectionProperty


def register():
    Scene.armature = EnumProperty(
        name='Armature',
        description='Select the armature which will be used by Cats',
        items=tools.common.get_armature_list,
        update=tools.atlas.update_material_list
    )

    Scene.full_body = BoolProperty(
        name='Apply Full Body Tracking Fix',
        description="Applies a general fix for Full Body Tracking.\n\n"
                    'Can potentially reduce the knee bending of every avatar in VRChat.\n'
                    'You can safely ignore the "Spine length zero" warning in Unity.\n'
                    'If you have problems with the hips ingame, uncheck this option and tell us!\n',
        default=False
    )

    Scene.combine_mats = BoolProperty(
        name='Combine Same Materials',
        description="Combines similar materials into one, reducing draw calls.\n\n"
                    'Your avatar should visibly look the same after this operation.\n'
                    'This is a very important step for optimizing your avatar.\n'
                    'If you have problems with this, uncheck this option and tell us!\n',
        default=True
    )

    Scene.remove_zero_weight = BoolProperty(
        name='Remove Zero Weight Bones',
        description="Cleans up the bones hierarchy, deleting all bones that don't directly affect any vertices.\n"
                    'Uncheck this if bones you want to keep got deleted',
        default=True
    )

    Scene.keep_end_bones = BoolProperty(
        name='Keep End Bones',
        description="Saves end bones from deletion."
                    '\n\nThis can improve skirt movement for dynamic bones, but increases the bone count.'
                    '\nThis can also fix issues with crumbled finger bones in Unity.'
                    '\nMake sure to always uncheck "Add Leaf Bones" when exporting or use the CATS export button',
        default=False
    )

    Scene.use_google_only = BoolProperty(
        name='Use Old Translations (not recommended)',
        description="Ignores the internal dictionary and only uses the Google Translator for shape key translations."
                    "\n"
                    '\nThis will result in slower translation speed and worse translations, but the translations will be like in CATS version 0.9.0 and older.'
                    "\nOnly use this if you have animations which rely on the old translations and you don't want to convert them to the new ones",
        default=False
    )

    Scene.show_more_options = BoolProperty(
        name='Show More Options',
        description="Shows more model options",
        default=False
    )

    Scene.merge_mode = EnumProperty(
        name="Merge Mode",
        description="Mode",
        items=[
            ("ARMATURE", "Merge Armatures", "Here you can merge two armatures together."),
            ("MESH", "Attach Mesh", "Here you can attach a mesh to an armature.")
        ]
    )

    Scene.merge_armature_into = EnumProperty(
        name='Base Armature',
        description='Select the armature into which the other armature will be merged\n',
        items=tools.common.get_armature_list
    )

    Scene.attach_to_bone = EnumProperty(
        name='Attach to Bone',
        description='Select the bone to which the armature will be attached to\n',
        items=tools.common.get_bones_merge
    )

    Scene.merge_armature = EnumProperty(
        name='Merge Armature',
        description='Select the armature which will be merged into the selected armature above\n',
        items=tools.common.get_armature_merge_list
    )

    Scene.attach_mesh = EnumProperty(
        name='Attach Mesh',
        description='Select the mesh which will be attached to the selected bone in the selected armature\n',
        items=tools.common.get_top_meshes
    )

    Scene.merge_same_bones = BoolProperty(
        name='Merge Similar Named Bones',
        description='Merges all bones together that have the same name.'
                    '\nYou will have to make sure that all the bones you want to merge have the same name.'
                    '\n'
                    "\nIf this is checked, you won't need to fix the model with CATS beforehand but it is still advised to do so."
                    "\nIf this is unchecked, CATS will only merge the base bones (Hips, Spine, etc)."
                    "\n"
                    "\nThis can have unintended side effects, so check your model afterwards!"
                    "\n",
        default=False
    )

    # Decimation
    Scene.decimation_mode = EnumProperty(
        name="Decimation Mode",
        description="Decimation Mode",
        items=[
            ("SAFE", "Safe", 'Decent results - no shape key loss\n'
                             '\n'
                             "This will only decimate meshes with no shape keys.\n"
                             "The results are decent and you won't lose any shape keys.\n"
                             'Eye Tracking and Lip Syncing will be fully preserved.'),

            ("HALF", "Half", 'Good results - minimal shape key loss\n'
                             "\n"
                             "This will only decimate meshes with less than 4 shape keys as those are often not used.\n"
                             'The results are better but you will lose the shape keys in some meshes.\n'
                             'Eye Tracking and Lip Syncing should still work.'),

            ("FULL", "Full", 'Best results - full shape key loss\n'
                             '\n'
                             "This will decimate your whole model deleting all shape keys in the process.\n"
                             'This will give the best results but you will lose the ability to add blinking and Lip Syncing.\n'
                             'Eye Tracking will still work if you disable Eye Blinking.'),

            ("CUSTOM", "Custom", 'Custom results - custom shape key loss\n'
                                 '\n'
                                 "This will let you choose which meshes and shape keys should not be decimated.\n")
        ],
        default='HALF'
    )

    Scene.selection_mode = EnumProperty(
        name="Selection Mode",
        description="Selection Mode",
        items=[
            ("SHAPES", "Shape Keys", 'Select all the shape keys you want to preserve here.'),
            ("MESHES", "Meshes", "Select all the meshes you don't want to decimate here.")
        ]
    )

    Scene.add_shape_key = EnumProperty(
        name='Shape',
        description='The shape key you want to keep',
        items=tools.common.get_shapekeys_decimation
    )

    Scene.add_mesh = EnumProperty(
        name='Mesh',
        description='The mesh you want to leave untouched by the decimation',
        items=tools.common.get_meshes_decimation
    )

    Scene.decimate_fingers = BoolProperty(
        name="Save Fingers",
        description="Check this if you don't want to decimate your fingers!\n"
                    "Results will be worse but there will be no issues with finger movement.\n"
                    "This is probably only useful if you have a VR headset.\n"
                    "\n"
                    "This operation requires the finger bones to be named specifically:\n"
                    "Thumb(0-2)_(L/R)\n"
                    "IndexFinger(1-3)_(L/R)\n"
                    "MiddleFinger(1-3)_(L/R)\n"
                    "RingFinger(1-3)_(L/R)\n"
                    "LittleFinger(1-3)_(L/R)"
    )

    Scene.decimate_hands = BoolProperty(
        name="Save Hands",
        description="Check this if you don't want to decimate your full hands!\n"
                    "Results will be worse but there will be no issues with hand movement.\n"
                    "This is probably only useful if you have a VR headset.\n"
                    "\n"
                    "This operation requires the finger and hand bones to be named specifically:\n"
                    "Left/Right wrist\n"
                    "Thumb(0-2)_(L/R)\n"
                    "IndexFinger(1-3)_(L/R)\n"
                    "MiddleFinger(1-3)_(L/R)\n"
                    "RingFinger(1-3)_(L/R)\n"
                    "LittleFinger(1-3)_(L/R)"
    )

    Scene.max_tris = IntProperty(
        name='Tris',
        description="The target amount of tris after decimation",
        default=19999,
        min=1,
        max=100000
    )

    # Eye Tracking
    Scene.eye_mode = EnumProperty(
        name="Eye Mode",
        description="Mode",
        items=[
            ("CREATION", "Creation", "Here you can create eye tracking."),
            ("TESTING", "Testing", "Here you can test how eye tracking will look ingame.")
        ],
        update=tools.eyetracking.stop_testing
    )

    Scene.mesh_name_eye = EnumProperty(
        name='Mesh',
        description='The mesh with the eyes vertex groups',
        items=tools.common.get_meshes
    )

    Scene.head = EnumProperty(
        name='Head',
        description='The head bone containing the eye bones',
        items=tools.common.get_bones_head
    )

    Scene.eye_left = EnumProperty(
        name='Left Eye',
        description='The models left eye bone',
        items=tools.common.get_bones_eye_l
    )

    Scene.eye_right = EnumProperty(
        name='Right Eye',
        description='The models right eye bone',
        items=tools.common.get_bones_eye_r
    )

    Scene.wink_left = EnumProperty(
        name='Blink Left',
        description='The shape key containing a blink with the left eye',
        items=tools.common.get_shapekeys_eye_blink_l
    )

    Scene.wink_right = EnumProperty(
        name='Blink Right',
        description='The shape key containing a blink with the right eye',
        items=tools.common.get_shapekeys_eye_blink_r
    )

    Scene.lowerlid_left = EnumProperty(
        name='Lowerlid Left',
        description='The shape key containing a slightly raised left lower lid.\n'
                    'Can be set to "Basis" to disable lower lid movement',
        items=tools.common.get_shapekeys_eye_low_l
    )

    Scene.lowerlid_right = EnumProperty(
        name='Lowerlid Right',
        description='The shape key containing a slightly raised right lower lid.\n'
                    'Can be set to "Basis" to disable lower lid movement',
        items=tools.common.get_shapekeys_eye_low_r
    )

    Scene.disable_eye_movement = BoolProperty(
        name='Disable Eye Movement',
        description='IMPORTANT: Do your decimation first if you check this!\n'
                    '\n'
                    'Disables eye movement. Useful if you only want blinking.\n'
                    'This creates eye bones with no movement bound to them.\n'
                    'You still have to assign "LeftEye" and "RightEye" to the eyes in Unity',
        subtype='DISTANCE'
    )

    Scene.disable_eye_blinking = BoolProperty(
        name='Disable Eye Blinking',
        description='Disables eye blinking. Useful if you only want eye movement.\n'
                    'This will create the necessary shape keys but leaves them empty',
        subtype='NONE'
    )

    Scene.eye_distance = FloatProperty(
        name='Eye Movement Range',
        description='Higher = more eye movement\n'
                    'Lower = less eye movement\n'
                    'Warning: Too little or too much range can glitch the eyes.\n'
                    'Test your results in the "Eye Testing"-Tab!\n',
        default=0.8,
        min=0.0,
        max=2.0,
        step=1.0,
        precision=2,
        subtype='FACTOR'
    )

    Scene.eye_rotation_x = IntProperty(
        name='Up - Down',
        description='Rotate the eye bones on the vertical axis',
        default=0,
        min=-19,
        max=25,
        step=1,
        subtype='FACTOR',
        update=tools.eyetracking.set_rotation
    )

    Scene.eye_rotation_y = IntProperty(
        name='Left - Right',
        description='Rotate the eye bones on the horizontal axis.'
                    '\nThis is from your own point of view',
        default=0,
        min=-19,
        max=19,
        step=1,
        subtype='FACTOR',
        update=tools.eyetracking.set_rotation
    )

    Scene.iris_height = IntProperty(
        name='Iris Height',
        description='Moves the iris away from the eye ball',
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='FACTOR'
    )

    Scene.eye_blink_shape = FloatProperty(
        name='Blink Strength',
        description='Test the blinking of the eye',
        default=1.0,
        min=0.0,
        max=1.0,
        step=1.0,
        precision=2,
        subtype='FACTOR'
    )

    Scene.eye_lowerlid_shape = FloatProperty(
        name='Lowerlid Strength',
        description='Test the lowerlid blinking of the eye',
        default=1.0,
        min=0.0,
        max=1.0,
        step=1.0,
        precision=2,
        subtype='FACTOR'
    )

    # Visemes
    Scene.mesh_name_viseme = EnumProperty(
        name='Mesh',
        description='The mesh with the mouth shape keys',
        items=tools.common.get_meshes
    )

    Scene.mouth_a = EnumProperty(
        name='Viseme AA',
        description='Shape key containing mouth movement that looks like someone is saying "aa".\nDo not put empty shape keys like "Basis" in here',
        items=tools.common.get_shapekeys_mouth_ah,
    )

    Scene.mouth_o = EnumProperty(
        name='Viseme OH',
        description='Shape key containing mouth movement that looks like someone is saying "oh".\nDo not put empty shape keys like "Basis" in here',
        items=tools.common.get_shapekeys_mouth_oh,
    )

    Scene.mouth_ch = EnumProperty(
        name='Viseme CH',
        description='Shape key containing mouth movement that looks like someone is saying "ch". Opened lips and clenched teeth.\nDo not put empty shape keys like "Basis" in here',
        items=tools.common.get_shapekeys_mouth_ch,
    )

    Scene.shape_intensity = FloatProperty(
        name='Shape Key Mix Intensity',
        description='Controls the strength in the creation of the shape keys. Lower for less mouth movement strength',
        default=1.0,
        min=0.0,
        max=10.0,
        step=0.1,
        precision=2,
        subtype='FACTOR'
    )

    # Bone Parenting
    Scene.root_bone = EnumProperty(
        name='To Parent',
        description='List of bones that look like they could be parented together to a root bone',
        items=tools.rootbone.get_parent_root_bones,
    )

    # Optimize
    Scene.optimize_mode = EnumProperty(
        name="Optimize Mode",
        description="Mode",
        items=[
            ("ATLAS", "Atlas", "Allows you to make a texture atlas."),
            ("MATERIAL", "Material", "Some various options on material manipulation."),
            ("BONEMERGING", "Bone Merging", "Allows child bones to be merged into their parents."),
        ]
    )

    # Atlas
    Material.add_to_atlas = BoolProperty(
        description='Add this material to the atlas',
        default=False
    )

    Scene.material_list_index = IntProperty(
        default=0
    )

    Scene.material_list = CollectionProperty(
        type=tools.atlas.MaterialsGroup
    )

    Scene.clear_materials = BoolProperty(
        description='Clear materials checkbox',
        default=True
    )

    # Bone Merging
    Scene.merge_ratio = FloatProperty(
        name='Merge Ratio',
        description='Higher = more bones will be merged\n'
                    'Lower = less bones will be merged\n',
        default=50,
        min=1,
        max=100,
        step=1,
        precision=0,
        subtype='PERCENTAGE'
    )

    Scene.merge_mesh = EnumProperty(
        name='Mesh',
        description='The mesh with the bones vertex groups',
        items=tools.common.get_meshes
    )

    Scene.merge_bone = EnumProperty(
        name='To Merge',
        description='List of bones that look like they could be merged together to reduce overall bones',
        items=tools.rootbone.get_parent_root_bones,
    )

    # Settings
    Scene.embed_textures = BoolProperty(
        name='Embed Textures on Export',
        description='Enable this to embed the texture files into the FBX file upon export.'
                    '\nUnity will automatically extract these textures and put them into a separate folder.'
                    '\nThis might not work for everyone and it increases the file size of the exported FBX file',
        default=False,
        update=tools.settings.update_settings
    )
    Scene.use_custom_mmd_tools = BoolProperty(
        name='Use Custom mmd_tools',
        description='Enable this to use your own version of mmd_tools. This will disable the internal cats mmd_tools',
        default=False,
        update=tools.settings.update_settings
    )

    Scene.debug_translations = BoolProperty(
        name='Debug Google Translations',
        description='Tests the Google Translations and prints the Google response in case of error',
        default=False
    )

    # Scene.disable_vrchat_features = BoolProperty(
    #     name='Disable VRChat Only Features',
    #     description='This will disable features which are solely used for VRChat.'
    #                 '\nThe following will be disabled:'
    #                 '\n- Eye Tracking'
    #                 '\n- Visemes',
    #     default=False,
    #     update=tools.settings.update_settings
    # )

    # Copy Protection - obsolete
    # Scene.protection_mode = EnumProperty(
    #     name="Randomization Level",
    #     description="Randomization Level",
    #     items=[
    #         ("FULL", "Full", "This will randomize every vertex of your model and it will be completely unusable for thieves.\n"
    #                          'However this method might cause problems with the Outline option from Cubed shader.\n'
    #                          'If you have any issues ingame try again with option "Partial".'),
    #         ("PARTIAL", "Partial", 'Use this if you experience issues ingame with the Full option!\n'
    #                                '\n'
    #                                "This will only randomize a number of vertices and therefore will have a few unprotected areas,\n"
    #                                "but it's still unusable to thieves as a whole.\n"
    #                                'This method however reduces the glitches that can occur ingame by a lot.')
    #     ],
    #     default='FULL'
    # )