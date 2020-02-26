# PyRest-Python
PyRest is an automation framework to test REST API endpoints. This framework includes methods to download the image files from the rest API and then compare with the stored image files. This framework is built in Python and inspired from the simplicity of [Karate framework by Intuit](https://github.com/intuit/karate) and snapshot mode from [Jest framework by Facebook](https://jestjs.io/).

Snapshot mode is added even for the image file comparison.


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-yellow.svg)](https://www.python.org/)
[![StackOverflow](http://img.shields.io/badge/Stack%20Overflow-Ask-blue.svg)]( https://stackoverflow.com/users/10505289/naresh-sekar )
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![email me](https://img.shields.io/badge/Contact-Email-green.svg)](mailto:nareshnavinash@gmail.com)


![alt text](Library/pyrest.png)


## Supports
* Rest API automation
* Allure reports
* Jenkins Integration
* Modes of run via CLI command
* Docker Execution
* Testdata driven tests
* Multi Thread run
* Snap Mode to replace the response data as the test data
* Static code analyser

## Setup
* Clone this repository
* Navigate to the cloned folder
* To install the dependencies in MAC we use Homebrew version manager install (using)[https://brew.sh/]
* Once brew is installed install python by `brew install python3`
* To get additional dependencies of python like pip3, do `brew postinstall python3`
* Install the required packages needed for this framework using `pip3 install -r requirements.txt`

## To Run the tests
For a simple run of all the test files in normal mode, try

```
pytest
```

To run the tests in snap mode (to save the UI texts to the dynamic file)
```
snap=1 pytest
```
Once the changes are saved to the file run the tests with `pytest` to get the test running against the saved data. To verify this feature I intentionally added two locator texts which will be changing continuously.

To Run the tests in parallel mode or multi thread run for the available test files, try (To have parallel run you need to have atleast 2 tests inside your folder structure)

```
pytest -s -v -n=2
```

## To open allure results
Allure is a open source framework for reporting the test runs. To install allure in mac, use the following steps

```
brew cask install adoptopenjdk
brew install allure
```

To view the results for the test run, use

```
allure serve reports/allure
```


## Reports
For better illustration on the testcases, allure reports has been integrated. Allure reports can also be integrated with jenkins to get a dashboard view. Apart from allure, pytest's default reporting such as html file has been added to the `reports/` folder.

If there is a failure while comparing the images, allure report will have all the files attached to it. The difference between the two images is generated in run time and attached to the allure report for our referenece.

![alt text](Library/diff_image.png)
 

## Jenkins Integration with Docker images
Get any of the linux with python docker image as the slaves in jenkins and use the same for executing the UI automation with this framework (Sample docker image - `https://hub.docker.com/_/python`). From the jenkins bash Execute the following to get the testcases to run,

```
#!/usr/bin/python3
python --version
cd <path_to_the_project>
pip3 install -r requirements.txt
snap=1 pytest -s -v -n 4
```

In Jenkins pipeline, try to add the following snippet to execute the tests,

```
pipeline {
    agent { docker { image 'python:3.7.6' } }
    stages {
        stage('test') {
            steps {
                sh 'python --version'
                sh 'cd project/'
                sh 'pip3 install -r requirements.txt'
                sh 'pytest -s -v -n 4'
            }
        }
    }
}
```












The supported markers are the following:

Marker | Description
------ | -----------
`$notnull` | Expects actual value to be not-`null`
`$array` | Expects actual value to be a JSON array
`$object` | Expects actual value to be a JSON object
`$boolean` | Expects actual value to be a boolean `true` or `false`
`$number` | Expects actual value to be a number
`$string` | Expects actual value to be a string
`$uuid` | Expects actual (string) value to conform to the UUID format
 
 
 
 
### Data sets:

In order to have distinguished set of data I have used three types of data.

* **Global** - Global configuration for the whole project. Here mode of run, browsers to use, browser configurations etc., are specified.
* **Test Data** - This is to store the module level data. Ideally for each test file we need to have a test data file, but that depends on the requirement.
* **Dynamic Data** - This is to store the dynamic data. Files in this folder are supposed to change when we run with `snap=1 pytest`. This is separated from the other data files so that other static files are not disturbed during the run.
* **Images** - This folder is to store all the image files that are needed to compare with the response Image files 


## Static code analyser:

For static code analyser I used flake8. To check the configurations view (.flake8)[.flake8] file. To check on the code status execte,

```
flake8
```

currently there are `0` vulnerabilities with this project.


## Built With

* [pytest](https://docs.pytest.org/en/latest/) - Core test framework
* [flake8](https://pypi.org/project/flake8/) - Static code analyser
* [pytest-xdist](https://pypi.org/project/pytest-xdist/) - To run pytest in parallel mode
* [Allure pytest](https://pypi.org/project/allure-pytest/) - For Detailed reporting
* [Image_Compare](https://pypi.org/project/imgcompare/) - To compare two image files
* [Diff_Image](https://pypi.org/project/diffimg/) - To generate image file with difference between two images

## Contributing

1. Clone the repo!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Create a pull request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code of conduct, and the process for submitting pull requests.

## Authors

* **[Naresh Sekar](https://github.com/nareshnavinash)**

## License

This project is licensed under the GNU GPL-3.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* To all the open source contributors whose code has been referred in this project.
