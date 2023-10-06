import math
from pymatgen.core import Lattice, Structure, Molecule
from pymatgen.io.vasp.inputs import Poscar

class StructureBuilder:
    def __init__(self, filename: str):
        self.filename = filename
        self.elements = []
        self.a = 0
        self.c = 0
        self.coordinates = []
        self.built_structure = None
        self.poscar = None  # To hold the Poscar object
        
    def extract_elements(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        self.elements = [line.split()[0] for line in lines[2:]]

# Included staticmethod decorator so that the alttice constant can be called without making an instance, since it doesnt need access to instance attributes
    @staticmethod
    def lattice_constant(x, y, z):
        return math.sqrt(x**2 + y**2 + z**2)

    def extract_lattice_values_from_file(self):
        with open(self.filename, 'r') as file:
            # Read the first two lines to account for the lattice being on either the first or second line
            first_line = file.readline().strip()
            second_line = file.readline().strip()
        
            if 'Lattice="' in first_line:
                lattice_line = first_line
            elif 'Lattice="' in second_line:
                lattice_line = second_line
            else:
                raise ValueError("The .xyz file is missing lattice constants in the first or second line.")
        
            lattice_values = lattice_line.split('Lattice="')[1].split('"')[0]
            return [float(value) for value in lattice_values.split()]

    
    def calculate_lattice_constants(self):
        values = self.extract_lattice_values_from_file()
        a = StructureBuilder.lattice_constant(values[0], values[1], values[2])
        c = StructureBuilder.lattice_constant(values[6], values[7], values[8])
        return a, c
    
    def set_lattice_constants(self):
        a, c = self.calculate_lattice_constants()
        self.a = a
        self.c = c
        
    def construct_coordinates(self):
        xyz = Molecule.from_file(self.filename)
        self.coordinates = xyz.cart_coords
        
    def build_structure(self):
        if not self.elements or len(self.coordinates) == 0 or self.a == 0 or self.c == 0:
            raise ValueError("Essential data is missing for structure construction")
        self.built_structure = Structure(Lattice.hexagonal(self.a, self.c), self.elements, self.coordinates, coords_are_cartesian=True)

    def supercell(self, scell_a, scell_b, scell_c):
        self.supercell_dimensions = (scell_a, scell_b, scell_c)
        self.supercell_structure = self.built_structure.make_supercell([scell_a, scell_b, scell_c])

    def convert_to_poscar(self):
        if self.built_structure is None:
            raise ValueError("Structure must be built before converting to POSCAR")
        if hasattr(self, 'supercell_structure'):
            self.poscar = Poscar(structure = self.supercell_structure)
        else:
            self.poscar = Poscar(structure = self.built_structure)

    
    def write_poscar_to_file(self):
        if self.poscar is None:
            raise ValueError("Poscar must be initialized before writing to a file")
    
        # Extract the base name of the file (without extension) and append the supercell dimensions and ".vasp"
        base_name = self.filename.rsplit('.', 1)[0]
        supercell_str = f"{self.supercell_dimensions[0]}x{self.supercell_dimensions[1]}x{self.supercell_dimensions[2]}"
        poscar_filename = f"{base_name}_{supercell_str}.vasp"
        self.poscar.write_file(poscar_filename)

        
    def display(self):
        print(self.elements)
        if self.poscar:
            # Use the updated write_poscar_to_file method here
            self.write_poscar_to_file()
            print(self.poscar)
        elif self.built_structure:
            print(self.built_structure)


