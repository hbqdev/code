import unittest
import stations

TEST_YAML_FILE="./testdata/stations_test.yaml"

class TestCases(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testStationSort(self):
    sbs_dict = {"sbs1": "172.17.26.1", "sbs10": "172.17.26.10",
                "sbs433": "172.17.26.4", "sbs2": "172.17.26.2"}
    sbs_list = ["sbs1", "sbs2", "sbs10", "sbs433"]
    self.assertEqual(stations.GetSortedHostnames(sbs_dict), sbs_list)

    sbs_dict = {"sbs134": "172.17.26.134", "sbs213": "172.17.26.213",
                "sbs156": "172.17.26.156", "sbs98": "172.17.26.98"}
    sbs_list = ["sbs98", "sbs134", "sbs156", "sbs213"]
    self.assertEqual(stations.GetSortedHostnames(sbs_dict), sbs_list)

    sbs_dict = {}
    sbs_list = []
    self.assertEqual(stations.GetSortedHostnames(sbs_dict), sbs_list)

  def testStationImport(self):
    test_station = stations.Stations(TEST_YAML_FILE)
    station_dict = test_station.GetStationIPs(station_types=["not-valid"])
    self.assertEqual(station_dict, {})
    station_dict = test_station.GetStationIPs(station_types=["prod"])
    sbs_dict = {"sbs1": "172.17.26.1", "sbs10": "172.17.26.10",
                "sbs2": "172.17.26.2"}
    self.assertEqual(station_dict, sbs_dict)
    station_dict = test_station.GetStationIPs(station_types=["prod", "canary"])
    sbs_dict = {"sbs1": "172.17.26.1", "sbs10": "172.17.26.10",
                "sbs2": "172.17.26.2", "sbs11": "172.17.26.11",
                "sbs12": "172.17.26.12"}
    self.assertEqual(station_dict, sbs_dict)


if __name__ == "__main__":
  unittest.main()
