# pylint: disable=no-member, multiple-statements, missing-module-docstring, missing-class-docstring
from typing import cast
from sqlite3 import Connection
from pathlib import Path
import json
from .better_json_tools import load_jsonc
from ._views import dbtableview

@dbtableview(
    properties={
        "path": (Path, "NOT NULL")
    },
    connects_to=["ResourcePack"]
)
class RpAnimationControllerFile: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL")
    },
    connects_to=["RpAnimationControllerFile"]
)
class RpAnimationController: ...

@dbtableview(
    properties={
        "shortName": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL")
    },
    connects_to=["RpAnimationController"]
)
class RpAnimationControllerParticleEffect: ...

@dbtableview(
    properties={
        "shortName": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL")
    },
    connects_to=["RpAnimationController"]
)
class RpAnimationControllerSoundEffect: ...

RP_ANIMATION_CONTROLLER_BUILD_SCRIPT: str = (
    RpAnimationControllerFile.build_script +
    RpAnimationController.build_script +
    RpAnimationControllerParticleEffect.build_script +
    RpAnimationControllerSoundEffect.build_script
)

def load_rp_animation_controllers(db: Connection, rp_id: int):
    '''
    Loads all animation controllers from the resource pack.
    '''
    rp_path: Path = db.execute(
        "SELECT path FROM ResourcePack WHERE ResourcePack_pk = ?",
        (rp_id,)
    ).fetchone()[0]

    for ac_path in (rp_path / "animation_controllers").rglob("*.json"):
        load_rp_animation_controller(db, ac_path, rp_id)


def load_rp_animation_controller(db: Connection, animation_controller_path: Path, rp_id: int):
    '''
    Loads an animation controller from the resource pack.
    '''
    cursor = db.cursor()
    # RP ANIMATION FILE
    cursor.execute(
        "INSERT INTO RpAnimationControllerFile (path, ResourcePack_fk) VALUES (?, ?)",
        (animation_controller_path.as_posix(), rp_id)
    )
    file_pk = cursor.lastrowid
    try:
        acs_walker = load_jsonc(animation_controller_path)
    except json.JSONDecodeError:
        # sinlently skip invalid files. The file is in db but has no data
        return

    for ac_walker in acs_walker / "animation_controllers" // str:
        identifier_data: str = cast(str, ac_walker.parent_key)
        if not identifier_data.startswith("controller.animation."):
            continue
        cursor.execute(
            '''
            INSERT INTO RpAnimationController (
                RpAnimationControllerFile_fk, identifier, jsonPath
            ) VALUES (?, ?, ?)
            ''',
            (file_pk, identifier_data, ac_walker.path_str)
        )
        rpanim_pk = cursor.lastrowid

        states = ac_walker / "states" // str
        # LOAD PARTICLE EFFECTS
        for particle_effect_walker in states / "particle_effects" // int:
            short_name = particle_effect_walker / "effect"
            if not isinstance(short_name.data, str):
                continue
            cursor.execute(
                '''
                INSERT INTO RpAnimationControllerParticleEffect (
                    RpAnimationController_fk, shortName, jsonPath
                ) VALUES (?, ?, ?)
                ''',
                (rpanim_pk, short_name.data, particle_effect_walker.path_str)
            )
        # LOAD SOUND EFFECTS
        for sound_effect_walker in states / "sound_effects" // int:
            short_name = sound_effect_walker / "effect"
            if not isinstance(short_name.data, str):
                continue
            cursor.execute(
                '''
                INSERT INTO RpAnimationControllerSoundEffect (
                    RpAnimationController_fk, shortName, jsonPath
                ) VALUES (?, ?, ?)
                ''',
                (rpanim_pk, short_name.data, sound_effect_walker.path_str)
            )
