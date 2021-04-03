# author: Mystic#9127
import os
import glob
import uuid


def map_semantic(sem): 
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
                "baseImage" "REPLACE_THIS_TEXT\\\\{img_name}.png"
                "compressionMethod" "compressed"
                "semantic" "{semantic}"
                "type" "image"
            }}
    """
    return template.format(img_name = img['image'], semantic = img['semantic'])
    

def import_images(gdt_file, images):
    """adds all the images contained in a .txt to the gdt

    Args:
        gdt_file (file handle): handle to the gdt file we are writing to
        images (list): list of {semantic, image} representing each line of the .txt file. 
    """
    # print(images)
    for img in images:
        mapped_sem = map_semantic(img['semantic']) 
        if mapped_sem:
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
        img_list += '\t\t\t\t"{semantic}" "{img}" \n'.format(semantic = img["semantic"], img = img["image"])
    return template.format(mtl_name = mtl_name, img_list = img_list)


def start_gdt():
    gdt = open(f'{uuid.uuid4()}.gdt', 'a+')
    gdt.write("{\n")
    return gdt


def end_gdt(gdt_file):
    gdt_file.write("\n}")
    gdt_file.close()

#oop
def main():
    # sets up the gdt output file
    gdt_out = start_gdt()
    input_directory = input("enter .txt folder path: ") # get the export directory 
    for file in glob.glob(f'{input_directory}/*.txt'):
        print(f"processing {os.path.split(file)[1]}...")
        mtl_name = os.path.split(file)[1].replace(' ', '_').replace(".txt", "")
        # print(mtl_name)
        mtl_list = parse_mtls(open(file).readlines()[1:])
    
        import_images(gdt_out, mtl_list)
        gdt_out.write(mtl_entry(mtl_name, mtl_list))
        #import images
        #import mtl
    end_gdt(gdt_out)
        

if __name__ == "__main__":
    main()
