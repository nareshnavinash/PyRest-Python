import imgcompare
import allure
import os
from Library.variable import Var


class Img:

    @staticmethod
    def is_equal(image1, image2):
        image1_path = os.path.dirname(os.path.abspath(__file__)).replace("/Library", "") + "/Data/Images/" + image1
        image2_path = os.path.dirname(os.path.abspath(__file__)).replace("/Library", "") + "/reports/images/" + image2
        result = imgcompare.is_equal(image1_path, image2_path)
        allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
        allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
        image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
        allure.step("Difference Percentage for comparing images is" + image_diff_percent)
        return result

    @staticmethod
    def is_equal_with_tolerance(image1, image2, tolerance=Var.current("tolerance")):
        image1_path = os.path.dirname(os.path.abspath(__file__)).replace("/Library", "") + "/Data/Images/" + image1
        image2_path = os.path.dirname(os.path.abspath(__file__)).replace("/Library", "") + "/reports/images/" + image2
        result = imgcompare.is_equal(image1_path, image2_path, tolerance=tolerance)
        allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
        allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
        image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
        allure.step("Difference Percentage for comparing images is" + image_diff_percent)
        return result
