import pytest
import psycopg
from ..conftest import prepare_fs


@pytest.fixture(autouse=True, scope="module")
def dbCleanup(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""TRUNCATE TABLE sequences, sequences_pictures, pictures, pictures_to_process CASCADE;""")


@pytest.fixture(scope="module")
def fs(tmp_path_factory):
    return prepare_fs(tmp_path_factory.mktemp("many_sequences"))
