import unittest

from hexarquia_totemica import create_totems, determine_dominant_totem


class TestHexarquiaTotemica(unittest.TestCase):
    def setUp(self):
        self.totems = create_totems()

    def test_invasion_triggers_oso_pardo(self):
        dominant = determine_dominant_totem(
            "Siento invasion en mi territorio", self.totems
        )
        self.assertEqual(dominant.name, "Oso Pardo")

    def test_caos_triggers_ogro(self):
        dominant = determine_dominant_totem("Mucho caos e incertidumbre", self.totems)
        self.assertEqual(dominant.name, "Ogro")

    def test_no_trigger_defaults_highest_dominance(self):
        dominant = determine_dominant_totem("Nada relevante", self.totems)
        self.assertEqual(dominant.name, "Oso Pardo")


if __name__ == "__main__":
    unittest.main()
