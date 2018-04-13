import datetime
import unittest

from sbs_log_parser import SBSLogParser
from time_range import TimeRange


class SimpleTestCases(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testGetLogTime(self):
    log_file = "log.txt"
    station = "sbs1"
    self.test_get_log_time = SBSLogParser(station, log_file,
                                          None, None, None)

    line = "2014-01-15 00:00:24-0800 [HTTPChannel,20,192.168.101.42]"
    line2 = "	Traceback (most recent call last):"

    date = datetime.datetime(2014, 1, 15, 0, 0, 24)

    self.assertEqual(self.test_get_log_time.GetLogTime(line),
                     date)

    self.assertIsNone(self.test_get_log_time.GetLogTime(line2))

  def testGenerateData(self):
    time_ranges = [TimeRange(0, 0, 8, 0),
                   TimeRange(8, 0, 13, 30),
                   TimeRange(13, 30, 16, 30),
                   TimeRange(16, 30, 23, 59),
                   TimeRange(0, 0, 23, 59)]

    start_capture = "configure for capture of type : swivel"
    end_capture = "capture complete"
    upload_capture = "uploading to config"

    log_file = open("testdata/log_test.txt", "r")
    station = "sbs1"
    self.test_timeblock_data = SBSLogParser(station, log_file, start_capture,
                                            end_capture, upload_capture)

    processed_data = self.test_timeblock_data.GenerateTimeBlockData(time_ranges)

    # Not testing html_string time because the data length is too long
    self.assertEqual(processed_data["Total"], 5)
    self.assertEqual(processed_data["Total_canceled"], 1)


if __name__ == "__main__":
  unittest.main()
