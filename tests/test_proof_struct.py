"""
Tests formal construction, serialization and representation of Merkle-proofs
"""

import pytest
import json

from pymerkle import MerkleTree
from pymerkle.prover import MerkleProof, PROOF_TEMPLATE
from pymerkle.utils import stringify_path


provider = '1a0894bc-9755-11e9-a651-70c94e89b637'
path = (
    (+1, b'3f824b56e7de850906e053efa4e9ed2762a15b9171824241c77b20e0eb44e3b8'),
    (+1, b'4d8ced510cab21d23a5fd527dd122d7a3c12df33bc90a937c0a6b91fb6ea0992'),
    (+1, b'35f75fd1cfef0437bc7a4cae7387998f909fab1dfe6ced53d449c16090d8aa52'),
    (-1, b'73c027eac67a7b43af1a13427b2ad455451e4edfcaced8c2350b5d34adaa8020'),
    (+1, b'cbd441af056bf79c65a2154bc04ac2e0e40d7a2c0e77b80c27125f47d3d7cba3'),
    (+1, b'4e467bd5f3fc6767f12f4ffb918359da84f2a4de9ca44074488b8acf1e10262e'),
    (-1, b'db7f4ee8be8025dbffee11b434f179b3b0d0f3a1d7693a441f19653a65662ad3'),
    (-1, b'f235a9eb55315c9a197d069db9c75a01d99da934c5f80f9f175307fb6ac4d8fe'),
    (+1, b'e003d116f27c877f6de213cf4d03cce17b94aece7b2ec2f2b19367abf914bcc8'),
    (-1, b'6a59026cd21a32aaee21fe6522778b398464c6ea742ccd52285aa727c367d8f2'),
    (-1, b'2dca521da60bf0628caa3491065e32afc9da712feb38ff3886d1c8dda31193f8'))

proof_11 = MerkleProof(
    provider=provider,
    hash_type='sha_256',
    encoding='utf_8',
    security=True,
    raw_bytes=True,
    offset=5,
    path=path)

proof_21 = MerkleProof(
    provider=provider,
    hash_type='sha_256',
    encoding='utf_8',
    security=True,
    raw_bytes=True,
    offset=-1,
    path=())

proof_12 = MerkleProof(
    provider=provider,
    hash_type='sha_256',
    encoding='utf_8',
    raw_bytes=True,
    security=True,
    offset=5,
    path=path
)

proof_22 = MerkleProof(
    provider=provider,
    hash_type='sha_256',
    encoding='utf_8',
    raw_bytes=True,
    security=True,
    offset=-1,
    path=()
)

proof_31 = MerkleProof(
    provider=provider,
    hash_type='sha_256',
    encoding='utf_8',
    raw_bytes=True,
    security=True,
    commitment=b'd079da3aee8025dbffee11b434f1abd52e97caa1d7693a441f196093abc64993',
    offset=5,
    path=path
)


@pytest.mark.parametrize('proof', (proof_11, proof_31))
def test_MerkleProof_deserialization_from_dict(proof):
    json_proof = proof.serialize()
    deserialized = MerkleProof.deserialize(json_proof)
    assert proof.__dict__ == deserialized.__dict__


@pytest.mark.parametrize('proof', (proof_11, proof_31))
def test_MerkleProof_deserialization_from_text(proof):
    json_proof = proof.toJSONtext()
    deserialized = MerkleProof.deserialize(json_proof)
    assert proof.__dict__ == deserialized.__dict__


serializations = [
    (
        proof_11,
        {
            'header': {
                'uuid': proof_11.uuid,
                'timestamp': proof_11.timestamp,
                'created_at': proof_11.created_at,
                'provider': provider,
                'hash_type': 'sha_256',
                'encoding': 'utf_8',
                'raw_bytes': True,
                'security': True,
                'commitment': None,
                'status': None
            },
            'body': {
                'offset': 5,
                'path': [
                    [+1, '3f824b56e7de850906e053efa4e9ed2762a15b9171824241c77b20e0eb44e3b8'],
                    [+1, '4d8ced510cab21d23a5fd527dd122d7a3c12df33bc90a937c0a6b91fb6ea0992'],
                    [+1, '35f75fd1cfef0437bc7a4cae7387998f909fab1dfe6ced53d449c16090d8aa52'],
                    [-1, '73c027eac67a7b43af1a13427b2ad455451e4edfcaced8c2350b5d34adaa8020'],
                    [+1, 'cbd441af056bf79c65a2154bc04ac2e0e40d7a2c0e77b80c27125f47d3d7cba3'],
                    [+1, '4e467bd5f3fc6767f12f4ffb918359da84f2a4de9ca44074488b8acf1e10262e'],
                    [-1, 'db7f4ee8be8025dbffee11b434f179b3b0d0f3a1d7693a441f19653a65662ad3'],
                    [-1, 'f235a9eb55315c9a197d069db9c75a01d99da934c5f80f9f175307fb6ac4d8fe'],
                    [+1, 'e003d116f27c877f6de213cf4d03cce17b94aece7b2ec2f2b19367abf914bcc8'],
                    [-1, '6a59026cd21a32aaee21fe6522778b398464c6ea742ccd52285aa727c367d8f2'],
                    [-1, '2dca521da60bf0628caa3491065e32afc9da712feb38ff3886d1c8dda31193f8']
                ]
            }
        }
    ),
    (
        proof_21,
        {
            'header': {
                'uuid': proof_21.uuid,
                'timestamp': proof_21.timestamp,
                'created_at': proof_21.created_at,
                'provider': provider,
                'hash_type': 'sha_256',
                'encoding': 'utf_8',
                'raw_bytes': True,
                'security': True,
                'commitment': None,
                'status': None
            },
            'body': {
                'offset': -1,
                'path': []
            }
        }
    )
]


