from collections import namedtuple
from typing import NoReturn, List
from prettytable import PrettyTable
from language_detection import LanguageDetector
import time

TestCaseData = namedtuple(
    "TestCaseData",
    ["sentence_to_detect_language", "correct_language", "correct_percentage"],
)


class TestLanguageDetector:
    def __init__(self, data_to_test: List[TestCaseData]) -> NoReturn:
        self.data_to_test = data_to_test
        self.result_table = PrettyTable(
            [
                "Sentence to detect language",
                "Predicted language",
                "Correct language",
                "Predicted percentage of matching",
                "Correct percentage of matching",
                "Result of testing",
            ]
        )

    def run_test(self) -> NoReturn:
        start_time = time.time()
        list_of_testing_results = []
        for data_to_test in self.data_to_test:
            list_of_testing_results.append(self._test_case(data_to_test))
        self.result_table.add_rows([[" " for _ in range(6)] for _ in range(3)])
        self.result_table.add_row(
            [
                "Total time:",
                f"{(time.time() - start_time) * 1000:.6f} ms",
                "Count of tests:",
                len(self.data_to_test),
                "All tests:",
                "Passed" if all(list_of_testing_results) else "Failed",
            ]
        )

        print(self.result_table)

    def _test_case(self, test_data: TestCaseData) -> NoReturn:
        result = False
        predicted_language_with_percentage = LanguageDetector.sentence_to_detect_language(
            test_data.sentence_to_detect_language)
        predicted_language_with_percentage = {
            key: value
            for key, value in predicted_language_with_percentage.items()
            if value == max(predicted_language_with_percentage.values())
        }
        vague_detection = "Few languages were detected"
        if len(predicted_language_with_percentage) == 6 and sum(predicted_language_with_percentage.values()) == 0:
            vague_detection = "No language was detected"
        if test_data.correct_percentage == 0:
            if sum(predicted_language_with_percentage.values()) == 0:
                result = True
            else:
                result = False
        else:
            if len(predicted_language_with_percentage) == 6 and sum(predicted_language_with_percentage.values()) == 0:
                result = test_data.correct_language not in predicted_language_with_percentage.keys()
            elif len(predicted_language_with_percentage) != 1:
                result = True
            else:
                if test_data.correct_language == list(predicted_language_with_percentage.keys())[0] and test_data.correct_percentage == int(
                    list(predicted_language_with_percentage.values())[0]
                ):
                    result = True
                else:
                    result = False

        self.result_table.add_row(
            [
                test_data.sentence_to_detect_language,
                vague_detection if len(predicted_language_with_percentage) != 1 else list(predicted_language_with_percentage.keys())[0],
                test_data.correct_language,
                "N/A" if len(predicted_language_with_percentage) != 1 else int(list(predicted_language_with_percentage.values())[0]),
                test_data.correct_percentage,
                "Passed" if result else "Failed",
            ]
        )

        return result


