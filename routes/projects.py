from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated  # Added Annotated
from pydantic import WithJsonSchema           # Added WithJsonSchema
import json
import models, schemas
from database import get_db
from dependencies import get_current_user, get_current_admin
from utils.cloudinary import upload_image

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)

# 💡 Workaround for FastAPI Swagger UI multi-file picker bug
SwaggerUploadFile = Annotated[UploadFile, WithJsonSchema({"type": "string", "format": "binary"})]


# -------------------------
# Create Project (Admin Only)
# -------------------------
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(
    title: str = Form(...),
    description: str = Form(...),
    techstack: List[str] = Form(...),
    category: Optional[str] = Form(None),
    live_link: Optional[str] = Form(None),
    is_visible: bool = Form(True),
    images: List[SwaggerUploadFile] = File(...),  # ✅ Uses the Swagger-friendly type
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    image_urls = []

    for image in images:
        image_urls.append(upload_image(image))

    project = models.Project(
        title=title,
        description=description,
        image_urls=",".join(image_urls),
        techstack=",".join(techstack),
        category=category,
        live_link=live_link,
        is_visible=is_visible,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    project.techstack = project.techstack.split(",")
    project.image_urls = (
        project.image_urls.split(",")
        if project.image_urls
        else []
    )

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
        projects = db.query(models.Project)\
        .order_by(models.Project.updated_at.desc())\
        .all()
    else:
        projects = db.query(models.Project)\
            .filter(models.Project.is_visible == True)\
            .order_by(models.Project.updated_at.desc())\
            .all()

    for project in projects:
        project.techstack = (
            project.techstack.split(",")
            if project.techstack
            else []
        )

        project.image_urls = (
            project.image_urls.split(",")
            if project.image_urls
            else []
        )

    return projects

# -------------------------
# Public view visible projects
# -------------------------
@router.get("/public", response_model=List[schemas.ProjectResponse])
def get_public_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project)\
        .filter(models.Project.is_visible == True)\
        .order_by(models.Project.updated_at.desc())\
        .all()

    for project in projects:
        project.techstack = (
            project.techstack.split(",")
            if project.techstack
            else []
        )

        project.image_urls = (
            project.image_urls.split(",")
            if project.image_urls
            else []
        )

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

    project.techstack = (
        project.techstack.split(",")
        if project.techstack
        else []
    )

    project.image_urls = (
        project.image_urls.split(",")
        if project.image_urls
        else []
    )

    return project


# -------------------------
# Update Project (Admin Only)
# -------------------------
@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    techstack: List[str] = Form([]),
    category: Optional[str] = Form(None),
    live_link: Optional[str] = Form(None),
    is_visible: Optional[bool] = Form(None),
    existing_images: Optional[str] = Form(None),
    images: List[SwaggerUploadFile] = File([]),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if title is not None:
        project.title = title

    if description is not None:
        project.description = description

    if techstack:
        project.techstack = ",".join(techstack)

    if category is not None:
        project.category = category

    if live_link is not None:
        project.live_link = live_link

    if is_visible is not None:
        project.is_visible = is_visible

    # Final images after update
    final_images = []

    # Keep only the images sent by the frontend
    if existing_images:
        final_images = json.loads(existing_images)

    # Upload newly selected images
    for image in images:
        url = upload_image(image)
        final_images.append(url)

    project.image_urls = ",".join(final_images)

    db.commit()
    db.refresh(project)

    project.techstack = (
        project.techstack.split(",")
        if project.techstack
        else []
    )

    project.image_urls = (
        project.image_urls.split(",")
        if project.image_urls
        else []
    )

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