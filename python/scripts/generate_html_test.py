import unittest
import stations

from generate_html import CreateHyperlink


class TestCases(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testImgWrite(self):
    station_ip = "172.17.26.10"
    tn = "10-300.tn.jpg"
    img = "10-300.jpg"
    file_type = "daily"

    hyperlink = "<td><a href=http://%s:8080/%s/%s>" % (
        station_ip, file_type, img)
    hyperlink += "<img src=http://%s:8080/%s/%s></a></td>" % (
        station_ip, file_type, tn)

    self.assertEqual(CreateHyperlink(station_ip, tn, img, file_type),
                     hyperlink)

    station_ip = "172.17.26.13"
    tn = "20-320.tn.jpg"
    img = "20-320.jpg"
    file_type = "calibration"

    hyperlink = "<td><a href=http://%s:8080/%s/%s>" % (
        station_ip, file_type, img)
    hyperlink += "<img src=http://%s:8080/%s/%s></a></td>" % (
        station_ip, file_type, tn)

    self.assertEqual(CreateHyperlink(station_ip, tn, img, file_type),
                     hyperlink)


if __name__ == "__main__":
  unittest.main()
