import time
import unittest

from storm_scheduler import scheduler


class TestScheduler(unittest.TestCase):
    def test_idle_wait(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        task1 = schedule.task(lambda: None).every(0.01)
        task2 = schedule.task(lambda: None).every(2)
        task3 = schedule.task(lambda: None).every(3)

        time.sleep(0.01)

        schedule._loop()

        self.assertEqual(0.01, schedule._idle_wait())
        self.assertIsNotNone(task1._next_run)
        self.assertGreaterEqual(1, int(task2.next_run))
        self.assertGreaterEqual(2, int(task3.next_run))

    def test_string_representation(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        def hello_world():
            pass

        task1 = schedule.task(hello_world).every(3)
        task2 = schedule.task(hello_world).every(6)
        task3 = schedule.task(hello_world).every(9)

        self.assertEqual('<Task: hello_world object schedule to run in 3.0s>', str(task1))
        self.assertEqual('<Task: hello_world object schedule to run in 6.0s>', str(task2))
        self.assertEqual('<Task: hello_world object schedule to run in 9.0s>', str(task3))
