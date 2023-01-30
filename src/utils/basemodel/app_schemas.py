from pydantic import BaseModel


class EncodeImageSchema(BaseModel):
    session: str
    base64_images: list[str]


class SearchImageSchema(BaseModel):
    session: str
    base64_images: list[str]
    index_name: str = "oxford5k_clip"
    top_results: int = 50


class SearchImageSchemaV2(BaseModel):
    session: str
    base64_image: str
    index_name: str = "oxford5k_clip"
    top_results: int = 50
