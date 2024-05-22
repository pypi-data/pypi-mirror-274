import unittest
from unittest.mock import patch
import  src.log_utility as log_utility

# init the test class
class TestLogUtility(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    # test function preprocessing_output_directory in log_utility.py
    def test_preprocessing_output_directory(self):
        # assume the output directory is /tmp/log_trans/
        # there are 12 different files in the directory
        # file name like : 20210913175500-log.tar.gz
        # mock files in the directory and its create time is sort by name
        mock_files = [
            "20210913175500-log.tar.gz",
            "20210913175501-log.tar.gz",
            "20210913175502-log.tar.gz",
            "20210913175503-log.tar.gz",
            "20210913175504-log.tar.gz",
            "20210913175505-log.tar.gz",
            "20210913175506-log.tar.gz",
            "20210913175507-log.tar.gz",
            "20210913175508-log.tar.gz",
            "20210913175509-log.tar.gz",
            "20210913175510-log.tar.gz",
            "20210913175511-log.tar.gz",
        ]
        # mock the os.listdir function
        with patch("os.listdir") as mock_listdir:
            # mock the return value of os.listdir
            mock_listdir.return_value = mock_files
            # mock the os.remove function
            with patch("os.remove") as mock_remove:
                # call the preprocessing_output_directory function
                log_utility.preprocessing_output_directory("/tmp/log_trans/")
                # assert the mock_remove function is called 2 times
                mock_remove.assert_has_calls(mock_remove, 2)

                # make sure remove the right file
                mock_remove.assert_has_calls(mock_remove, "20210913175500-log.tar.gz")
                mock_remove.assert_has_calls(mock_remove, "20210913175501-log.tar.gz")



if __name__ == "__main__":
    unittest.main()
