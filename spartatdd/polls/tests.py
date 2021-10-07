from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
import datetime

# Create your tests here.
def create_question(question_text, timedelta_from_now):
    """
    Create a question with the given `question_text` and `timedelta_from_now`
    """
    time = timezone.now() + timedelta_from_now
    question = Question(question_text=question_text, pub_date=time)
    question.save()
    return question
    
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          timedelta_from_now=datetime.timedelta(days=5))
        response = self.client.get(f'/polls/{future_question.id}/')
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Future question.',
                                        timedelta_from_now=datetime.timedelta(days=-5))
        response = self.client.get(f'/polls/{past_question.id}/')
        self.assertContains(response, past_question.question_text)

    def test_past_question_with_choices(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's choices.
        """
        past_question = create_question(question_text='Future question.',
                                        timedelta_from_now=datetime.timedelta(days=-5))
        choice1 = Choice(question=past_question, choice_text="choice 1")
        choice1.save()
        choice2 = Choice(question=past_question, choice_text="choice 2")
        choice2.save()
        response = self.client.get(f'/polls/{past_question.id}/')

        self.assertContains(response, choice1.choice_text)
        self.assertContains(response, choice2.choice_text)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_has_a_href_link(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page with a href link.
        """

        question = create_question(question_text="Recent question.", timedelta_from_now=datetime.timedelta(days=-30))
        response = self.client.get("/polls/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="/polls/{question.id}/"')

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", timedelta_from_now=datetime.timedelta(days=-30))
        question2 = create_question(question_text="Past question 2.", timedelta_from_now=datetime.timedelta(days=-5))

        response = self.client.get("/polls/")
        self.assertQuerysetEqual(
            response.context['question_list'],
            [question2, question1],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Past question.", timedelta_from_now=datetime.timedelta(days=30))
        response = self.client.get("/polls/")
        self.assertContains(response, "등록된 설문조사가 없습니다.")
        self.assertQuerysetEqual(response.context['question_list'], [])


    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", timedelta_from_now=datetime.timedelta(days=-30))
        response = self.client.get("/polls/")

        self.assertQuerysetEqual(
            response.context['question_list'],
            [question],
        )

    
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get("/polls/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "등록된 설문조사가 없습니다.")
        self.assertQuerysetEqual(response.context['question_list'], [])
    
    def test_published_recently_has_new_mark(self):
        """
        Questions with a recent pub_date are displayed on the
        index page with [New] mark.
        """

        question = create_question(question_text="Recent question.", timedelta_from_now=datetime.timedelta(hours=-8))
        response = self.client.get("/polls/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"[New]")
        self.assertQuerysetEqual(response.context['question_list'], [question])
    
