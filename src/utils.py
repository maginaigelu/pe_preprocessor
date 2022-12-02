import os

import mmh3
import pefile
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StructType, StructField, StringType


def get_env(prefix, name, default=None, ):
    return os.getenv(f'{prefix}{name}]'.upper(), default)


@udf(returnType=IntegerType())
def hash_it(x):
    return mmh3.hash(bytes(x))


@udf(
    returnType=StructType(
        [
            StructField("architecture", StringType(), False),
            StructField("file_type", StringType(), False),
            StructField("imports", IntegerType(), False),
            StructField("exports", IntegerType(), False)
        ]
    )
)
def get_pe_meta(bfile):
    architecture = 'unrecognized'
    file_type = 'unrecognized'
    imports = 0
    exports = 0
    try:
        pf = pefile.PE(data=bytes(bfile), fast_load=True)
        architecture = pefile.MACHINE_TYPE[pf.FILE_HEADER.Machine]
        imports = len(getattr(pf, 'DIRECTORY_ENTRY_IMPORT', []))
        exports = len(getattr(pf, 'DIRECTORY_ENTRY_EXPORT', []))
        if pf.is_exe():
            file_type = 'exe'
        if pf.is_dll():
            file_type = 'dll'
    except pefile.PEFormatError:
        pass
    finally:
        return architecture, file_type, imports, exports


def transform_s3_page(data, bucket, s3a_prefix='s3a://'):
    return [f'{s3a_prefix}{bucket}/{j["Key"]}' for j in data]
