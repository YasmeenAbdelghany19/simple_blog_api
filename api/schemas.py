import os
from dotenv import load_dotenv
import motor.motor_asyncio
from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from pydantic_core import SchemaSerializer, core_schema
from pydantic import GetCoreSchemaHandler


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.blog_api

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        # Create a core schema that validates and serializes ObjectId as a string
        schema = core_schema.no_info_after_validator_function(
            cls.validate,
            handler(core_schema.str_schema()),  # Use str_schema instead of set
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda obj: str(obj),  # Serialize ObjectId to string
                info_arg=False,
                return_schema=core_schema.str_schema(),  # Expect string schema
            )
        )
        cls.__pydantic_serializer__ = SchemaSerializer(schema)  # Assign serializer
        return schema    
        
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "secret_code"
            }
        }
        
class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com"
            }
        }
        
class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    body: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "blog title",
                "body": "blog content"
            }
        }

class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    body: str = Field(...)
    auther_name: str = Field(...)
    auther_id: str = Field(...)
    created_at: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "blog title",
                "body": "blog content",
                "auther_name": "name of the auther",
                "auther_id": "ID of the auther",
                "created_at": "Date of blog creation"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(...)

class PasswordReset(BaseModel):
    password: str = Field(...)