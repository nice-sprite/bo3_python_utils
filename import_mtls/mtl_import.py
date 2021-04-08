# author: Mystic#9127
import os
import glob

import uuid


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
    "detailMap": "normalMap",
}   

mtl_sems = {
	'mixMap': 'alphaRevealMap',
	'aoMap': 'occMap',
	'specularMapDetail2': 'colorMap03',
	'unk_semantic_0x5031EE8E': 'colorMap02',
	'detailMap1': 'detailMap',
	'detailMap2': 'colorMap00',
	'normalMap': 'normalMap',
	'colorMapDetail2': 'colorMap01',
	'colorMap': 'colorMap',
	'glossMap': 'cosinePowerMap',
	'specColorMap': 'specColorMap',
	'unk_semantic_0x13817CC0': 'camoMaskMap',
	'detailNormal2': 'colorMap01',
	'detailNormal3': 'colorMap02',
	'detailNormal1': 'detailMap',
	'detailNormal4': 'colorMap03',
	'detailNormalMask': 'colorMap04',
	'emissiveMap1': 'colorMap00',
	'emissiveMap2': 'colorMap01',
	'emissiveMap3': 'colorMap02',
	'tintMask': 'colorMap00',
	'alphaMap': 'alphaRevealMap',
	'emissiveMap': 'colorMap00',
	'alphaMaskMap': 'colorMap02',
}

export_dir = input(""" Enter path to the "_images" folder for your model, 

Example: model_export\\kingslayer_kyle\\my_model\\_images

(Press enter to skip, find "REPLACE_THIS_TEXT" in a text editor)""")
if (export_dir == ""):
    export_dir = "REPLACE_THIS_TEXT"

def map_semantic(sem): 

     
    if sem in semantic_map.keys():
        mapped_sem = semantic_map[sem]
        print(f'\tmapped {sem} -> {mapped_sem}')
        return mapped_sem
    else: 
        print(f'\tmapping not found for {sem}, skipping import') 
        return False


def parse_mtls(mtl_images):
    mtls = []
    for mtl in mtl_images:
        mtl = mtl.replace("\n", '')
        sem, img = mtl.split(',')
        mtls.append({'semantic': sem, 'image': img})
    return mtls


def img_gdt_format(img):
    
    template = """
            "{img_name}" ( "image.gdf" )
            {{
                "baseImage" "{export_dir}\\\\{img_name}.png"
                "semantic" "{semantic}"
                "type" "image"
            }}
    """
    return template.format(img_name = img['image'], semantic = img['semantic'], export_dir = export_dir)
    
seen = []
def has_img_been_added(img_name):
    if img_name in seen:
        return True
    else:
        seen.append(img_name)
        return False
            

def import_images(gdt_file, images):
    """adds all the images contained in a .txt to the gdt

    Args:
        gdt_file (file handle): handle to the gdt file we are writing to
        images (list): list of {semantic, image} representing each line of the .txt file. 
    """
    
    for img in images:
        mapped_sem = map_semantic(img['semantic']) 
        if mapped_sem:
            if not has_img_been_added(img['image']): # should remove duplicate image entries, but still add them to mtls
                img['semantic'] = mapped_sem
                img_entry = img_gdt_format(img)
                gdt_file.write(img_entry)
        else: 
            print(f'\tskipping {img} because of unknown semantic.')


def mtl_entry(mtl_name, mtl_images):
    template = """
            "{mtl_name}" ( "material.gdf" )
            {{
                "materialCategory" "Geometry"
                "materialType" "lit"
{img_list}
            }}
    """
    # img_list is the insertion point for the list of images used for the material

    img_list = ""
    for img in mtl_images:
        #if img["semantic"] in semantic_map.keys():
            if img['semantic'] in mtl_sems.keys(): 
                img['semantic'] = mtl_sems[img['semantic']]
            img_list += '\t\t\t\t"{semantic}" "{img}" \n'.format(semantic = img["semantic"], img = img["image"])
    return template.format(mtl_name = mtl_name, img_list = img_list)


def start_gdt(output_name):
    gdt = open(f'{output_name}.gdt', 'a+')
    gdt.write("{\n")
    return gdt


def end_gdt(gdt_file):
    gdt_file.write("\n}")
    gdt_file.close()

#oop
def main():
    # sets up the gdt output file
    input_directory = input("enter .txt folder path: ") # get the directory 
    gdt_out = start_gdt(os.path.split(input_directory)[1])
    print(os.path.split(input_directory)[1])
    
    for file in glob.glob(f'{input_directory}/*.txt'):
        print(f"processing {os.path.split(file)[1]}...")
        mtl_name = os.path.split(file)[1].replace(' ', '_').replace("_images.txt", "")
        # print(mtl_name)
        mtl_list = parse_mtls(open(file).readlines()[1:])
        mtl_list_2 =  parse_mtls(open(file).readlines()[1:])
        import_images(gdt_out, mtl_list)
        gdt_out.write(mtl_entry(mtl_name, mtl_list_2))
        #import images
        #import mtl
    end_gdt(gdt_out)
        

if __name__ == "__main__":
    main()