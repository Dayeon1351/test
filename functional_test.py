from selenium import webdriver
import unittest


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        path = "./chromedriver"
        self.driver = webdriver.Chrome(path)

    def tearDown(self):
        self.driver.quit()

    def test_go_to_detail_page(self):
        self.driver.get("http://localhost:8000/polls/")
        a_tag = self.driver.find_elements_by_tag_name("li > a")[1]
        self.assertIn("What's up?", a_tag.text)
        a_tag.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/polls/1/")

        self.assertIn(self.driver.find_element_by_tag_name("h1").text, "What's up?")
        li_tags = self.driver.find_elements_by_tag_name("ul > li")
        self.assertTrue(
            any(li_tag.text == 'choice!' for li_tag in li_tags)
        )
        self.assertTrue(
            any(li_tag.text == 'choice 2!' for li_tag in li_tags)
        )