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

    def test_go_to_result_page(self):
        self.driver.get("http://localhost:8000/polls/1/")
        a_tag = self.driver.find_element_by_tag_name("a")
        self.assertIn(a_tag.text, "투표 결과 보기")
        a_tag.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/polls/1/results/")

        self.assertIn(self.driver.find_element_by_tag_name("h1").text, "What's up?")
        p_tags = self.driver.find_elements_by_tag_name("ul > p")
        self.assertTrue(
            any('Choice:' in p_tag.text for p_tag in p_tags)
        )
        self.assertTrue(
            any('Vote Count:' in p_tag.text for p_tag in p_tags)
        )