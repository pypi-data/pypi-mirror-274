"""
Module for converting SPDI descriptions and lark parse trees
to their equivalent dictionary models.
"""

from lark import Transformer

from .spdi_parser import parse


def to_spdi_model(description):
    """
    Convert an SPDI description to a dictionary model.
    :arg str description: SPDI description.
    :returns: Description dictionary model.
    :rtype: dict
    """
    return parse_tree_to_model(parse(description))


def to_hgvs_internal_model(description):
    """
    Convert an SPDI description to an internal HGVS dictionary model
    (delins variants with internal locations).
    :arg str description: SPDI description.
    :returns: HGVS internal dictionary model.
    :rtype: dict
    """
    return _to_hgvs_internal(parse_tree_to_model(parse(description)))


def parse_tree_to_model(parse_tree):
    """
    Convert a parse tree to a dictionary model.
    :arg lark.Tree parse_tree: SPDI description equivalent parse tree.
    :returns: Description dictionary model.
    :rtype: dict
    """
    return Converter().transform(parse_tree)


class Converter(Transformer):
    def description(self, children):
        output = {k: v for d in children for k, v in d.items()}
        output["seq_id"] = output["id"]
        output.pop("id")
        return output

    def reference(self, children):
        output = {"id": children[0]["seq_id"]}
        if len(children) == 2:
            output["id"] = children[0]["seq_id"]
            output["selector"] = children[1]
        return output

    def deleted_sequence(self, children):
        return {"deleted_sequence": children[0]}

    def inserted_sequence(self, children):
        return {"inserted_sequence": children[0]}

    def position(self, children):
        return {"position": children[0]}

    def deleted_length(self, children):
        return {"deleted_length": children[0]}

    def sequence(self, children):
        return children[0]

    def NUMBER(self, name):
        return int(name)

    def D_SEQUENCE(self, name):
        return name.value

    def R_SEQUENCE(self, name):
        return name.value

    def P_SEQUENCE(self, name):
        return name.value

    def ID(self, name):
        return {"seq_id": name.value}


def _to_hgvs_internal(s_m):
    m = {"type": "description_dna", "reference": {"id": s_m["seq_id"]}}
    if s_m.get("selector"):
        m["reference"]["selector"]= s_m["selector"]

    v = {"type": "deletion_insertion"}
    if s_m.get("deleted_sequence"):
        v["location"] = _range(
            s_m["position"], s_m["position"] + len(s_m["deleted_sequence"])
        )
        v["deleted"] = [{"sequence": s_m["deleted_sequence"], "source": "description"}]
    elif s_m.get("deleted_length"):
        v["location"] = _range(s_m["position"], s_m["position"] + s_m["deleted_length"])
    else:
        v["location"] = _range(s_m["position"], s_m["position"])

    v["inserted"] = []
    if s_m.get("inserted_sequence"):
        v["inserted"].append({"sequence": s_m["inserted_sequence"], "source": "description"})

    if not s_m.get("inserted_sequence") and not (
        s_m.get("deleted_sequence") or s_m.get("deleted_length")
    ):
        v["location"] = _range(s_m["position"], s_m["position"] + 1)
        v["inserted"] = [
            {
                "location": _range(s_m["position"], s_m["position"] + 1),
                "source": "reference",
            }
        ]

    m["variants"] = [v]
    return m


def _range(s, e):
    return {
        "type": "range",
        "start": {
            "type": "point",
            "position": s,
        },
        "end": {
            "type": "point",
            "position": e,
        },
    }


def _point(p):
    return {
        "type": "point",
        "position": p,
    }
