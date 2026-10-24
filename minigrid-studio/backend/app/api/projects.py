from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Membership, Project, ProjectMember
from ..schemas import ProjectIn, ProjectOut, ProjectPatch
from ..security import Caller, current_caller, project_for
from ..services import audit

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    if not caller.roles:
        return []
    rows = db.scalars(select(Project).where(Project.org_id.in_(list(caller.roles))).order_by(Project.created_at)).all()
    out = []
    for p in rows:
        try:
            project_for(db, caller, p.id)
            out.append(p)
        except HTTPException:
            continue
    return out


@router.post("", response_model=ProjectOut, status_code=201)
def create_project(body: ProjectIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    caller.require(body.org_id, "edit")
    p = Project(org_id=body.org_id, name=body.name, country=body.country, description=body.description,
                restricted=body.restricted, created_by=caller.user.id)
    db.add(p)
    db.flush()
    if p.restricted:
        db.add(ProjectMember(project_id=p.id, user_id=caller.user.id))
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="project.create", entity_type="project",
                 entity_id=p.id, payload=body.model_dump())
    return p


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    return project_for(db, caller, project_id)[0]


@router.patch("/{project_id}", response_model=ProjectOut)
def patch_project(project_id: str, body: ProjectPatch, caller: Caller = Depends(current_caller),
                  db: Session = Depends(get_db)):
    changes = body.model_dump(exclude_none=True)
    # visibility and archiving are governance decisions: admins only
    p, _ = project_for(db, caller, project_id,
                       "manage" if {"restricted", "archived"} & set(changes) else "edit")
    for k, v in changes.items():
        setattr(p, k, v)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="project.update", entity_type="project",
                 entity_id=p.id, payload=changes)
    return p


@router.post("/{project_id}/members/{user_id}", status_code=204)
def add_project_member(project_id: str, user_id: str, caller: Caller = Depends(current_caller),
                       db: Session = Depends(get_db)):
    p, _ = project_for(db, caller, project_id, "manage")
    if not db.scalar(select(Membership).where(Membership.user_id == user_id, Membership.org_id == p.org_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user is not a member of this organisation")
    if not db.scalar(select(ProjectMember).where(ProjectMember.project_id == p.id, ProjectMember.user_id == user_id)):
        db.add(ProjectMember(project_id=p.id, user_id=user_id))
        audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="project.member.add",
                     entity_type="project", entity_id=p.id, payload={"user_id": user_id})


@router.delete("/{project_id}/members/{user_id}", status_code=204)
def remove_project_member(project_id: str, user_id: str, caller: Caller = Depends(current_caller),
                          db: Session = Depends(get_db)):
    p, _ = project_for(db, caller, project_id, "manage")
    pm = db.scalar(select(ProjectMember).where(ProjectMember.project_id == p.id, ProjectMember.user_id == user_id))
    if pm is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    db.delete(pm)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="project.member.remove",
                 entity_type="project", entity_id=p.id, payload={"user_id": user_id})
