import os, secrets, requests, json
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Response, status, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_503_SERVICE_UNAVAILABLE

from sqlalchemy.orm import Session 
from sqlalchemy import MetaData, inspect
from sqlalchemy.sql import func

from app import model, schema, crud
from app.database import SessionLocal, engine

from dotenv import load_dotenv, find_dotenv

app = FastAPI()

#security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def start(
        db:   Session = Depends(get_db)
    ):
    print("Starting up...")
    inspector = inspect(engine)
    """
    # check if we created the tables in the database already. If not, create and populate them
    if not inspector.has_table('customer'):
        print("Creating the tables in the database")
        model.LoyaltyLevel.metadata.create_all(engine)
        model.Customer.metadata.create_all(engine)
        model.Purchase.metadata.create_all(engine)

        #populate the tables with test data
        print("Populating the tables in the database")
        session = Session(engine)
        loyalty_level_instance_1 = model.LoyaltyLevel(level_id="pl", description='Platinum', discount=25)
        loyalty_level_instance_2 = model.LoyaltyLevel(level_id="gl", description='Gold', discount=15)
        session.add_all([loyalty_level_instance_1, loyalty_level_instance_2])
        
        customer_instance = model.Customer(firstname='John', lastname='Doe', date_of_birth=func.now(), level_id=loyalty_level_instance_1.level_id,  signup_date=func.now())
        purchase_instance = model.Purchase(customer = customer_instance, purchase_name="something")
        session.add_all([purchase_instance])
        session.commit()
    else:   
        print("Found the database tables")
    """
@app.on_event("shutdown")
async def shutdown(db:   Session = Depends(get_db)):
        print("Shutting down...")
    
       # print("Dropping tables")
       # model.LoyaltyLevel.metadata.drop_all(engine)
       # model.Customer.metadata.drop_all(engine)
       # model.Purchase.metadata.drop_all(engine)
       # print("Tables dropped") 
           
    
# # authentication piece (we don't use it in this example)
# def is_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "someusername")
#     correct_password = secrets.compare_digest(credentials.password, "somepassword")
#     if not (correct_username and correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect login credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return True


@app.get("/")
def read_root():
    return {"Hello": "World"}

# -- Demographic Profile --#
@app.get(
    "/demographicProfiles",
    tags=["Demographic Profiles"],
    response_model=List[schema.Demo_profile],
    summary="Gets all Demographic Profile",
    response_description="A list containing all the demographic profile details"
)
def get_demo_profiles(
        db:   Session = Depends(get_db)
        #,auth: bool    = Depends(is_authenticated)
    ):
    return crud.get_demo_profiles(db)


@app.get(
    "/demographicProfile/{sisid}",
    tags=["Demographic Profile"], 
    response_model=List[schema.Demo_profile],
    summary="Gets a single Demograhic profile based on SIS ID",
    response_description="A single Demographic profile based on the SIS ID",
    responses={404: {"model": None, "description": "SIS ID not found"}}
)
def get_demo_profile(sisid: str = Path(
                                        ...,
                                        title="Demo profile SIS ID",
                                        description="Unique Student ID indetifier",
                                        max_length=15
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):

    result = crud.get_demo_profile(db, sisid)

    if not result:
        return Response(
            'Student ID not found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return result

@app.post("/demographicProfile/", 
        tags=["Demographic Profile"], 
        response_model=schema.Demo_profile, 
        summary="Create a demographic profile",
        response_description="Newly created demographic profile",
        status_code = status.HTTP_201_CREATED
        )
def create_demo_profile(demo_profile: schema.Demo_profile,
                    db:   Session = Depends(get_db), 
                    #,auth: bool    = Depends(is_authenticated)
                    ):
        
    result = crud.create_demo_profile(db, demo_profile)
    return result

@app.put("/demographicProfile/", 
        tags=["Demographic Profile"],
        response_model=schema.Demo_profile, 
        summary="Update a single Demographic Profile",
        response_description="Updated Demographic Profile",
        status_code = status.HTTP_200_OK
        )
def update_demo_profile(demo_profile: schema.Demo_profile,
                    db:   Session = Depends(get_db),
                    #,auth: bool    = Depends(is_authenticated)
                    ):
    # if not crud.get_loyalty_level_count(db, loyalty_level.level_id) > 0:
    #     raise HTTPException(status_code=404, detail=str(loyalty_level.level_id) + " is not a valid loyalty level.")

    result = crud.update_demo_profile(db, demo_profile)    
    if isinstance(result, model.Demo_profile):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a Student ID with key (SISID=" + str(demo_profile.sisid) + ")",
                headers={"X-Error": "Some error goes here"},
            )
            

@app.delete("/demographicProfile/{sisid}", 
        tags=["Demographic Profile"],
        response_model=schema.Demo_profile, 
        summary="Delete a single Demographic profile based sisid",
        response_description="Deleted demographic profile",
        status_code = status.HTTP_200_OK
        )
def delete_demo_profile(sisid: str = Path(
                                        ...,
                                        title="Demo Profile SIS ID",
                                        description="Unique Student ID indetifier",
                                        max_length=9
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    
    
    result = crud.delete_demo_profile(db, sisid)
    if isinstance(result, model.Demo_profile):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a demographic profile with key (sisid=" + str(sisid) + ")",
                headers={"X-Error": "Some error goes here"},
            )
