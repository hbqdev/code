import glob
import os
import unittest

from check_storage import AvailableSpace
from check_storage import CleanUp
from check_storage import GetDirectories2d
import utils

# Test data will be contained within this directory
TEST_DIR = "testdata"
# Regex for test backup directories
TEST_GLOB_PATTERN = "testdata/sbs*-backup"
# Test backup dirs
TEST_BACKUP_DIRS = ["sbs1-backup", "sbs2-backup", "sbs3-backup"]
# The backup date for the test dir
TEST_DATES = ["2014-02-03", "2014-02-04", "2014-02-05",
              "2014-02-06", "2014-02-07"]


def GenerateTestData(backup_dirs, dates):
  """Simulate the file hierarchy on persephone at /scan.

  Args:
    backup_dirs: the test backup dirs to be created
    dates: the date dirs to create within each backup_dir

  Returns:
    dictionary of created backup dirs
  """
  for backup_dir in backup_dirs:
    backup_dir_path = os.path.join(TEST_DIR, backup_dir)
    make_backup_dir_cmd = ["mkdir", backup_dir_path]

    # Make the test backup station directory
    utils.CheckSubprocessCall(make_backup_dir_cmd)

    for date in dates:
      backup_date_path = os.path.join(backup_dir_path, date)
      make_backup_date_cmd = ["mkdir", backup_date_path]

      # Make the test backup date directory
      utils.CheckSubprocessCall(make_backup_date_cmd)

      test_file_path = os.path.join(backup_date_path, "file.txt")
      make_file_cmd = ["dd", "if=/dev/zero", "of=" + test_file_path,
                       "count=1024", "bs=2048"]

      # Make the individual test files inside of the backup date directory
      utils.CheckSubprocessCall(make_file_cmd)


class SimpleTestCases(unittest.TestCase):
  def setUp(self):
    GenerateTestData(TEST_BACKUP_DIRS, TEST_DATES)

    # Make an empty directory to test special cases
    utils.CheckSubprocessCall(["mkdir", "testdata/sbs4-backup"])

  def tearDown(self):
    for backup_dir_path in glob.glob(TEST_GLOB_PATTERN):
      delete_test_dir_cmd = ["rm", "-r", backup_dir_path]
      utils.CheckSubprocessCall(delete_test_dir_cmd)

  def testGetBackupDirs(self):
    test_dirs = {"2014-02-03": [("testdata/sbs1-backup/2014-02-03", 2048),
                                ("testdata/sbs2-backup/2014-02-03", 2048),
                                ("testdata/sbs3-backup/2014-02-03", 2048)],
                 "2014-02-04": [("testdata/sbs1-backup/2014-02-04", 2048),
                                ("testdata/sbs2-backup/2014-02-04", 2048),
                                ("testdata/sbs3-backup/2014-02-04", 2048)],
                 "2014-02-05": [("testdata/sbs1-backup/2014-02-05", 2048),
                                ("testdata/sbs2-backup/2014-02-05", 2048),
                                ("testdata/sbs3-backup/2014-02-05", 2048)],
                 "2014-02-06": [("testdata/sbs1-backup/2014-02-06", 2048),
                                ("testdata/sbs2-backup/2014-02-06", 2048),
                                ("testdata/sbs3-backup/2014-02-06", 2048)],
                 "2014-02-07": [("testdata/sbs1-backup/2014-02-07", 2048),
                                ("testdata/sbs2-backup/2014-02-07", 2048),
                                ("testdata/sbs3-backup/2014-02-07", 2048)]}

    self.backup_dirs = GetDirectories2d(TEST_GLOB_PATTERN)
    self.backup_dates = self.backup_dirs.keys()
    self.backup_dates.sort()

    # Testing the GetBackupDirectories functon
    self.assertEqual(TEST_DATES, self.backup_dates)
    self.assertItemsEqual(test_dirs, self.backup_dirs)

  def testCleanUp(self):
    free_space = AvailableSpace(TEST_DIR)

    # Set the current buffer size to 16MB more than the current size
    buffer_size = free_space + (16 * 1024)

    self.deleted_dirs = CleanUp(False, free_space, buffer_size,
                                False, TEST_GLOB_PATTERN)

    new_free_space = AvailableSpace(TEST_DIR)
    self.assertGreaterEqual(new_free_space, buffer_size)


if __name__ == "__main__":
  unittest.main()
