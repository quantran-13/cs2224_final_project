import logging

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.const.global_map import RESOURCE_MAP
from src.const import const_map as CONST_MAP
from src.api_endpoint.add_api import api_log_aischema
from src.utils.basemodel import app_schemas as schemas
from src.utils.basemodel.response_schemas import create_response, ResponseModel
from src.encode_image import encode_image_func
from src.search_image import search_image_func, search_image_func_return_image


app_logger = logging.getLogger("app_logger")
utils_logger = logging.getLogger("utils_logger")
error_logger = logging.getLogger("error_logger")


app = RESOURCE_MAP["fastapi_app"]
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/encode_image", response_model=ResponseModel)
@api_log_aischema
async def encode_image(input_map: schemas.EncodeImageSchema) -> ResponseModel:
    base64_images = input_map.base64_images
    utils_logger.info(
        f"Number of image requests in {input_map.session}: {len(base64_images)}"
    )

    result = []
    for base64_image in base64_images:
        image_features = encode_image_func(base64_image=base64_image)
        result.append({"image_features": image_features})

    utils_logger.debug(f"=" * 10)
    return create_response(status_code=200, content=result)


@app.post("/v1/search", response_model=ResponseModel)
@api_log_aischema
async def search(input_map: schemas.SearchImageSchema) -> ResponseModel:
    base64_images = input_map.base64_images
    utils_logger.info(
        f"Number of image requests in {input_map.session}: {len(base64_images)}"
    )

    index_name = input_map.index_name
    if index_name not in CONST_MAP.indexes:
        error_logger.error(f"index {index_name} is unknown.")
        return create_response(
            status_code=500, content=f"index {index_name} is unknown."
        )

    result = []
    for base64_image in base64_images:
        dists, ids = search_image_func(
            base64_image=base64_image,
            index_name=input_map.index_name,
            top_results=input_map.top_results,
        )
        result.append({"ids": ids, "dists": dists})

    utils_logger.debug(f"=" * 10)
    return create_response(status_code=200, content=result)


@app.post("/v2/search", response_model=ResponseModel)
@api_log_aischema
async def search(input_map: schemas.SearchImageSchemaV2) -> ResponseModel:
    base64_image = input_map.base64_image
    utils_logger.info(
        f"Number of image requests in {input_map.session}: {len(base64_image)}"
    )

    index_name = input_map.index_name
    if index_name not in CONST_MAP.indexes:
        error_logger.error(f"index {index_name} is unknown.")
        return create_response(
            status_code=500, content=f"index {index_name} is unknown."
        )

    result = search_image_func_return_image(
        base64_image=base64_image,
        index_name=input_map.index_name,
        top_results=input_map.top_results,
    )
    utils_logger.debug(f"=" * 10)
    return create_response(status_code=200, content=result)
