Mutalyzer HGVS Parser
=====================

.. image:: https://img.shields.io/github/last-commit/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser/graphs/commit-activity
.. image:: https://readthedocs.org/projects/mutalyzer-spdi-parser/badge/?version=latest
   :target: https://mutalyzer-spdi-parser.readthedocs.io/en/latest
.. image:: https://img.shields.io/github/release-date/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser/releases
.. image:: https://img.shields.io/github/release/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser/releases
.. image:: https://img.shields.io/pypi/v/mutalyzer-spdi-parser.svg
   :target: https://pypi.org/project/mutalyzer-spdi-parser/
.. image:: https://img.shields.io/github/languages/code-size/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser
.. image:: https://img.shields.io/github/languages/count/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser
.. image:: https://img.shields.io/github/languages/top/mutalyzer/spdi-parser.svg
   :target: https://github.com/mutalyzer/spdi-parser
.. image:: https://img.shields.io/github/license/mutalyzer/spdi-parser.svg
   :target: https://raw.githubusercontent.com/mutalyzer/spdi-parser/master/LICENSE.md

----

Package to syntax check and convert SPDI descriptions into a dictionary model.


Quick start
-----------

Parse and convert a description from the command line:

.. code-block:: console

    $ mutalyzer_spdi_parser -cs "NG_012337.3:10:C:T"
    {
      "seq_id": "NG_012337.3",
      "position": 10,
      "deleted_sequence": "C",
      "inserted_sequence": "T"
    }

    $ mutalyzer_spdi_parser -ch "NG_012337.3:10:C:T"
    {
      "type": "description_dna",
      "reference": {
        "id": "NG_012337.3"
      },
      "variants": [
        {
          "type": "deletion_insertion",
          "location": {
            "type": "range",
            "start": {
              "type": "point",
              "position": 10
            },
            "end": {
              "type": "point",
              "position": 11
            }
          },
          "deleted": [
            {
              "sequence": "C",
              "source": "description"
            }
          ],
          "inserted": [
            {
              "sequence": "T",
              "source": "description"
            }
          ]
        }
      ]
    }


The ``to_hgvs_internal_model()`` function can be used to obtain the equivalent
HGVS dictionary model (deletion insertion variants with internal locations and
indexing):

.. code:: python

    >>> from mutalyzer_spdi_parser import to_hgvs_internal_model
    >>> model = to_hgvs_internal_model("NG_012337.3:10:C:T")
    >>> model['reference']
    {'id': 'NG_012337.3'}
