import unittest
from src.DFPlayer import DFPlayer
from time import sleep


class TestDFPlayer(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    def test_connection(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        self.assertEqual(dfplayer.get_status(), 512)

    def test_specific_play(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        if dfplayer.num_files() == 0:
            raise Exception('File empty')
        dfplayer.play(track=1)
        self.assertEqual(dfplayer.get_status(), 513)

    def test_random_play(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.random()
        self.assertEqual(dfplayer.get_status(), 513)

    def test_pause(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.random()
        sleep(5)
        dfplayer.pause()
        self.assertEqual(dfplayer.get_status(), 514)

    def test_stop(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.random()
        sleep(5)
        dfplayer.pause()
        self.assertEqual(dfplayer.get_status(), 514)

    def test_next(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.random()
        sleep(5)
        dfplayer.next()
        self.assertEqual(dfplayer.get_status(), 513)

    def test_previous(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.random()
        sleep(5)
        dfplayer.next()
        self.assertEqual(dfplayer.get_status(), 513)

    def test_volume_up(self):
        # current volume is 50
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.volume_up()
        self.assertEqual(dfplayer.get_volume(), 53)

    def test_volume_down(self):
        # current volume is 50
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.volume_down()
        self.assertEqual(dfplayer.get_volume(), 46)

    def test_set_volume(self):
        # current volume is 50
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.set_volume(60)
        self.assertEqual(dfplayer.get_volume(), 60)

    def test_set_eq(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.set_eq(DFPlayer.EQ_ROCK)
        self.assertEqual(dfplayer.get_eq(), DFPlayer.EQ_ROCK)

    # def test_standby(self):
    #     dfplayer = DFPlayer('/dev/ttyUSB0')
    #     dfplayer.set_standby()
    #     self.assertEqual(dfplayer.get_status(), 2)
    #     dfplayer.set_standby(False)

    def test_reset(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        dfplayer.reset()
        self.assertEqual(dfplayer.get_status(), 512)

    def test_count_files(self):
        dfplayer = DFPlayer('/dev/ttyUSB0')
        files = dfplayer.num_files()
        self.assertTrue(files)


if __name__ == '__main__':
    unittest.main()
