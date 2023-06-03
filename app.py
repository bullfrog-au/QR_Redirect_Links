from fastapi import FastAPI, Depends, Request, status, HTTPException

from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
templates = Jinja2Templates(directory= os.path.join(BASE_DIR,"templates"))

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def landing(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/item")
def home(request: Request, db: Session = Depends(get_db), id: int = 0):
    if id:
        records = db.query(models.records).filter(
            models.records.id == id).first()
        if records != None:
            return templates.TemplateResponse("default.html",
                                              {"request": request, "qr": records})
        else:
            return templates.TemplateResponse("not_found.html", {"request": request})
    else:
        return templates.TemplateResponse("home.html", {"request": request})


@app.post("/add", status_code=status.HTTP_201_CREATED)
def add(request: Request, db: Session = Depends(get_db), id: int = 0, name: str = None, status: str = None, link: str = None):
    if id and name and status and link:
        try:
            db.add(models.records(id=id, name=name, status=status, link=link))
            db.commit()
            return {"id": id, "name": name, "status": status, "link": link}
        except:
            raise HTTPException(status_code=400, detail="Unable to add record")
    else:
        raise HTTPException(status_code=400, detail="Error in parameters")


@app.patch("/update/{id}")
def update(id, db: Session = Depends(get_db), name: str = None, status: str = None, link: str = None):
    try:
        record = db.query(models.records).filter(
            models.records.id == id).first()
        record.name = name
        record.status = status
        record.link = link
        db.commit()
        return {"id": id, "name": name, "status": status, "link": link}
    except:
        raise HTTPException(status_code=400, detail="Unable to update record")


@app.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    print("Got here")
    try:
        record = db.query(models.records).filter(
            models.records.id == id).first()
        db.delete(record)
        db.commit()
        return {"message": "Record deleted successfully"}
    except:
        raise HTTPException(status_code=400, detail="Unable to delete record")
