import datetime
import unittest

from time_range import TimeRange


class SimpleTestCases(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testReset(self):
    self.test_reset = TimeRange(0, 0, 8, 0)

    self.test_reset.total = 4
    self.test_reset.canceled = 1

    self.test_reset.Reset()

    self.assertEqual(self.test_reset.total, 0)
    self.assertEqual(self.test_reset.canceled, 0)

  def testValidTime(self):
    self.test_valid = TimeRange(0, 0, 8, 0)

    test_time = datetime.datetime(2014, 1, 22, 7, 59, 59)
    test_time2 = datetime.datetime(2014, 1, 22, 8, 0, 1)

    self.assertTrue(self.test_valid.TimeisValid(test_time))
    self.assertFalse(self.test_valid.TimeisValid(test_time2))

  def testAdd(self):
    start_time = datetime.datetime(2014, 1, 22, 8, 15, 0)
    end_time = datetime.datetime(2014, 1, 22, 8, 19, 0)
    upload_time = datetime.datetime(2014, 1, 22, 8, 20, 0)

    self.test_add = TimeRange(8, 0, 13, 30)

    self.test_add.AddScan(start_time, end_time, upload_time)
    self.test_add.AddScan(start_time, None, None)

    self.assertEqual(self.test_add.total, 1)
    self.assertEqual(self.test_add.canceled, 1)

  def testAverage(self):
    start_time = datetime.datetime(2014, 1, 22, 8, 15, 0)
    end_time = datetime.datetime(2014, 1, 22, 8, 20, 0)
    upload_time = datetime.datetime(2014, 1, 22, 8, 21, 0)
    start_time1 = datetime.datetime(2014, 1, 22, 10, 30, 0)
    end_time1 = datetime.datetime(2014, 1, 22, 10, 41, 0)
    upload_time1 = datetime.datetime(2014, 1, 22, 10, 42, 0)
    start_time2 = datetime.datetime(2014, 1, 22, 13, 22, 0)
    end_time2 = datetime.datetime(2014, 1, 22, 13, 27, 0)
    upload_time2 = datetime.datetime(2014, 1, 22, 13, 28, 0)

    self.test_average = TimeRange(8, 0, 13, 30)

    self.test_average.AddScan(start_time, end_time, upload_time)
    self.test_average.AddScan(start_time1, end_time1, upload_time1)
    self.test_average.AddScan(start_time2, end_time2, upload_time2)

    self.assertEqual(self.test_average.AverageOperatorScanTime(),
                     480.0)
    self.assertEqual(self.test_average.AverageIdletime(),
                     8670.0)

  def testTotalIdleTime(self):
    start_time = datetime.datetime(2014, 1, 22, 8, 0, 1)
    end_time = datetime.datetime(2014, 1, 22, 8, 20, 1)
    upload_time = datetime.datetime(2014, 1, 22, 8, 25, 1)

    self.test_total_idle = TimeRange(8, 0, 13, 30)

    self.test_total_idle.AddScan(start_time, end_time, upload_time)

    self.assertEqual(self.test_total_idle.TotalIdleTime(), 18300.0)

  def testTimeRangeString(self):
    self.test_get_start_time = TimeRange(0, 0, 23, 59, True)
    self.test_get_start_time2 = TimeRange(16, 30, 23, 59)
    self.test_get_start_time3 = TimeRange(13, 30, 16, 30)

    time_range = "%s" % self.test_get_start_time
    time_range2 = "%s" % self.test_get_start_time2
    time_range3 = "%s" % self.test_get_start_time3

    self.assertEqual(time_range, "Total")
    self.assertEqual(time_range2, "04:30 PM - End of Day")
    self.assertEqual(time_range3, "01:30 PM - 04:30 PM")


if __name__ == "__main__":
  unittest.main()
