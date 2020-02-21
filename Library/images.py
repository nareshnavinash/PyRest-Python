import imgcompare
import allure
import os
import diffimg
from Library.variable import Var


class Img:

    @staticmethod
    def is_equal(image1, image2):
        image1_path = Img.root_path() + "/Data/Images/" + image1
        image2_path = Img.root_path() + "/reports/images/" + image2
        result = imgcompare.is_equal(image1_path, image2_path)
        allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
        allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
        if not result:
            image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
            allure.step("Difference Percentage for comparing images is" + image_diff_percent)
            diff_img_name = "diff_" + image1 + image2 + ".png"
            diff_img_path = Img.root_path() + "/reports/images/" + diff_img_name
            diffimg.diff(image1_path, image2_path, delete_diff_file=False,
                         diff_img_file=diff_img_path, ignore_alpha=False)
            allure.attach.file(diff_img_path, name=diff_img_name, attachment_type=allure.attachment_type.PNG)
        return result

    @staticmethod
    def is_equal_with_tolerance(image1, image2, tolerance=Var.current("tolerance")):
        image1_path = Img.root_path() + "/Data/Images/" + image1
        image2_path = Img.root_path() + "/reports/images/" + image2
        result = imgcompare.is_equal(image1_path, image2_path, tolerance=tolerance)
        allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
        allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
        if not result:
            image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
            allure.step("Difference Percentage for comparing images is" + image_diff_percent)
            diff_img_name = "diff_" + image1 + image2 + ".png"
            diff_img_path = Img.root_path() + "/reports/images/" + diff_img_name
            diffimg.diff(image1_path, image2_path, delete_diff_file=False,
                         diff_img_file=diff_img_path, ignore_alpha=False)
            allure.attach.file(diff_img_path, name=diff_img_name, attachment_type=allure.attachment_type.PNG)
        return result

    @staticmethod
    def root_path():
        return os.path.dirname(os.path.abspath(__file__)).replace("/Library", "")
