import os
from typing import Literal, TypedDict, List, Optional

import boto3
import hashlib
from botocore.client import Config
from botocore.exceptions import ClientError

from rov_db_access.authentication.models import User, Organization
from rov_db_access.utils.geoserver_utils import GeoServerClient
from rov_db_access.utils.s3_utils import S3Client
from rov_db_access.utils.utils import wkbelement_to_wkt
from rov_db_access.config.db_utils import init_db_engine
from rov_db_access.config.settings import Settings
from rov_db_access.sentinel.worker import is_valid_uuid
from rov_db_access.gis.models import Process, Image, InferenceModel, Input, ResultsRaster, Run, ResultsRaw, Mosaic
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

settings = Settings()

CreateProcessDict = TypedDict("CreateProcessDict", {
    "name": str,
    "inference_model_id": int,
    "area": float,
    "cost_estimated": float,
    "images": List[dict],
    "geom": str,
    "mask": Optional[str]
})

CreateTaskingDict = TypedDict("CreateTaskingDict", {
    "name": str,
    "inference_model_id": int,
    "area": float,
    "cost_estimated": float,
    "tasking_config": dict,
    "geom": str,
    "mask": Optional[str]
})

UploadImageDict = TypedDict("UploadImageDict", {
    "name": str,
    "url": str,
    "bbox": str
})


def get_upload_s3_url():
    region = settings.gis_inference_region
    bucket_name = settings.gis_inference_bucket
    access_key_id = settings.aws_key
    secret_access_key = settings.aws_secret

    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=Config(signature_version='s3v4', region_name=region)
    )

    # Generate a unique image name
    raw_bytes = os.urandom(16)
    image_name = hashlib.sha256(raw_bytes).hexdigest()
    object_key = image_name + ".tif"

    params = {
        "Bucket": bucket_name,
        "Key": object_key,
    }

    try:
        upload_url = s3.generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=60
        )
        return {"upload_url": upload_url, "object_key": object_key}

    except ClientError as e:
        return None


def get_date(obj):
    return tuple(map(int, obj["date"].split("/")[::-1]))


