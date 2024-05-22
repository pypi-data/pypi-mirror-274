from typing import Callable
from zipfile import ZipFile
import firebase_admin
from firebase_admin import credentials, storage, firestore, auth as fb_auth
from firebase_admin._auth_utils import UserNotFoundError
from pathlib import Path
import json, os, io
from google.cloud.firestore_v1.transaction import Transaction
from google.cloud.firestore_v1 import (
    DocumentSnapshot,
    DocumentReference,
    Query,
)
from google.cloud.exceptions import Conflict
import streamlit as st
import base64
import pandas as pd
import toml

from vizkit.pipeline.data_source import DataFile, DataFileMeta

__SERVICE_ACCOUNT_KEY_FILE = (
    Path(__file__).parent.parent.parent.parent.parent / "serviceAccountKey.json"
)

if __SERVICE_ACCOUNT_KEY_FILE.exists():
    with open(__SERVICE_ACCOUNT_KEY_FILE, "r") as f:
        cert = json.load(f)
    cred = credentials.Certificate(cert)
else:
    # Load from env-var
    if key_base64 := os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_BASE64"):
        cert_str = base64.b64decode(key_base64).decode("utf-8")
        cert = json.loads(cert_str)
        cred = credentials.Certificate(cert)
    else:
        raise FileNotFoundError(
            f"Service account key file not found: {__SERVICE_ACCOUNT_KEY_FILE.absolute()}"
        )


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def __get_default_bucket_name():
    if bucket := os.environ.get("FIRESBASE_STORAGE_BUCKET"):
        if not bucket.startswith("gs://") or not bucket.endswith(".appspot.com"):
            raise ValueError(f"Invalid bucket name: {bucket}")
        bocket_url = f"{bucket}.appspot.com"
    project_id = cert["project_id"]
    bocket_url = f"gs://{project_id}.appspot.com"
    return bocket_url.removeprefix("gs://")


_DEFAULT_BUCKET_NAME = __get_default_bucket_name()
_BUCKET = storage.bucket(name=_DEFAULT_BUCKET_NAME)

_STORE = firestore.client()


def get_user_name_by_uid(uid: str) -> str:
    try:
        user = fb_auth.get_user(uid=uid)
    except UserNotFoundError:
        user = None
    return user.display_name if user else "<unknown>"


def get_or_create_user(email: str, name: str, avatar: str) -> str:
    try:
        user = fb_auth.get_user_by_email(email)
    except UserNotFoundError:
        user = None
    if not user:
        user = fb_auth.create_user(
            email=email, display_name=name, email_verified=True, photo_url=avatar
        )
    doc: DocumentSnapshot = _STORE.document("users", user.uid).get()
    if not doc.exists:
        _STORE.document("users", user.uid).set({"uid": user.uid})
    return user.uid


def upload_file(data: bytes, name: str, meta: DataFileMeta) -> tuple[str, bool]:
    file = io.BytesIO(data)
    blob = _BUCKET.blob(name)
    new_blob = not blob.exists()
    if not blob.exists():
        blob.upload_from_file(file)
        blob.patch()
        blob.metadata = meta.to_dict()
        blob.patch()
    return blob.public_url, new_blob


def get_data_file(id: str) -> DataFile:
    blob = _BUCKET.blob(f"results/{id}.zip")
    if not blob.exists():
        blobs = list(_BUCKET.list_blobs(prefix=f"results/{id}", max_results=1))
        if len(blobs) == 0:
            raise ValueError("File not found")
        blob = blobs[0]
    assert isinstance(blob.name, str)
    id = blob.name.split("/")[-1].removesuffix(".zip")
    file = io.BytesIO()
    blob.download_to_file(file)
    file.seek(0)
    with ZipFile(file, "r") as zip:
        with zip.open("results.csv") as f:
            results = pd.read_csv(f)
        with zip.open("config.toml") as f:
            config = toml.loads(f.read().decode("utf-8"))
    return DataFile(
        results=results,
        config=config,
        meta=get_data_file_meta(id),
    )


def get_data_file_meta(id: str) -> DataFileMeta:
    cache = st.session_state.setdefault("data_file_meta_cache", {})
    if id in cache:
        return cache[id]
    blob = _BUCKET.blob(f"results/{id}.zip")
    if not blob.exists():
        raise ValueError("File not found")
    blob.reload()
    m = blob.metadata or {}
    runid = m.get("runid")
    assert runid is not None
    project = m.get("project")
    assert project is not None
    profile = m.get("profile")
    assert profile is not None
    meta = DataFileMeta(
        sha256=m.get("sha256", id),
        runid=runid,
        project=project,
        profile=profile,
        owner=m.get("owner"),
    )
    cache[id] = meta
    return meta


def claim_data_file(id: str, owner: str):
    # update user data
    docRef = _STORE.document("users", owner)
    docRef.update({"results": firestore.firestore.ArrayUnion([id])})
    # update blob
    blob = _BUCKET.blob("results/" + id + ".zip")
    if not blob.exists():
        raise ValueError("File not found")
    blob.reload()
    m = blob.metadata or {}
    m["owner"] = owner
    blob.metadata = m
    blob.patch()
    # Update cache
    get_data_file_meta(id).owner = owner


def get_owned_data_files(owner: str) -> list[DataFileMeta]:
    docRef = _STORE.document("users", owner).get()
    if not docRef.exists:
        return []
    try:
        results = docRef.get("results") or []
    except KeyError:
        results = []
    metas = []
    for id in results:
        blob = _BUCKET.blob(f"results/{id}.zip")
        if not blob.exists():
            continue
        metas.append(get_data_file_meta(id))
    return metas


def delete_data_file(owner: str, id: str):
    _STORE.document("users", owner).update(
        {"results": firestore.firestore.ArrayRemove([id])}
    )
    _BUCKET.blob(f"results/{id}.zip").delete()


def get_inflated_id(short_id: str) -> str | None:
    doc = _STORE.document("share-links-v1", short_id).get()
    if not doc.exists:
        return None
    return doc.get("inflated")


def insert_inflated_id(inflated: str, gen_key: Callable[[], str]) -> str:
    while True:
        try:
            tx = _STORE.transaction()
            links = _STORE.collection("share-links-v1")
            query = links.where("inflated", "==", inflated).limit(1)
            short_id = gen_key()
            new_doc = links.document(short_id)
            return __insert_inflated_id(tx, inflated, query, new_doc, short_id)
        except Conflict:
            continue


@firestore.firestore.transactional
def __insert_inflated_id(
    transaction: Transaction,
    inflated: str,
    query: Query,
    new_doc: DocumentReference,
    short_id: str,
):
    docs = query.get(transaction=transaction)
    if len(docs) > 0:
        return docs[0].id
    transaction.create(new_doc, {"inflated": inflated})
    return short_id


def get_user_auth_info(key: str) -> dict | None:
    doc = _STORE.document("auth-cache", key).get()
    if not doc.exists:
        return None
    return doc.to_dict()


def set_user_auth_info(key: str, uid: str, token: dict):
    _STORE.document("auth-cache", key).set({"uid": uid, "token": token})


def delete_user_auth_info(key: str):
    _STORE.document("auth-cache", key).delete()