@pytest.mark.parametrize('proof, _serialization', serializations)
def test_serialization(proof, _serialization):
    assert proof.serialize() == _serialization


json_texts = [
    (
        proof_11,
        '{\n    "body": {\n        "offset": 5,\n        "path": [\n            [\n                1,\n                "3f824b56e7de850906e053efa4e9ed2762a15b9171824241c77b20e0eb44e3b8"\n            ],\n            [\n                1,\n                "4d8ced510cab21d23a5fd527dd122d7a3c12df33bc90a937c0a6b91fb6ea0992"\n            ],\n            [\n                1,\n                "35f75fd1cfef0437bc7a4cae7387998f909fab1dfe6ced53d449c16090d8aa52"\n            ],\n            [\n                -1,\n                "73c027eac67a7b43af1a13427b2ad455451e4edfcaced8c2350b5d34adaa8020"\n            ],\n            [\n                1,\n                "cbd441af056bf79c65a2154bc04ac2e0e40d7a2c0e77b80c27125f47d3d7cba3"\n            ],\n            [\n                1,\n                "4e467bd5f3fc6767f12f4ffb918359da84f2a4de9ca44074488b8acf1e10262e"\n            ],\n            [\n                -1,\n                "db7f4ee8be8025dbffee11b434f179b3b0d0f3a1d7693a441f19653a65662ad3"\n            ],\n            [\n                -1,\n                "f235a9eb55315c9a197d069db9c75a01d99da934c5f80f9f175307fb6ac4d8fe"\n            ],\n            [\n                1,\n                "e003d116f27c877f6de213cf4d03cce17b94aece7b2ec2f2b19367abf914bcc8"\n            ],\n            [\n                -1,\n                "6a59026cd21a32aaee21fe6522778b398464c6ea742ccd52285aa727c367d8f2"\n            ],\n            [\n                -1,\n                "2dca521da60bf0628caa3491065e32afc9da712feb38ff3886d1c8dda31193f8"\n            ]\n        ]\n    },\n    "header": {\n        "commitment": %s,\n        "created_at": "%s",\n        "encoding": "utf_8",\n        "hash_type": "sha_256",\n        "provider": "%s",\n        "raw_bytes": true,\n        "security": true,\n        "status": null,\n        "timestamp": %d,\n        "uuid": "%s"\n    }\n}' %
        ('null', proof_11.created_at, provider,
         proof_11.timestamp, proof_11.uuid)
    ),
    (
        proof_21,
        '{\n    "body": {\n        "offset": -1,\n        "path": []\n    },\n    "header": {\n        "commitment": %s,\n        "created_at": "%s",\n        "encoding": "utf_8",\n        "hash_type": "sha_256",\n        "provider": "%s",\n        "raw_bytes": true,\n        "security": true,\n        "status": null,\n        "timestamp": %d,\n        "uuid": "%s"\n    }\n}' % (
            'null', proof_21.created_at, provider, proof_21.timestamp, proof_21.uuid)
    )
]


@pytest.mark.parametrize('proof, json_text', json_texts)
def test_proof_toJSONtext(proof, json_text):
    assert proof.toJSONtext() == json_text


proof_13 = MerkleProof.from_json(proof_11.toJSONtext())
proof_23 = MerkleProof.from_json(proof_21.toJSONtext())
proof_14 = MerkleProof.from_dict(json.loads(proof_11.toJSONtext()))
proof_24 = MerkleProof.from_dict(json.loads(proof_21.toJSONtext()))

@pytest.mark.parametrize('proof, generation',
                         ((proof_11, True), (proof_12, True), (proof_13, True), (proof_14, True),
                          (proof_21, False), (proof_22, False), (proof_23, False), (proof_24, False)))
def test___repr__(proof, generation):
    assert proof.__repr__() == PROOF_TEMPLATE.format(uuid=proof.uuid,
                                                     timestamp=proof.timestamp,
                                                     created_at=proof.created_at,
                                                     provider=provider,
                                                     hash_type='SHA256',
                                                     encoding='UTF-8',
                                                     raw_bytes='TRUE',
                                                     security='ACTIVATED',
                                                     offset=5 if generation else -1,
                                                     path=stringify_path(
                                                         path, 'utf-8')
                                                     if generation else '',
                                                     commitment=proof.commitment,
                                                     status='UNVERIFIED')
