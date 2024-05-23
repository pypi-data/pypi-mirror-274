# LAMMPS Dump Reader
A fast and memory-efficient LAMMPS dump file reader with great developer experience.

## Project Charter
**Goal:** The goal of this project is to develop an open-source Python package that can read LAMMPS dump files into Python for further analysis.

**Objectives:**
1. The package will be unopinionated. All `dump` and `dump_modify` configurations will be easy to read, and all output data will be treated on equal footing.
2. The package will be easy to install using `pip`.
3. The package will have a good developer experience, including type-hinting and documentation.
4. The package will be fast and memory-efficient (only one frame will be loaded into memory at a time).

### Envisioned usage
There will be two overarching ways to use this package. The most forgiving way would be to use
```python
import dump_reader

# Bring whole dump file into memory
data = dump_reader.read_whole_dump("dump.lammpstrj")
```
This will bring the entire dump file into memory, so that it can be accessed at any point.

Because dump files may be large, you may not want to bring the whole file into memory at once. In this case, you can use
```python
import dump_reader

timesteps = []
positions = []

# Bring each snapshot in individually
for snapshot in dump_reader.read_dump("dump.lammpstrj"):
    timesteps.append(snapshot["TIMESTEP"])
    positions.append([])

    for atom in snapshot["ATOMS"]:
        if atom["element"] == "Li":
            positions[-1].append([atom["xu"], atom["yu"], atom["zu"]])
```
You would extract the information needed at the start of the script. `read_dump` would return an generator object, so that each snapshot is read in only as needed.

### Milestones
1. Implement `read_whole_dump`.
2. Implement `read_dump` using what was learned.
3. Potentially rewrite `read_whole_dump`, if performance improvements are expected.
4. Potentially rewrite the whole package with Rust bindings.


### Current Usage
```python
import undumper 

data = undumper.read_dump(file) #where file can be a classic, grid or yaml lammps dump file 

for snapshot in data:
    timesteps.append(snapshot["TIMESTEP"])
    positions.append([])

    for atom in snapshot["ATOMS"]:
        if atom["element"] == "Li":
            positions[-1].append([atom["xu"], atom["yu"], atom["zu"]])

whole_data = undumper.read_whole_dump(file) #where file can be a classic, grid or yaml lammps dump file
```

The output data structure in each of these cases looks as follows, the only difference is that read_dump generates a dictionary representing one frame and read_whole dump generates a list of dictionaries with each being an individual frame

```python
unDumped = [{'TIMESTEP':0, 'NUMBER OF ATOMS':1600, 'BOX BOUNDS':{x: [0,0], y: [0,0]. z: [0,0]}, 'ATOMS':{id: 1, 'Element': "Li", "xu": 1, "yu": 2, "zu": 3}]
```

### FUll COMMAND LIST

**read_dump**
**read_whole_dump**
**read_classic**
**read_yaml**
**read_grid**
