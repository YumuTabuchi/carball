import io
import logging

from pandas import DataFrame

from replay_analysis.analysis.utils.numpy_manager import write_array_to_file, read_array_from_file


logger = logging.getLogger(__name__)


class PandasManager:

    @staticmethod
    def safe_write_pandas_to_memory(df, field_name=""):
        try:
            # return PandasManager.write_hdf_to_buffer(df)
            return PandasManager.write_numpy_to_memory(df)
        except BaseException as e:
            logger.exception("Failure to write pandas [%s] to memory: %s", field_name, e)

    @staticmethod
    def safe_read_pandas_to_memory(buffer, field_name=""):
        try:
            return PandasManager.read_numpy_from_memory(buffer)
        except BaseException as e:
            logger.exception("Failure to read pandas [%s] from memory: %s", field_name, e)

    @staticmethod
    def read_hdf_from_buffer(buffer, key="/data"):
        from pandas import get_store
        with get_store(
                "data.h5",
                mode="r",
                driver="H5FD_CORE",
                driver_core_backing_store=0,
                driver_core_image=buffer.read()
        ) as store:
            return store[key]

    @staticmethod
    def write_hdf_to_buffer(df):
        from pandas import get_store
        with get_store(
                "data.h5", mode="a", driver="H5FD_CORE",
                driver_core_backing_store=0
        ) as out:
            out["/data"] = df
            return out._handle.get_file_image()

    @staticmethod
    def write_numpy_to_memory(df):
        numpy_array = df.to_records(index=True)
        compressed_array = io.BytesIO()
        write_array_to_file(compressed_array, numpy_array)
        return compressed_array.getvalue()

    @staticmethod
    def read_numpy_from_memory(buffer):
        array = read_array_from_file(buffer)
        return DataFrame.from_records(array)
