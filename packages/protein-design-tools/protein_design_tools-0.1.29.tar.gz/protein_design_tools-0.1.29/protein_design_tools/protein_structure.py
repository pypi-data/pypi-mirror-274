"""
protein_structure.py
====================================
The protein_structure module contains the ProteinStructure class, which represents a protein structure and its 
components.
"""
from pathlib import Path
import h5py
import numpy as np

# Atomic weights from https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=ascii
ATOMIC_WEIGHTS = {
    'H': 1.00794075405578,
    'C': 12.0107358967352,
    'N': 14.0067032114458,
    'O': 15.9994049243183,
    'S': 32.0647874061271
    # Add the rest of the elements here
}

# Dictionary to convert three-letter amino acid codes to one-letter codes
THREE_TO_ONE = {'ALA': 'A',
                'ARG': 'R',
                'ASN': 'N',
                'ASP': 'D',
                'CYS': 'C',
                'GLN': 'Q',
                'GLU': 'E',
                'GLY': 'G',
                'HIS': 'H',
                'ILE': 'I',
                'LEU': 'L',
                'LYS': 'K',
                'MET': 'M',
                'PHE': 'F',
                'PRO': 'P',
                'SER': 'S',
                'THR': 'T',
                'TRP': 'W',
                'TYR': 'Y',
                'VAL': 'V'
                }

ATOM_NAME_TO_ELEMENT = {'N': 'N',
                        'CA': 'C',
                        'C': 'C',
                        'O': 'O',
                        'CB': 'C',
                        'CG': 'C',
                        'CG1': 'C',
                        'CG2': 'C',
                        'CD': 'C',
                        'CD1': 'C',
                        'CD2': 'C',
                        'CE': 'C',
                        'CE1': 'C',
                        'CE2': 'C',
                        'CE3': 'C',
                        'CZ': 'C',
                        'CZ2': 'C',
                        'CZ3': 'C',
                        'CH2': 'C',
                        'ND1': 'N',
                        'ND2': 'N',
                        'NE': 'N',
                        'NE1': 'N',
                        'NE2': 'N',
                        'NH1': 'N',
                        'NH2': 'N',
                        'NZ': 'N',
                        'SD': 'S',
                        'SG': 'S',
                        'OG': 'O',
                        'OG1': 'O',
                        'OD1': 'O',
                        'OD2': 'O',
                        'OE1': 'O',
                        'OE2': 'O',
                        'OH': 'O',
                        'OXT': 'O',
                        'H': 'H'}

