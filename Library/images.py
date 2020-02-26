import imgcompare
import allure
import os
import diffimg
import requests
from Library.variable import Var


class Img:

    @staticmethod
    def download_image(url, name):
        with allure.step("Downloading image from the URL: " + url):
            response = requests.get(url, stream=True)
            image_path = Img.root_path() + "/reports/images/" + name + ".png"
            with open(image_path, "wb") as image:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        image.write(chunk)
            allure.attach.file(image_path, name="downloaded_image: " + name, attachment_type=allure.attachment_type.PNG)

    @staticmethod
    def is_equal(image1, image2):
        with allure.step("Comparing two images"):
            try:
                image1_path = Img.root_path() + "/Data/Images/" + image1 + ".png"
                image2_path = Img.root_path() + "/reports/images/" + image2 + ".png"
                result = imgcompare.is_equal(image1_path, image2_path)
                allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
                allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.step("Exception happened while comparing the image: " + str(e))
                result = False
        if not result:
            if Var.env("snap") == "1":
                with allure.step("Copying the response file to the source file"):
                    Img.copy_image(image1_path, image2_path)
            with allure.step("Attaching the diff image file"):
                image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
                allure.step("Difference Percentage for comparing images is" + str(image_diff_percent))
                diff_img_name = "diff_" + image1 + image2 + ".png"
                diff_img_path = Img.root_path() + "/reports/images/" + diff_img_name
                diffimg.diff(image1_path, image2_path, delete_diff_file=False,
                             diff_img_file=diff_img_path, ignore_alpha=False)
                allure.attach.file(diff_img_path, name=diff_img_name, attachment_type=allure.attachment_type.PNG)
        assert (result is True), "Compared images are not equal"

    @staticmethod
    def is_equal_with_tolerance(image1, image2, tolerance=Var.current("tolerance")):
        with allure.step("Comparing two images with tolerance: " + tolerance):
            image1_path = Img.root_path() + "/Data/Images/" + image1
            image2_path = Img.root_path() + "/reports/images/" + image2
            result = imgcompare.is_equal(image1_path, image2_path, tolerance=tolerance)
            allure.attach.file(image1_path, name=image1, attachment_type=allure.attachment_type.PNG)
            allure.attach.file(image2_path, name=image2, attachment_type=allure.attachment_type.PNG)
        if not result:
            if Var.env("snap") == "1":
                with allure.step("Copying the response file to the source file"):
                    Img.copy_image(image2_path, image1_path)
            with allure.step("Attaching the diff image file"):
                image_diff_percent = imgcompare.image_diff_percent(image1_path, image2_path)
                allure.step("Difference Percentage for comparing images is" + image_diff_percent)
                diff_img_name = "diff_" + image1 + image2 + ".png"
                diff_img_path = Img.root_path() + "/reports/images/" + diff_img_name
                diffimg.diff(image1_path, image2_path, delete_diff_file=False,
                             diff_img_file=diff_img_path, ignore_alpha=False)
                allure.attach.file(diff_img_path, name=diff_img_name, attachment_type=allure.attachment_type.PNG)
        assert (result is True), "Compared images are not equal even with tolerance"

    @staticmethod
    def root_path():
        return os.path.dirname(os.path.abspath(__file__)).replace("/Library", "")

    @staticmethod
    def copy_image(source, destination):
        file = open(source, "wb")
        with open(destination, "rb") as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                file.write(byte)
