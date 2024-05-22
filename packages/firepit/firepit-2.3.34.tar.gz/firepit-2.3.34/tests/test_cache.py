from .helpers import tmp_storage


def test_cache_type_change(tmpdir):
    identity = {
        "type": "identity",
        "id": "identity--2e0c124c-f2af-4810-bf80-44a0fd218540",
        "created": "2020-06-30T19:31:23.304Z",
        "modified": "2021-07-14T19:45:16.866Z",
        "name": "test",
        "identity_class": "program"
    }

    obs1 = {
        "type": "observed-data",
        "id": "observed-data--0b968993-a378-4085-b1e1-052fc996fe78",
        "created_by_ref": "identity--2e0c124c-f2af-4810-bf80-44a0fd218540",
        "first_observed": "2020-06-30T19:25:09.447726Z",
        "last_observed": "2020-06-30T19:28:49.692424Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "x-foo",
                "value": 1
            }
        },
    }

    obs2 = {
        "type": "observed-data",
        "id": "observed-data--e1a5b370-6d53-491a-9b47-7cf55a8ac849",
        "created_by_ref": "identity--2e0c124c-f2af-4810-bf80-44a0fd218540",
        "first_observed": "2020-06-30T19:25:09.447726Z",
        "last_observed": "2020-06-30T19:28:49.692424Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "x-foo",
                "value": 1.1
            }
        }
    }

    bundle = {
        "type": "bundle",
        "id": "bundle--accb7075-8639-438f-9d36-fc7707ea9214",
        "objects": [
            identity,
            obs1.copy(),
            obs2.copy(),
        ]
    }

    store = tmp_storage(tmpdir)
    store.cache('q1', bundle)

    obs1['id'] = "observed-data--c71ee7fc-db1e-42f1-9fde-94ca7ac718b3"
    obs1['objects']['0']['value'] = 1.2
    bundle['objects'][1] = obs1

    store.cache('q2', bundle)
