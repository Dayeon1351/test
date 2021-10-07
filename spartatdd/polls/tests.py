from django.test import TestCase

# Create your tests here.

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get("/polls/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "등록된 설문조사가 없습니다.")
        self.assertQuerysetEqual(response.context['question_list'], [])