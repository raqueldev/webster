=======
Webster - Website Test Response
=======

.. image:: webster/resources/webster.png
Author: Raquel V

**Disclaimer**

If you have arrived to this project, take into account that this project is my very first Python project
and may not be following the best practices, this project has been done as a practice for using Aiven.io services
so do not take it as an example for your duties although it can inspire you.

-----
Getting Started in Webster
-----

Webster is a system that monitors Website availability over the network,
produce metrics about this and passes these events through Kafka into PostgreSQL db.
Those metrics will be stored:
    - as historical data in a table called: 'webster_metrics_history'
    - as live data with no duplicates in a table called: 'webster_metrics'

Ideally this could run periodically for example by a cronjob or any other scheduler, to simulate that in execution time
I just added a loop in the main.

For this project we will use Aiven instances, like Kafka, and PostgreSQL but feel free to configure all you need
by the following:

-----
Requirements
-----
This are the following technical requirements you would need

    * PostgreSQL Instance
    * Kafka Instance
    * Python

Prepare the list of Urls you want to track. Go to resources/urls.json and add there the list of them, by default
the project comes with some examples (you can skip this part).
For example:
..code:: json
    "websitename": "https://YOURURL/"

Add your certs files into certs folder for your external services like Kafka and PostgreSQL (.pem,cert,key)

Creates a Virtualenv
    make virtualenv

Setup the project
    make setup

Update the new config.ini prepared by the setup and configure your parameters
    You will need: (absolute path)
        - virtualenv
        - Database instance
        - Kafka instance
        - URL of a Json file with your websites to check
        - Path for your logging files

Run your code
    make run

Outcome - Your outcome should be similar to the one below

.. image:: webster/resources/outcome_example.png


----
Troubleshooting
----
I have notice that sometimes there is a lag between producer and consumer, I have not find out yet why, but I think
the consumer is slower for some reason. If this happens to you in your tests, please go to consumer.py
remove the consumer_timeout_ms, run the project, it will catch up eventually and then put back the timeout.
I will continue investigating why it can be.

-----
Missing parts
-----
This project is not covered by test, do not do that! If you are going to implement something similar please do you test.

-----
Attributions
-----
https://developer.aiven.io/
https://kafka-python.readthedocs.io/
https://realpython.com

-----
Contributions
-----
If you wanna contribute in this project please read Contribution_.

.. _CONTRIBUTING:


-----
Code of conduct
-----
Refer to https://www.contributor-covenant.org/ to follow the code of conduct for Open Source projects