class ProteinStructure:
    """ProteinStruture represents a protein structure and its components."""
    def __init__(self, name=None):
        """
        Initialize a ProteinStructure object.

        Parameters
        ----------
        name : str, optional
            The name of the protein structure. Defaults to None.
        """
        self.name = None
        self.chains = []

    class Chain:
        """Chain represents a chain in a protein structure."""
        def __init__(self, name):
            """
            Initialize a Chain object, which will contain a list of Residue objects.
            
            Parameters
            ----------
            name : str
                chainID - chain identifier
            """
            self.name = name
            self.residues = [] # list of Residue objects

        class Residue:
            """Represents a residue in a protein structure."""
            # Residue class will contain a list of Atom objects
            def __init__(self, name, res_seq, i_code):
                """
                Initialize a Residue object, which will contain a list of Atom objects.
                
                Parameters
                ----------
                res_name : str
                    The name of the residue.
                res_seq : int
                    The sequence number of the residue.
                i_code : str
                    The insertion code of the residue.
                """
                self.name = name
                self.res_seq = res_seq
                self.i_code = i_code

                # Unique identifiers for each residue
                self.index = None
                self.res_seq_i = f"{res_seq}{i_code}"
                self.res_name_seq_i = f"{name}{res_seq}{i_code}"

                self.atoms = [] # list of Atom objects

            class Atom:
                """Represents an atom in a protein structure."""
                def __init__(self, atom_id, name, alt_loc, x, y, z, occupancy, temp_factor, segment_id, element, charge):
                    """
                    Initialize an Atom object.
                    
                    Parameters
                    ----------
                    atom_id : int
                        The atom serial number.
                    name : str
                        The atom  name.
                    alt_loc : str
                        The alternate location indicator.
                    x : float
                        The orthogonal coordinates for X in Angstroms.
                    y : float
                        The orthogonal coordinates for Y in Angstroms.
                    z : float
                        The orthogonal coordinates for Z in Angstroms.
                    occupancy : float
                        The occupancy of the atom.
                    temp_factor : float
                        The temperature factor of the atom.
                    segment_id : str
                        The segment ID.
                    element : str
                        The element symbol of the atom.
                    charge : str
                        The charge on the atom.
                    """
                    self.atom_id = atom_id
                    self.name = name
                    self.alt_loc = alt_loc
                    self.x = x
                    self.y = y
                    self.z = z
                    self.occupancy = occupancy
                    self.temp_factor = temp_factor
                    self.segment_id = segment_id
                    self.element = element
                    self.charge = charge

                    # Calculate the mass of the atom
                    self.mass = ATOMIC_WEIGHTS[element]
    
    def read_pdb(self, file_path, chains=None, name=None):
        """
        Read a PDB file and populate the ProteinStructure object with its contents. Atom elements are obtained from the
        atom name. 
        
        Note: The element is determined from columns 13-14 of the PDB file, so check that your PDB file is formatted
        correctly. Specifically, hydrogen atoms can sometimes have weird names such as 'HE11', and this function would
        incorrectly assign helium as the element. If you encounter this issue, you can manually set the element of the
        atom after reading the PDB file. 
        
        Reference: https://cdn.rcsb.org/wwpdb/docs/documentation/file-format/PDB_format_1992.pdf
        
        Parameters
        ----------
        file_path : str
            The path to the PDB file.
        chains : str or list of str, optional
            The chain(s) to read from the PDB file. If None, read all chains. Defaults to None.
        name : str, optional
            The name of the protein structure. Defaults to None.
        """
        self.name = name # The name of the protein structure. Defaults to None.

        # If the user passed a string for chains, convert it to a list
        if isinstance(chains, str):
            chains = [chains]

        # Parse PDB file and populate self.atoms
        p = Path(file_path)
        if p.suffix == ".pdb":
            with open(p, "r") as f:
                for line in f:
                    if line.startswith("ATOM"):

                        chain_name = line[21].strip()
                        # Check if the chain already exists in self.chains
                        chain = next((c for c in self.chains if c.name == chain_name), None)
                        if chains is None or chain_name in chains:
                            if chain is None:
                                chain = self.Chain(chain_name)
                                self.chains.append(chain)

                            # Check if the residue already exists in self.residues
                            res_name = line[17:20].strip()
                            res_seq = int(line[22:26].strip())
                            i_code = line[26].strip()
                            residue = next((r for r in chain.residues if r.res_seq == res_seq and r.i_code == i_code), None)
                            if residue is None:
                                # Create a Residue object and append it to self.residues
                                residue = self.Chain.Residue(res_name, res_seq, i_code)
                                # Check if the residue index is already assigned, if not assign it
                                if residue.index is None:
                                    # assign it next index value in the chain
                                    residue.index = len(chain.residues)
                                chain.residues.append(residue)

                            # Check if the atom already exists in self.atoms
                            atom_id = int(line[6:11].strip())
                            element = line[12:14].strip()
                            atom_name = line[12:16].strip()
                            alt_loc = line[16].strip()
                            x = float(line[30:38].strip())
                            y = float(line[38:46].strip())
                            z = float(line[46:54].strip())
                            occupancy = float(line[54:60].strip())
                            temp_factor = float(line[60:66].strip())
                            
                            segment_id = line[72:76].strip()
                            charge = line[78:80].strip()

                            # remove digits from element
                            if element in ['1H', '2H', '3H']:
                                element = 'H'

                            atom = next((a for a in residue.atoms if a.atom_id == atom_id), None)
                            if atom is None:
                                # Create an Atom object and append it to self.atoms
                                atom = self.Chain.Residue.Atom(atom_id, atom_name, alt_loc, x, y, z, occupancy, temp_factor, segment_id, element, charge)
                                residue.atoms.append(atom)

    
    def generate_coordinates(self):
        """
        Generate a dictionary of coordinates from the Structure object.

        Returns
        -------
        dict
            A dictionary of coordinates. The keys are the chain names and the values are the coordinate data.
            Each coordinate is a 4-element array [x, y, z, b], where x, y, and z are the coordinates, and b is a binary
            flag indicating whether the atom is a backbone atom (1) or not (0).
        """
        coordinates = {}
        for chain in self.structure:
            chain_coordinates = []
            for residue in chain:
                for atom in residue:
                    is_backbone = 1 if atom.name in ['N', 'CA', 'C', 'O'] else 0
                    chain_coordinates.append(np.append(atom.coord, is_backbone))
            coordinates[chain.id] = np.array(chain_coordinates)
        return coordinates 
    
    def get_sequence_dict(self):
        """
        Return the sequence of the protein structure as a dictionary of chains and sequences.

        :returns: A dictionary of chains and sequences. The keys are the chain names and the values are the sequences.
        :rtype: dict
        """
        sequences = {}
        for chain in self.chains:
            sequence = ""
            for residue in chain.residues:
                sequence += THREE_TO_ONE[residue.name]
            sequences[chain.name] = sequence
        return sequences
    
    def write_coordinates_hdf5(file_path, coordinates):
        """
        Write coordinate data to an HDF5 file.

        Parameters
        ----------
        file_path : str
            The path to the HDF5 file.
        coordinates : dict
            A dictionary of coordinates. The keys are the chain names and the values are the coordinate data.
        """
        with h5py.File(file_path, 'w') as f:
            for chain_name, chain_coordinates in coordinates.items():
                f.create_dataset(chain_name, data=chain_coordinates)

    def read_coordinates_hdf5(file_path):
        """
        Read coordinate data from an HDF5 file.

        Parameters
        ----------
        file_path : str
            The path to the HDF5 file.

        Returns
        -------
        dict
            A dictionary of coordinates. The keys are the chain names and the values are the coordinate data.
        """
        coordinates = {}
        with h5py.File(file_path, 'r') as f:
            for chain_name in f.keys():
                coordinates[chain_name] = f[chain_name][:]
        return coordinates
