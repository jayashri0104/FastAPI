

from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Contact(BaseModel):
    id: int 
    name: str
    phone: Union[str, None] = None
    


contacts_db = []
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Contact CRUD App!"}



@app.post("/contacts/", response_model=Contact)
def create_contact(contact: Contact):
    global next_id
    contact.id = next_id
    next_id += 1
    contacts_db.append(contact)
    return contact



@app.get("/contacts/", response_model=List[Contact])
def get_contacts():
    return contacts_db



@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    for contact in contacts_db:
        if contact.id == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")



@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, updated_contact: Contact):
    for index, contact in enumerate(contacts_db):
        if contact.id == contact_id:
            updated_contact.id = contact_id
            contacts_db[index] = updated_contact
            return updated_contact
    raise HTTPException(status_code=404, detail="Contact not found")



@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    for index, contact in enumerate(contacts_db):
        if contact.id == contact_id:
            contacts_db.pop(index)
            return {"message": "Contact deleted successfully"}
    raise HTTPException(status_code=404, detail="Contact not found")