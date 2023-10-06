"""
A very simple (too simple?) way of generating a simple vacancy in a POSCAR file.

Use Example: (given that POSCAR file is stored in ../structures)
python3 defect_generation.py

File name of POSCAR to defect:  "Input POSCAR name"
Enter site of defect:  "Input site to defect"
Name of defect POSCAR:  "Input filename to save to"

Current limitations, you must know which site to defect (ie for 2x2 MoS2, there are 4 Mo and 8 S, So index 0-3 describes Mo and 4-7 describes S)
"""

from pathlib import Path
from pymatgen.analysis.defects.core import Vacancy
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar

class DefectFormation:
    STRUCTURE_FILES = Path("../structures")
    
    def __init__(self, filename: str):
        self.filename = filename
        self.structure = Structure.from_file(DefectFormation.STRUCTURE_FILES / self.filename)
        self.defect_structure = None
    
    def create_vacancy(self, site_index: int):
        vac_site = self.structure[site_index]
        self.defect_structure = Vacancy(self.structure, site=vac_site)
        return self.defect_structure
    
    def write_poscar(self, output_filename: str):
        if not self.defect_structure:
            raise ValueError("Defect structure has not been initialized.")
        defect_poscar = Poscar(self.defect_structure.defect_structure)
        defect_poscar.write_file(output_filename)

if __name__ == "__main__":
    filename = input("File name of POSCAR to defect: ")
    site_index = int(input("Enter site of defect: "))
    output_filename = input("Name of defect POSCAR: ")
    
    defect_creator = DefectFormation(filename)
    defect = defect_creator.create_vacancy(site_index)
    print(defect)
    
    defect_creator.write_poscar(output_filename)

