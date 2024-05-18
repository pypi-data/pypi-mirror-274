from openghg.util import running_locally

cloud_env = not running_locally()

if cloud_env:
    from ._oci_store import (
        create_bucket,
        create_par,
        delete_object,
        delete_par,
        exists,
        get_all_object_names,
        get_bucket,
        get_object,
        get_object_from_json,
        set_object,
        set_object_from_file,
        set_object_from_json,
        upload,
    )
    from ._par import PAR
else:
    from ._local_store import (
        delete_object,
        delete_objects,
        exists,
        get_all_object_names,
        get_bucket,
        get_object,
        get_object_data_path,
        get_object_lock_path,
        get_object_from_json,
        get_object_names,
        get_objectstore_info,
        get_user_objectstore_path,
        get_tutorial_store_path,
        move_object,
        move_objects,
        query_store,
        set_object,
        set_object_from_file,
        set_object_from_json,
        get_writable_bucket,
        get_writable_buckets,
        get_readable_buckets,
        get_folder_size,
    )

from ._encoding import bytes_to_string, datetime_to_datetime, get_datetime_now, string_to_bytes
from ._integrity import integrity_check