class GisWorker:

    def __init__(self) -> None:
        self.engine = init_db_engine(
            settings.db_rov_gis_user,
            settings.db_rov_gis_password,
            settings.db_rov_gis_host,
            settings.db_rov_gis_port,
            settings.db_rov_gis_database
        )

    def add_mosaic_result(self, raster_result_id: str, mosaic_id: str, user: User):
        with Session(self.engine) as session:
            mosaic_query = (
                select(Mosaic)
                .where(Mosaic.id == mosaic_id)
                .limit(1)
            )
            mosaic = session.scalar(mosaic_query)
            if mosaic is None:
                print(f'No Raster with id ${raster_result_id} found!')
                return None
            if mosaic.organization_id != user.organization_id:
                print(f'This mosaic is not from this org_id: {user.organization_id}')
                return None

            raster_result_query = (
                select(ResultsRaster)
                .where(ResultsRaster.id == raster_result_id)
                .limit(1)
            )
            raster_result = session.scalar(raster_result_query)
            if raster_result is None:
                print(f'No Raster with id ${raster_result_id} found!')
                return None

            org_query = (
                select(Organization.workspace)
                .where(Organization.id == user.organization_id)
                .limit(1)
            )
            workspace = session.scalar(org_query)

            s3 = S3Client(settings.run_results_bucket, settings.s3_region)
            granule_path = s3.get_file_url(key=raster_result.url)


            geoserver_client = GeoServerClient()
            print("BORRAR: url", geoserver_client.url)
            print("BORRAR: server url", geoserver_client.server_url)
            print("BORRAR: workspace", workspace
                  )
            geoserver_client.set_workspace(workspace)

            print("BORRAR: coverage_store", mosaic.coverage_store)
            print("BORRAR: granule_path", granule_path)

            result = geoserver_client.add_mosaic_granule(mosaic.coverage_store, granule_path)
            if result is None:
                return False
            return True

    def remove_mosaic_result(self, raster_result_id: str, mosaic_id: str, user: User):
        # TODO: get Fid of the geoserver table and remove granule
        return False

    def copy_process(self, process_id, user: User):
        with Session(self.engine) as session:
            query = (
                select(Process)
                .where(Process.id == process_id)
                .limit(1)
            )
            process_to_copy = session.scalar(query)
            if process_to_copy is None:
                print(f'No process with id ${id} found!')
                return {}
            elif process_to_copy.organization_id != user.organization_id:
                print(f'This process is not from this org_id: {user.organization_id}')
                return None
            else:
                process_type = process_to_copy.type
                new_name = "Copy of " + process_to_copy.name
                model_id: int = process_to_copy.inference_model_id
                area: float = process_to_copy.area
                cost_estimated: float = process_to_copy.cost_estimated
                data: dict = process_to_copy.data
                geom: str = wkbelement_to_wkt(process_to_copy.geom)
                mask = wkbelement_to_wkt(process_to_copy.mask)
                print(f'Process with id: {process_to_copy.id} found! type: {process_type}')

                if process_type == 'on demand':
                    images = []
                    img_ids = []
                    for run in process_to_copy.runs:
                        if run.input is None:
                            print(f'Process with corrupted Run {run.id} without Input data')
                            return False
                        input_type = run.input.type
                        if input_type == 'upload':
                            images.append(run.input.data)
                        elif input_type == 'change':
                            t1 = run.input.data.get("t1")
                            t1["type"] = 'sentinel'
                            t2 = run.input.data.get("t2")
                            t2["type"] = 'sentinel'
                            if t1.get("id") not in img_ids:
                                images.append(t1)
                                img_ids.append(t1.get("id"))
                            if t2.get("id") not in img_ids:
                                images.append(t2)
                                img_ids.append(t2.get("id"))
                        else:
                            print(f'Process with corrupted Input data type: {input_type}')
                            return False
                    print(f'Images to create as input & runs for process on demand id: {process_id}')
                    data: CreateProcessDict = {
                        "name": new_name,
                        "inference_model_id": model_id,
                        "area": area,
                        "cost_estimated": cost_estimated,
                        "images": images,
                        "geom": geom,
                        "mask": mask
                    }
                    return self.create_process(data, user)
                elif process_type == 'tasking':
                    data: CreateTaskingDict = {
                        "name": new_name,
                        "inference_model_id": model_id,
                        "area": area,
                        "cost_estimated": cost_estimated,
                        "tasking_config": data,
                        "geom": geom,
                        "mask": mask
                    }
                    return self.create_tasking(data, user)
                else:
                    return False

    def create_process(self, data: CreateProcessDict, user: User):
        name = data["name"]
        inference_model_id = data["inference_model_id"]
        area = data["area"]
        cost_estimated = data["cost_estimated"]
        images = data["images"]
        geom = data["geom"]
        mask = data["mask"]
        user_id = user.id
        organization_id = user.organization_id

        print(f'Creating process for user_id: {user_id}')

        with Session(self.engine) as session:
            # Check if inference_model_id exists
            model_query = (
                select(InferenceModel.id)
                .where(InferenceModel.id == inference_model_id)
                .limit(1)
            )
            model = session.scalar(model_query)
            if model is None:
                return False

            input_images = {
                "sentinel": [],
                "upload": []
            }
            unsorted_sentinel = []
            for img in images:
                img_type = img.get("type")
                if img_type == "sentinel":
                    data = {
                        "id": img.get("id"),
                        "date": img.get("date"),
                        "title": img.get("title")
                    }
                    unsorted_sentinel.append(data)
                elif img_type == "upload":
                    input_images["upload"].append(img.get("id"))

            input_images["sentinel"] = sorted(unsorted_sentinel, key=get_date)

            print(f'Create process validation on images: {input_images}')
            if len(input_images["upload"]) > 0:
                # Check upload image exists
                img_query_count = session.scalar(
                    select(func.count(Image.id))
                    .where(
                        (Image.id.in_(input_images["upload"])) &
                        (Image.organization_id == organization_id)
                    )
                )
                if img_query_count != len(input_images["upload"]):
                    print(f'Create process validation failed! An Upload image is not valid')
                    return False

            if len(input_images["sentinel"]) > 0:
                # Check format of sentinel uuid
                for data in input_images["sentinel"]:
                    if not is_valid_uuid(data["id"]):
                        print(f'Create process validation failed! A Sentinel image is not valid')
                        return False

            print(f'Create process validation ready!. Adding to DB...')
            process = Process(
                name=name,
                cost_estimated=cost_estimated,
                area=area,
                type='on demand',
                inference_model_id=inference_model_id,
                organization_id=organization_id,
                geom=geom,
                mask=mask,
                user_id=user_id
            )

            # if model is change detector with sentinel, then different process creation with multiple runs
            if inference_model_id == 1:
                if len(input_images["sentinel"]) < 2:
                    print("ERROR Create change detector process. Not enough sentinel images:")
                    return False
                for i in range(len(input_images["sentinel"]) - 1):
                    new_input = Input(
                        type='change',
                        data={
                            "t1": input_images["sentinel"][i],
                            "t2": input_images["sentinel"][i+1]
                        },
                        user_id=user_id,
                        organization_id=organization_id
                    )
                    session.add(new_input)
                    new_run = Run(
                        input=new_input,
                        inference_model_id=inference_model_id,
                        process=process
                    )
                    session.add(new_run)
                session.add(process)
                try:
                    session.commit()
                    return True
                except Exception as error:
                    print("ERROR Create change detector process. An exception occurred during DB insertion:", error)
                    return False
            else:
                for img in images:
                    new_input = Input(
                        type=img.get("type"),
                        data=img,
                        user_id=user_id,
                        organization_id=organization_id
                    )
                    session.add(new_input)
                    new_run = Run(
                        input=new_input,
                        inference_model_id=inference_model_id,
                        process=process
                    )
                    session.add(new_run)
                session.add(process)
                try:
                    session.commit()
                    return True
                except Exception as error:
                    print("ERROR Create process. An exception occurred during DB insertion:", error)
                    return False

    def create_tasking(self, data: CreateTaskingDict, user: User):
        name = data["name"]
        inference_model_id = data["inference_model_id"]
        area = data["area"]
        cost_estimated = data["cost_estimated"]
        tasking_config = data["tasking_config"]
        user_id = user.id
        geom = data["geom"]
        mask = data["mask"]
        organization_id = user.organization_id

        print(f'Creating tasking for user_id: {user_id}')

        # Check if inference_model_id exists
        with Session(self.engine) as session:
            model_query = (
                select(InferenceModel.id)
                .where(InferenceModel.id == inference_model_id)
                .limit(1)
            )
            model = session.scalar(model_query)
            if model is None:
                return False

            process = Process(
                name=name,
                cost_estimated=cost_estimated,
                area=area,
                inference_model_id=inference_model_id,
                data=tasking_config,
                organization_id=organization_id,
                type='tasking',
                geom=geom,
                mask=mask,
                user_id=user_id
            )

            session.add(process)
            try:
                session.commit()
                return True
            except Exception as error:
                # handle the exception
                print("Create tasking. An exception occurred during DB insertion:", error)
                return False

    def get_inference_models(self):
        with Session(self.engine) as session:
            query = (
                select(InferenceModel)
                .order_by(InferenceModel.id)
            )
            models = session.execute(query).all()
            if models is None:
                return {}
            result = []
            for model in models:
                model = model[0]
                result.append({
                    "id": model.id,
                    "name": model.name,
                    "title": model.title,
                    "description": model.description,
                    "img_url": model.img_url,
                    "price": model.price,
                    "min_resolution": model.min_resolution,
                    "config": model.config
                })
            return result

    def get_inference_model_by_id(self, id: str):
        with Session(self.engine) as session:
            query = (
                select(InferenceModel)
                .where(InferenceModel.id == id)
                .limit(1)
            )
            model = session.scalar(query)
            if model is None:
                return {}
            print(f'Model with id: {id} found! ')
            return {
                "id": model.id,
                "name": model.name,
                "title": model.title,
                "description": model.description,
                "img_url": model.img_url,
                "price": model.price,
                "min_resolution": model.min_resolution,
                "config": model.config
            }

    def load_images_by_org(self, organization_id: str):
        with Session(self.engine) as session:
            query = (
                select(Image)
                .where(
                    (Image.organization_id == organization_id)
                )
            )
            images = session.execute(query).all()
            if images is None:
                return {}
            result = []
            for img in images:
                img = img[0]
                bbox = None
                footprint = None
                if img.bbox is not None:
                    bbox = wkbelement_to_wkt(img.bbox)
                if img.footprint is not None:
                    footprint = wkbelement_to_wkt(img.footprint)
                result.append({
                    "id": img.id,
                    "name": img.name,
                    "created_at": img.created_at,
                    "url": img.url,
                    "data": img.data,
                    "bbox": bbox,
                    "footprint": footprint,
                    "user": img.user.username
                })
            return result

    def load_mosaics_by_org(self, organization_id: str):
        with Session(self.engine) as session:
            query = (
                select(Mosaic)
                .where(
                    (Mosaic.organization_id == organization_id)
                )
            )
            mosaics = session.execute(query).all()
            if mosaics is None:
                return {}
            result = []
            for mosaic in mosaics:
                mosaic = mosaic[0]
                result.append({
                    "id": mosaic.id,
                    "name": mosaic.name,
                    "description": mosaic.description,
                    "created_at": mosaic.created_at,
                    "coverage_store": mosaic.coverage_store,
                    "workspace": mosaic.organization.workspace
                })
            return result

    def load_process_by_id(self, id: str, user: User):
        with Session(self.engine) as session:
            query = (
                select(Process)
                .where(Process.id == id)
                .limit(1)
            )
            process = session.scalar(query)
            if process is None:
                print(f'No process with id ${id} found!')
                return {}
            elif process.organization_id != user.organization_id:
                print(f'This process is not from this org_id: {user.organization_id}')
                return None
            else:
                print(f'Process with id: {id} found! ')
                runs = []
                for run in process.runs:
                    finished_run_time = None
                    if run.finished_at is not None:
                        finished_run_time = run.finished_at.strftime("%d/%m/%Y: %H:%M")
                    runs.append({
                        "id": run.id,
                        "status": run.status,
                        "created_at": run.created_at.strftime("%d/%m/%Y: %H:%M"),
                        "finished_at": finished_run_time,
                        "engine": run.engine,
                        "runtime": run.runtime,
                        "cost": run.cost,
                        "data": run.data,
                        "input": {
                            "id": run.input.id,
                            "type": run.input.type,
                            "data": run.input.data
                        },
                        "model": run.inference_model.name
                    })
                geom = None
                if process.geom is not None:
                    geom = wkbelement_to_wkt(process.geom)
                mask = None
                if process.mask is not None:
                    mask = wkbelement_to_wkt(process.mask)
                return {
                    "id": process.id,
                    "name": process.name,
                    "status": process.status,
                    "type": process.type,
                    "created_at": process.created_at,
                    "finished_at": process.finished_at,
                    "runtime": process.runtime,
                    "area": process.area,
                    "cost_estimated": process.cost_estimated,
                    "data": process.data,
                    "user": process.user.username,
                    "inference_model_id": process.inference_model_id,
                    "geom": geom,
                    "mask": mask,
                    "runs": runs
                }

    def load_processes_by_org(self, org_id: int):
        with Session(self.engine) as session:
            query = (
                select(Process)
                .where(
                    (Process.organization_id == org_id)
                )
            )
            processes = session.execute(query).all()
            if processes is None:
                return []
            result = []
            for process in processes:
                process = process[0]
                geom = None
                if process.geom is not None:
                    geom = wkbelement_to_wkt(process.geom)
                mask = None
                if process.mask is not None:
                    mask = wkbelement_to_wkt(process.mask)
                result.append({
                    "id": process.id,
                    "name": process.name,
                    "status": process.status,
                    "type": process.type,
                    "created_at": process.created_at,
                    "finished_at": process.finished_at,
                    "runtime": process.runtime,
                    "area": process.area,
                    "cost_estimated": process.cost_estimated,
                    "data": process.data,
                    "user": process.user.username,
                    "inference_model_id": process.inference_model_id,
                    "geom": geom,
                    "mask": mask,
                })
            return result

    def load_results_by_run_id(self, id: str):
        results = {
            "raw": [],
            "raster": []
        }
        with Session(self.engine) as session:
            query_raw = (
                select(ResultsRaw)
                .where(ResultsRaw.run_id == id)
                .order_by(ResultsRaw.id)
            )
            raw_results = session.execute(query_raw).all()
            if raw_results is None:
                print(f'No raw results for run_id ${id}')
            else:
                print(f'Raw results for run_id={id} found!: {len(raw_results)} results')
                for raw_result in raw_results:
                    raw_result = raw_result[0]
                    wkt = wkbelement_to_wkt(raw_result.geom)
                    results["raw"].append({
                        "id": raw_result.id,
                        "data": raw_result.data,
                        "geom": wkt
                    })

            query_raster = (
                select(ResultsRaster)
                .where(ResultsRaster.run_id == id)
                .order_by(ResultsRaster.id)
            )
            raster_results = session.execute(query_raster).all()
            if raster_results is None:
                print(f'No raster results for run_id ${id}')
            else:
                print(f'Raster results for run_id={id} found!: {len(raster_results)} results')
                for raster_result in raster_results:
                    raster_result = raster_result[0]
                    wkt = wkbelement_to_wkt(raster_result.bbox)
                    results["raster"].append({
                        "id": raster_result.id,
                        "url": raster_result.url,
                        "data": raster_result.data,
                        "bbox": wkt
                    })

            return results

    def load_runs_by_process(self, id: str, user: User):
        with Session(self.engine) as session:
            organization_id = session.scalar(select(Process.organization_id).where(Process.id == id))

            if organization_id is None or organization_id != user.organization_id:
                return None

            query_run = (
                select(Run)
                .where(Run.process_id == id)
            )
            runs = session.scalars(query_run)

            results = []

            for run in runs:
                results.append({
                    "id": run.id,
                    "status": run.status,
                    "created_at": run.created_at,
                    "finished_at": run.finished_at,
                    "engine": run.engine,
                    "runtime": run.runtime,
                    "cost": run.cost,
                    "data": run.data,
                    "inference_model_id": run.inference_model_id,
                    "bbox": wkbelement_to_wkt(run.bbox) if run.bbox is not None else None,
                })

            return results

    def load_run_by_id(self, id: str, user: User):
        with Session(self.engine) as session:
            query_run = (
                select(Run)
                .where(Run.id == id)
                .limit(1)
            )
            run = session.scalar(query_run)
            if run is None:
                print(f'No run with id ${id} found!')
                return {}
            elif run.process.organization_id != user.organization_id:
                print(f'This process is not from this org_id: {user.organization_id}')
                return None
            else:
                print(f'Run with id: {id} found! ')
                raw_results = []
                for raw_result in run.results_raw:
                    wkt = wkbelement_to_wkt(raw_result.geom)
                    raw_results.append({
                        "id": raw_result.id,
                        "data": raw_result.data,
                        "geom": wkt
                    })
                raster_results = []
                for raster_result in run.results_raster:
                    wkt = wkbelement_to_wkt(raster_result.bbox)
                    raster_results.append({
                        "id": raster_result.id,
                        "url": raster_result.url,
                        "data": raster_result.data,
                        "bbox": wkt
                    })
                return {
                    "id": run.id,
                    "status": run.status,
                    "created_at": run.created_at,
                    "finished_at": run.finished_at,
                    "engine": run.engine,
                    "runtime": run.runtime,
                    "cost": run.cost,
                    "data": run.data,
                    "process_id": run.process_id,
                    "process_name": run.process.name,
                    "mask": wkbelement_to_wkt(run.process.mask),
                    "inference_model_id": run.inference_model_id,
                    "input_id": run.input_id,
                    "input_data": run.input.data,
                    "organization_id": run.process.organization_id,
                    "organization_name": run.process.organization.name,
                    "results_raw": raw_results,
                    "results_raster": raster_results
                }

    def upload_image(self, img: UploadImageDict, user: User):
        name = img["name"]
        url = img["url"]
        bbox = img["bbox"]
        print(f'Adding new uploaded image: {name} from user_id: {user.id}')
        with Session(self.engine) as session:
            new_image = Image(
                name=name,
                url=url,
                bbox=bbox,
                user_id=user.id,
                organization_id=user.organization_id
            )
            session.add(new_image)
            session.commit()
            return new_image

    def add_results_raster(self, run_id, object_key, data=None, bbox=None):
        with Session(self.engine) as session:
            new_result = ResultsRaster(
                url=object_key,
                data=data,
                bbox=bbox,
                run_id=run_id
            )
            session.add(new_result)
            session.commit()
            return new_result

    def delete_process(self, id: str, user: User):
        with Session(self.engine) as session:
            query = (
                select(Process)
                .where(
                    and_(
                        (Process.id == id),
                        (Process.organization_id == user.organization_id)
                    )
                )
                .limit(1)
            )
            process = session.scalar(query)
            if process is None:
                print(f'No process with id ${id} found!')
                return False
            else:
                print(f'Deleting process with id: {id}')
                session.delete(process)
                session.commit()
                return True

    def get_raster_img_url(self, id: str, user: User):
        with Session(self.engine) as session:
            query = (
                select(ResultsRaster)
                .where(ResultsRaster.id == id)
                .limit(1)
            )
            raster = session.scalar(query)
            if raster is None:
                print(f'No raster result with id ${id} found!')
                return None
            else:
                print(f'Raster result with id: {id} found!')
                return raster.url

    def get_run_thumbnail_url(self, id: str, user: User):
        with Session(self.engine) as session:
            query = (
                select(Run)
                .where(Run.id == id)
                .limit(1)
            )
            run = session.scalar(query)
            if run is None:
                print(f'No run with id ${id} found!')
                return None
            else:
                print(f'Run with id: {id} found!')
                url = run.filepath + "thumbnail.png"
                return url

    def edit_process_name(self, id: str, name: str, user: User):
        with Session(self.engine) as session:
            query = (
                select(Process)
                .where(
                    and_(
                        (Process.id == id),
                        (Process.organization_id == user.organization_id)
                    )
                )
                .limit(1)
            )
            process = session.scalar(query)
            if process is None:
                print(f'No process with id ${id} found!')
                return False
            else:
                print(f'Editing process name with id: {id}')
                process.name = name
                session.commit()
                return True

