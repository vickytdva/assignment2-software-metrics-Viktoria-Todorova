import unittest
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By

ORIGINAL_URL = 'https://en.wikipedia.org/wiki/Software_metric'
CYCLES = 10

class TestPerformanceMetrics(unittest.TestCase):
    
    def setUp(self):
        self.url = ORIGINAL_URL
        self.cycles = CYCLES

    def test_performance(self):
        raw_data = defaultdict(list)

        for _ in range(self.cycles):
            opts = webdriver.ChromeOptions()
            opts.add_argument("--incognito")
            driver = webdriver.Chrome(options=opts)
            driver.get(self.url)
            title = driver.find_element(By.CSS_SELECTOR, "#firstHeading > span")
            self.assertIn('Software metric', title.text)
            script = "return window.performance.getEntries().map(x => [x.name, x.duration])"
            data = driver.execute_script(script)

            for key, value in data:
                raw_data[key].append(value)
            
            driver.quit()

        raw_json_string = json.dumps(raw_data, indent=4)
        with open("rawData.json", 'w', encoding='utf8') as file:
            file.writelines(raw_json_string)

        processed_data = defaultdict(list)

        for key, values in raw_data.items():
            non_zero_values = list(filter(lambda x: x != 0, values))
            if non_zero_values:
                average = sum(non_zero_values) / len(non_zero_values)
                processed_data[key].append(average)
            else:
                processed_data[key].append(0)

        processed_json_string = json.dumps(processed_data, indent=4)
        with open("processedData.json", 'w', encoding='utf8') as file:
            file.writelines(processed_json_string)

    def tearDown(self):
        print("Test completed.")

if __name__ == "__main__":
    unittest.main()