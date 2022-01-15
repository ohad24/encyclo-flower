from pydantic import BaseModel, FileUrl
from typing import List
from enum import Enum


class WhatInImage(Enum, str):
    a = "הצמח במלואו"
    b = "פרי"
    c = "פרח"
    d = "עלים"
    e = "זרעים"
    f = "הצמח בבית הגידול"
    g = "לא נבחר"


class QuestionImage(BaseModel):
    file_name: str
    url: FileUrl
    description: str | None = None
    notes: str | None = None
    what_in_image: WhatInImage


class Question(BaseModel):
    question_text: str
    images: List[str]
