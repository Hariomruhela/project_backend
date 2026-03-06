from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from utils.cloudinary import upload_image
import models, schemas
from database import get_db
from dependencies import get_current_user, get_current_admin
from utils.cloudinary import upload_image
from fastapi import Query

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


# -------------------------
# Create Project (Admin Only)
# -------------------------
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(
    title: str = Form(...),
    description: str = Form(...),
    techstack: List[str] = Form(...),
    live_link: Optional[str] = Form(None),
    is_visible: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    image_url = None

    # ✅ Only upload if image exists
    if image:
        image_url = upload_image(image)


    project = models.Project(
        title=title,
        description=description,
        image_url=image_url,
        techstack=",".join(techstack),
        live_link=live_link,
        is_visible=is_visible,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    project.techstack = project.techstack.split(",")

    return project


# -------------------------
# Get All Projects
# -------------------------
@router.get("/", response_model=List[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    if current_user.is_admin:
        projects = db.query(models.Project).all()
    else:
        projects = db.query(models.Project).filter(models.Project.is_visible == True).all()

    for project in projects:
        project.techstack = project.techstack.split(",")

    return projects


# -------------------------
# Get Project By ID
# -------------------------
@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.is_visible and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")

    project.techstack = project.techstack.split(",")

    return project


# -------------------------
# Update Project (Admin Only)
# -------------------------
@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    techstack: Optional[str] = Form(None),
    live_link: Optional[str] = Form(None),
    is_visible: Optional[bool] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if title:
        project.title = title

    if description:
        project.description = description

    if techstack:
        project.techstack = techstack

    if live_link:
        project.live_link = live_link

    if is_visible is not None:
        project.is_visible = is_visible

    # ✅ Upload image to Cloudinary
    if image:
        image_url = upload_image(image)
        project.image_url = image_url

    db.commit()
    db.refresh(project)

    if project.techstack:
        project.techstack = project.techstack.split(",")

    return project


# -------------------------
# Delete Project (Admin Only)
# -------------------------
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}


# -------------------------
# Toggle Visibility (Admin Only)
# -------------------------
@router.patch("/{project_id}/visibility")
def update_visibility(
    project_id: int,
    is_visible: bool = Query(...),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.is_visible = is_visible
    db.commit()
    db.refresh(project)

    return {"message": "Visibility updated successfully"}