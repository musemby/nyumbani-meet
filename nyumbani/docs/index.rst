.. Zoloni API documentation master file, created by
   sphinx-quickstart on Fri Jun  3 13:50:09 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Zoloni API's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
============


Getting Started
===============
A few things will need. ``Client ID`` and ``Client Secret`` to follow the authetication and authorization process below.
You will also need an organization ID that will be required as the param ``current_org_id`` in the actual API requests.
Please reach out to hello@zoloni.com to get these before continuing. When going live do not forget to get Production
different credentials.

* Base Staging API URL: https://api.staging.zoloni.com
* Base Production API URL: https://api.zoloni.com

The code examples below are in python. They are meant to give you an idea of how you might do the language specific
stuff in your language of choice.


Geting the Access Token
-----------------------
1. Concatenate the client id and the client secret with a colon(:)

.. code-block:: python

   client_id = 'ejUHzNFx5lAuACvmjAMceL0ReJEX5rlhO2eAwvsq'
   client_secret = 'c52BQ2NUEVrelxbeExmbfFPuKJJxt6Nt3bQ6vvT05ci83CAbJ3daWd08ABeRORaLTReAbRcTQebEJscuGOghWuGQwCoiUjVgdY4FqesHp99hkUZCkdYPyFyJsKEPvxxG'

   credential = "{0}:{1}".format(client_id, client_secret)

2. Base 64 encode the resulting ``credential`` from above. Ensure you encode it as ``utf-8`` first.

.. code-block:: python

   import base64

   b64_credential_string = base64.b64encode(credential.encode("utf-8"))

3. Send a ``POST`` request to ``/o/token/``

   `Headers`

   ``Authorization: Basic b64_credential_string`` (from 2 above)

   `Request Body(JSON)`

   .. code-block:: json

      {
         "grant_type": "client_credentials"
      }

   `Response`

   .. code-block:: json

      {
         "access_token": "FJKLimhq8seXdH1a7JtlIzHh9Mujsb",
         "expires_in": 36000,
         "token_type": "Bearer",
         "scope": "delivery_requests"
      }

Grab the access token above. You will need it to authenticate all requests going forward.
By default the token expires in 36000 seconds(10 hours). To get a new one, simply repeat the process above.

Authenticating Requests
-----------------------

When making requests include the ``access_token`` from above in the header as a `Bearer Token` like so:

``Authorization: Bearer FJKLimhq8seXdH1a7JtlIzHh9Mujsb``

Now let's jump to the good part.

Zoloni API Go Live` and request
for the production credentials and details which you you will just replace and be good to go!