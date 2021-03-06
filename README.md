# ProVoice

## Overview 

ProVoice is an intelligent chat assistant designed to give you that 
"perfect thing to say" in response to any text input  (text, tweet, Slack, etc).
This works much like typing suggestions, but is slightly more suggestive and 
also configurable and context aware to fit the particular communications scenario.

For example, assume a friend  tweets the following:

   * "And I'm stuck in another long line at the gas station!"

ProVoice would be able to give you context-sensitive responses based on your mood, time of day, 
your relationship to the sender, etc.

So, if this is your mother, ProVoice might suggest the following response:

   * "Maybe you should break down and get the Tesla!  you deserve it :)"

If it was your college roommate, and you're set to "playful mood" it might suggest:

   * "Are you there for another 6 pack or for fuel?"

## Components

ProVoice consists of the following components:

  * A RESTful Web Application Program Interface (API).   This is the main brain of ProVoice.  You send 
it input, it cranks the repsponse, and returns it to you as a json object.  It's up to you to
    format and render.
    
  * A Test web-based UI where you can test the API 

## Installation & Running

### API

#### Install (one time)  [Linux/MAc] 

Create a python virtual environment.

In the project root folder:

```
python3 -m venv ve-provoice
```

Activate the virtual environment

```
source ve-provoice/bin/activate
```

Install requirements

```
pip install -r requirements
```

Deactivate virtual environment

```
deactivate
```

#### Running the API

Activate the virtual environment

```
source ve-provoice/bin/activate
```

Start the API:

```python
python provoice-api.py
```

Then visit the API, specifying the input `string` and the `model`:

##### Examples

Here we invoke the TestModel:

```python
http://localhost:5000/get_provoice_response?input=New%20york&model=test_provoice
```

Returns:

```json
{
  "model": {
    "description": "A test model for ProVoice to test API integration.", 
    "id": "test_provoice"
  }, 
  "response": "I AM A TEST MODEL AND THIS IS MY ONLY RESPONSE :)"
}
```

And here we invoke the `BasicProvoice` model, which recognizes "New York" and gives an appropriate response:

```html
http://localhost:5000/get_provoice_response?input=New%20york&model=basic_provoice
```

Yields:

```json
{
"model": {
"description": "A simple Provoice model with simple responses.",
"id": "basic_provoice"
},
"response": "Oh I love New York!"
}
```

## Roadmap

   * July 2020 :  Get a basic API up with some very simple responses, assuming a single user.  Focus on an architecture
that is modular and allows expansion based on various capability.
     
   * August 2020 :  Establish multi-tennent/multi-user capability.  Individuals get their own experiences.

   * September 2020:  Add increasingly complex AI modules.  Leverage Alexa and Google Voice APIs.  Search and sentiment.

