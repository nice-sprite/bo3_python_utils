#author: Mystic#9127
import os
import glob
import uuid
text = input("enter .txt file/folder path: ")

FILEPATH = "REPLACE_THIS_TEXT"

semantic_map = {
    "aoMap": "occlusionMap",
    "normalMap": "normalMap",
    "detailNormal2": "normalMap",
    "detailNormal3": "normalMap",
    "detailNormal1": "normalMap",
    "detailNormal4": "normalMap",
    "colorMap": "diffuseMap",
    "detailNormalMask": "multipleMask",
    "glossMap": "glossMap",
    "specColorMap": "specularMap",
    "velveteenMask": "revealMap",
    "tintMask": "revealMap",
    "thicknessMap": "thicknessMap",
    "revealMap": "revealMap",
    "camoMaskMap": "revealMap",
    "emissiveMap": "diffuseMap",
    "glossBodyMap": "glossMap",
    "normalBodyMap": "normalMap",
    "flickerLookupMap": "revealMap",
}

usingTempFile = False
outfile = os.path.split(text)
exportDetails = ''
if os.path.isdir(text):
    for files in glob.glob(f"{text}/*.txt"):
        exportDetails += open(files).read() + '\n'

    temp_file = f'{text}/temp-{uuid.uuid4()}.txt'
    print(f"writing temp file {temp_file}")
    outfile = open(temp_file, 'a+').write(exportDetails)
    text = temp_file
    usingTempFile = True
else:
    print(f'not a directory, reading in 1 file ({text})')
    exportDetails = open(text).read()


# print(exportDetails)

with open(text) as file:
    print(os.path.split(text))
    gdt_out = open(f"{os.path.split(text)[1].replace('.txt', '')}.gdt", "a+")
    gdt_out.write("{\n")  # begin output
    
    for line in file.readlines()[1:]:
        line = line.replace("\n", "")
        if len(line.split(',')) < 2:
            continue

        SEMANTIC = line.split(",")[0]
        NAME = line.split(",")[1].replace("\n", '')
        if 'unk' in SEMANTIC:
            print(f"UNKNOWN SEMANTIC '{SEMANTIC}' @ {line} ")
            continue
        if SEMANTIC in semantic_map:
            print(f'mapping {SEMANTIC} --> {semantic_map[SEMANTIC]}')
            SEMANTIC = semantic_map[SEMANTIC]

            
            
            
            gdt_entry = f"""
            "{NAME}" ( "image.gdf" )
            {{
                "baseImage" "{FILEPATH}\\\\{NAME}.png"
                "compressionMethod" "compressed"
                "semantic" "{SEMANTIC}"
                "type" "image"
            }}
    """
            # print(gdt_entry)
            gdt_out.write(gdt_entry)
        else:
            print(f'skipping {SEMANTIC},{NAME} because its not in semantic list... ')

    gdt_out.write("\n}")
    gdt_out.close()
if usingTempFile:
    os.remove(text)