if __name__ == "__main__":
    test_data = [
        TestCaseData(
            sentence_to_detect_language="Hello my name is",
            correct_language="English",
            correct_percentage=75,
        ),
        TestCaseData(
            sentence_to_detect_language="La nostra famiglia",
            correct_language="Few languages were detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="La nostra famiglia come come ! ! ?? composta anche da altre !!2683",
            correct_language="Italian",
            correct_percentage=60,
        ),
        TestCaseData(
            sentence_to_detect_language="La nostra famiglia !! 2 34 5 6 564 come come ?? composta anche da altre due persone, i nostri figli, che ha diciassette anni, e che ha quindici anni, e poi anche , il cane che vive con noi da nove anni, ed ?? parte della famiglia. Viviamo tutti nella nostra splendida casa con un grande giardino.",
            correct_language="Italian",
            correct_percentage=58,
        ),
        TestCaseData(
            sentence_to_detect_language="Manon ! ont 123 tr??s? !!!",
            correct_language="French",
            correct_percentage=33,
            ),
        TestCaseData(
            sentence_to_detect_language="Manon ont tr??s faim et la pendule du salon sonne",
            correct_language="French",
            correct_percentage=30,
        ),
        TestCaseData(
            sentence_to_detect_language="Manon ont tr??s faim et la pendule du salon sonne midi. Ils d??cident d???aller au march?? pour acheter les ingr??dients qu???ils vont cuisiner.Ils ont besoin d???une salade verte, de 6 tomates",
            correct_language="French",
            correct_percentage=36,
        ),
        TestCaseData(
            sentence_to_detect_language="Ich komme aus",
            correct_language="German",
            correct_percentage=66,
        ),
        TestCaseData(
            sentence_to_detect_language="Ich komme aus ??sterreich und lebe seit drei Jahren in",
            correct_language="German",
            correct_percentage=50,
        ),
        TestCaseData(
            sentence_to_detect_language="Ich komme aus ??sterreich und lebe seit drei Jahren in Deutschland. Ich bin 15 Jahre alt und habe zwei Geschwister: Meine Schwester ist 13 Jahre alt, mein Bruder ist 18 Jahre alt. Wir wohnen mit unseren Eltern in einem Haus in der N??he von M??nchen. Meine Mutter ist K??chin, mein Vater arbeitet in einer Bank.",
            correct_language="German",
            correct_percentage=36,
        ),
        TestCaseData(
            sentence_to_detect_language="She recently took",
            correct_language="English",
            correct_percentage=66,
        ),
        TestCaseData(
            sentence_to_detect_language="She recently took a weekend trip to Los Angeles, California.",
            correct_language="English",
            correct_percentage=50,
        ),
        TestCaseData(
            sentence_to_detect_language="She recently took a weekend trip to Los Angeles, California. Los Angeles is a coastal city situated along the Pacific Ocean. Many celebrities earned their claim to fame here. Although the town offers many attractions centered around Hollywood culture, there is a lot to see and visit in Los Angeles.",
            correct_language="English",
            correct_percentage=54,
        ),
        TestCaseData(
            sentence_to_detect_language="Mi nueva casa",
            correct_language="Spanish",
            correct_percentage=66,
        ),
        TestCaseData(
            sentence_to_detect_language="Mi nueva casa est?? en una calle ancha que tiene",
            correct_language="Spanish",
            correct_percentage=60,
        ),
        TestCaseData(
            sentence_to_detect_language="Mi nueva casa est?? en una calle ancha que tiene muchos ??rboles. El piso de arriba de mi casa tiene tres dormitorios y un despacho para trabajar. El piso de abajo tiene una cocina muy grande, un comedor con una mesa y seis sillas, un sal??n con dos sof??s verdes, una televisi??n y cortinas. Adem??s, tiene una peque??a terraza con piscina donde puedo tomar el sol en verano.",
            correct_language="Spanish",
            correct_percentage=57,
        ),
        TestCaseData(
            sentence_to_detect_language="Muitos depois diante",
            correct_language="Portuguese",
            correct_percentage=66,
        ),
        TestCaseData(
            sentence_to_detect_language="Muitos depois diante do pelot??o de fuzilamento, Aureliano Buend??a hav??a",
            correct_language="Portuguese",
            correct_percentage=30,
        ),
        TestCaseData(
            sentence_to_detect_language="Muitos depois diante do pelot??o de fuzilamento, Aureliano Buend??a hav??a de aquela o seu pai o levou para o gelo",
            correct_language="Portuguese",
            correct_percentage=55,
        ),
        TestCaseData(
            sentence_to_detect_language="????????????",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="f8cdef31-a31e-4b4a-93e4-5f571e91255a",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="test-car-machine-name-ixioo123@gmail.com",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="DefaultEndpointsProtocol=https;AccountName=testixiooazure;AccountKey=FlfFygeoRpjoJ6as1xB/Zk",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="9k7dhowew7l0hsy",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="ixioocontainer",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="iXiooDotCom!",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="f21f80c8-3fbb-4007-9154-8b64359e9b91",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="????????????, ???????? ?????????? ????????",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="list_of_words_in_unidentified_language = self.sentence_to_detect_language.split(self.list_of_words_in_unidentified_language = list_of_words_in_unidentified_language",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="326854547249-98gjh75luq2a8gah4vp9u8pp3me1d4vf.apps.googleusercontent.com",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="ook leuk jou te ontmoeten",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="trevligt att tr??ffa dig med",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="hyggelig ?? m??te deg ogs??",
            correct_language="No language was detected",
            correct_percentage="N/A",
        ),
        TestCaseData(
            sentence_to_detect_language="te?? mi??o ci?? pozna??", correct_language="No language was detected",
            correct_percentage="N/A"
        )]
    TestLanguageDetector(data_to_test=test_data).run_test()