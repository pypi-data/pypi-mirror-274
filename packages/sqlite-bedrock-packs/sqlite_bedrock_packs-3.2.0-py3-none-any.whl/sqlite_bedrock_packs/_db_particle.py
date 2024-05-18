# pylint: disable=no-member, multiple-statements, missing-module-docstring, missing-class-docstring
from sqlite3 import Connection
from pathlib import Path
import json
from .better_json_tools import load_jsonc
from ._views import dbtableview, WeakTableConnection

@dbtableview(
    properties={
        "path": (Path, "NOT NULL")
    },
    connects_to=["ResourcePack"]
)
class ParticleFile: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "material": (str, ""),
        "texture": (str, "")
    },
    connects_to=["ParticleFile"],
    weak_connects_to=[
        WeakTableConnection("texture", "TextureFile", "identifier")
    ]
)
class Particle: ...

PARTICLE_BUILD_SCRIPT: str = (
    ParticleFile.build_script +
    Particle.build_script
)

def load_particles(db: Connection, rp_id: int):
    '''
    Loads all particles from the resource pack.
    '''
    rp_path: Path = db.execute(
        "SELECT path FROM ResourcePack WHERE ResourcePack_pk = ?",
        (rp_id,)
    ).fetchone()[0]

    for particle_path in (rp_path / "particles").rglob("*.json"):
        load_particle(db, particle_path, rp_id)

def load_particle(db: Connection, particle_path: Path, rp_id: int):
    '''
    Loads a particle from the resource pack.
    '''
    cursor = db.cursor()
    # PARTICLE FILE
    cursor.execute(
        "INSERT INTO ParticleFile (path, ResourcePack_fk) VALUES (?, ?)",
        (particle_path.as_posix(), rp_id)
    )
    file_pk = cursor.lastrowid
    try:
        particle_walker = load_jsonc(particle_path)
    except json.JSONDecodeError:
        # sinlently skip invalid files. The file is in db but has no data
        return
    description = particle_walker / "particle_effect" / "description"
    basic_render_parameters = description / "basic_render_parameters"

    identifier = description / "identifier"
    material = basic_render_parameters / "material"
    texture = basic_render_parameters / "texture"

    identifier_data = identifier.data
    if not isinstance(identifier_data, str):
        return
    material_data = material.data
    if not isinstance(material.data, str):
        material_data = None
    texture_data = texture.data
    if not isinstance(texture.data, str):
        texture_data = None
    cursor.execute(
        '''
        INSERT INTO Particle (
            identifier, material, texture, ParticleFile_fk
        ) VALUES (?, ?, ?, ?)
        ''',
        (identifier_data, material_data, texture_data, file_pk)
    )
