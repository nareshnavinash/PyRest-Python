# PyRest-Python
PyRest is an automation framework to test REST API endpoints. This framework is built in Python and inspired from the simplicity of Karate framework by Intuit and snapshot mode from Jest framework by Facebook.

The supported markers are the following:

Marker | Description
------ | -----------
`$null` | Expects actual value to be `null`, and the data element or JSON key *must* be present
`$notnull` | Expects actual value to be not-`null`
`$array` | Expects actual value to be a JSON array
`$object` | Expects actual value to be a JSON object
`$boolean` | Expects actual value to be a boolean `true` or `false`
`$number` | Expects actual value to be a number
`$string` | Expects actual value to be a string
`$uuid` | Expects actual (string) value to conform to the UUID format
 