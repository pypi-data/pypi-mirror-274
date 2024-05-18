import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
import requests

from hyp3_sdk import Job
from hyp3_sdk.hyp3 import HyP3


@pytest.fixture(autouse=True)
def get_mock_hyp3():
    def mock_my_info(self):
        return {'application_status': 'APPROVED'}

    def mock_get_authenticated_session(username, password):
        return requests.Session()

    def default_hyp3():
        with patch('hyp3_sdk.hyp3.HyP3.my_info', mock_my_info):
            with patch('hyp3_sdk.util.get_authenticated_session', mock_get_authenticated_session):
                return HyP3()
    return default_hyp3


@pytest.fixture(autouse=True)
def get_mock_job():
    def default_job(
            job_type='JOB_TYPE',
            request_time=datetime.now(),
            status_code='RUNNING',
            user_id='user',
            name='name',
            job_parameters=None,
            files=None,
            browse_images=None,
            thumbnail_images=None,
            expiration_time=None,
            credit_cost=None,
            priority=None,
    ):
        if job_parameters is None:
            job_parameters = {'param1': 'value1'}
        job_dict = {
            'job_type': job_type,
            'job_id': str(uuid4()),
            'request_time': request_time.isoformat(timespec='seconds'),
            'status_code': status_code,
            'user_id': user_id,
            'name': name,
            'job_parameters': job_parameters,
            'files': files,
            'browse_images': browse_images,
            'thumbnail_images': thumbnail_images,
            'expiration_time': expiration_time,
        }
        keys_to_delete = []
        for k, v in job_dict.items():
            if v is None:
                keys_to_delete.append(k)

        for key in keys_to_delete:
            del job_dict[key]

        return Job.from_dict(job_dict)
    return default_job


@pytest.fixture
def test_data_dir():
    data_dir = Path(__file__).resolve().parent / 'data'
    return data_dir


@pytest.fixture
def product_zip(tmp_path_factory, test_data_dir):
    tmp_dir = tmp_path_factory.mktemp('data')

    product_file = tmp_dir / 'product.zip'
    shutil.copy(test_data_dir / 'product.zip', product_file)

    return product_file
