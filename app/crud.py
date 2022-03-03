from sqlalchemy.orm import Session
from sqlalchemy import func, or_, exc
from fastapi.encoders import jsonable_encoder
from . import model, schema

# -- Demographic Profile --#

def get_demo_profiles(db: Session):
    return db.query(model.Demo_profile).all()


def get_demo_profile(db: Session, sisid: int):
    return db.query(model.Demo_profile).filter(
        model.Demo_profile.sisid == sisid
    ).all()

def get_demo_profile_count(db: Session, sisid: int):
    return db.query(model.Demo_profile).filter(
        model.Demo_profile.sisid == sisid
    ).count()
    

def create_demo_profile(db: Session, demo_profile: schema.Demo_profile):   
    db_profile = model.Demo_profile(**demo_profile.dict())                                  
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_demo_profile(db: Session, demo_profile: schema.Demo_profile): 
    existing_demo_profile = db.query(model.Demo_profile).filter(model.Demo_profile.sisid == demo_profile.sisid).first()
    if existing_demo_profile:
        db.query(model.Demo_profile).filter(model.Demo_profile.sisid == existing_demo_profile.sisid).update(demo_profile.dict())
        db.commit()
        return existing_demo_profile
    else:
        return 404

def delete_demo_profile(db: Session, sisid: int): 
    existing_demo_profile = db.query(model.Demo_profile).filter(model.Demo_profile.sisid == sisid).first()
    if existing_demo_profile:
        existing_demo_profile = db.query(model.Demo_profile).filter(model.Demo_profile.sisid == sisid).delete()
        db.commit()
        return existing_demo_profile
    else:
        return 404