#######################################
######### library methods #############
#######################################

    def update_run_status(self, run_id: int, status: Literal['queued', 'running', 'finished', 'failed', 'canceled']):
        """
        Updates the status of the run

        Args:
            run_id: The id of the run
            status: The new status of the run
        """
        assert isinstance(run_id, int), 'Invalid run_id!'
        assert status in ['queued', 'running', 'finished', 'failed', 'canceled'], 'Invalid status!'

        with Session(self.engine) as session:
            query = (
                select(Run)
                .where(Run.id == run_id)
                .limit(1)
            )
            run = session.scalar(query)
            if run is None:
                print(f'No run with id ${run_id} found!')
                return False
            run.status = status
            if status == 'running':
                run.process.status = 'running'
            session.commit()
            return True

    def upload_run_results(self, run_id: int, runtime: int, bbox: str, files_path: str, raster_name: str=None, file_names: list[str]=[], data: dict=None):
        """
        Uploads the files to the S3 bucket and updates the run status to finished

        Args:
            run_id: The id of the run
            bbox: The bbox of the raster
            files_path: The path where the files are located
            runtime: The runtime of the run
            raster_name: The name of the raster file
            file_names: Array with the names of additional files to upload
            data: additional data to store in the results raster table
        """
        assert isinstance(run_id, int), 'Invalid run_id!'
        assert bbox is None or isinstance(bbox, str), 'Invalid bbox!'
        assert isinstance(runtime, (int, float)), 'Invalid runtime!'
        runtime = int(runtime)
        assert isinstance(files_path, str), 'Invalid files_path!'
        assert raster_name is None or isinstance(raster_name, str), 'Invalid raster_name!'
        assert isinstance(file_names, list), 'Invalid file_names!'
        assert data is None or isinstance(data, dict), 'Invalid data!'

        assert raster_name is not None or len(file_names) != 0, 'No files to upload!'

        with Session(self.engine) as session:
            # actual function
            query = (
                select(Run)
                .where(Run.id == run_id)
                .limit(1)
            )
            run = session.scalar(query)
            if run is None:
                print(f'No run with id ${run_id} found!')
                return False

            process_id = run.process_id
            org_id = run.process.organization_id
            run_id = run.id

            # upload files to bucket
            s3_client = S3Client(settings.run_results_bucket, settings.s3_region)
            bucket_base_directory = f"{org_id}/{process_id}/{run_id}/"

            for file_name in file_names:
                if not isinstance(file_name, str):
                    print('Invalid file_name!')
                    return False
                print(f'Uploading file: {file_name}')
                object_key = bucket_base_directory + file_name
                file_path = os.path.join(files_path, file_name)
                s3_client.upload_file(file_path, object_key)
                print(f'File uploaded to S3 with key: {object_key}')

            if raster_name is not None:
                print(f'Uploading raster file: {raster_name}')
                object_key = bucket_base_directory + raster_name
                file_path = os.path.join(files_path, raster_name)
                s3_client.upload_file(file_path, object_key)
                print(f'File uploaded to S3 with key: {object_key}')
                self.add_results_raster(run_id, object_key, data, bbox)

            # update run status
            # when all runs of a process are finished, an SQL trigger will update the process status
            run.status = 'finished'
            run.finished_at = func.now()
            run.bbox = bbox
            # SQL trigger will update the process runtime
            run.runtime = runtime
            run.filepath = bucket_base_directory
            session.commit()

            return True

    def load_queued_runs_by_model(self, model_id: str):
        with Session(self.engine) as session:
            query_runs = (
                select(Run)
                .where(Run.inference_model_id == model_id)
                .where(
                    (Run.inference_model_id == model_id) &
                    (Run.status == 'queued')
                )
                .order_by(Run.id)
            )
            runs = session.execute(query_runs).all()
            if runs is None:
                return []
            else:
                print(f'Queued runs found!: {len(runs)} results')
                results = []
                for run in runs:
                    run = run[0]
                    results.append({
                        "id": run.id,
                        "status": run.status,
                        "created_at": run.created_at.strftime("%d/%m/%Y: %H:%M"),
                        "engine": run.engine,
                        "runtime": run.runtime,
                        "cost": run.cost,
                        "data": run.data,
                        "process_id": run.process_id,
                        "process_name": run.process.name,
                        "mask": wkbelement_to_wkt(run.process.mask),
                        "inference_model_id": run.inference_model_id,
                        "organization_id": run.process.organization_id,
                        "organization_name": run.process.organization.name,
                        "input":{
                            "input_id": run.input_id,
                            "input_type": run.input.type,
                            "input_data": run.input.data
                        }
                    })
                return results
