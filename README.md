# PyRest-Python
PyRest is an automation framework to test REST API endpoints. This framework is built in Python and inspired from the simplicity of [Karate framework by Intuit](https://github.com/intuit/karate) and snapshot mode from [Jest framework by Facebook](https://jestjs.io/).



[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-yellow.svg)](https://www.python.org/)
[![StackOverflow](http://img.shields.io/badge/Stack%20Overflow-Ask-blue.svg)]( https://stackoverflow.com/users/10505289/naresh-sekar )
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![email me](https://img.shields.io/badge/Contact-Email-green.svg)](mailto:nareshnavinash@gmail.com)


![alt text](Library/pyrest.png)


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
 