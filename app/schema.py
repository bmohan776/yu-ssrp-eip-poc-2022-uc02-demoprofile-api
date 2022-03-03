from ast import LtE, Num
from typing import List, Optional
from unicodedata import numeric
from fastapi import Query
from pydantic import BaseModel
from datetime import date


class Demo_profile(BaseModel):
    sisid: int = Query(                                         
        ...,                                                                    
        title="SIS ID",                                                    
        description="The SISID of the customer",                                 
        gt=0,

    )
    firstname: Optional[str] = Query(
        None,
        title="Student's first name",
        description="The first name of the Student",
        max_length=225,
    )
    surname: Optional[str] = Query(
        None,
        title="Student's last name",
        description="The last name of the Student",
        max_length=100,
    )
    
    gender: str = Query(
        ...,
        title="Gender",
        description="Gender Title",
        max_length=1
    )    
    birthdate: Optional[date] = Query(
        None,
        title="Date of birth",
        description="Student's date of birth",
    )

    email: str = Query(
        None,
        title="Email",
        description="Student's email",
    )
        
    class Config:
        orm_mode = True









