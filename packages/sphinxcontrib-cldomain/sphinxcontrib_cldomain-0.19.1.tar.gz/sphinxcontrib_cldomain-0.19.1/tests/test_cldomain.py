# -*- coding: utf-8 -*-
# cldomain is a Common Lisp domain for the Sphinx documentation tool.
# Copyright (C) Russell Sim <russell.sim@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sphinx import addnodes

from sphinxcontrib.cldomain import cldomain

from .support.nodes import node_to_dict


def test_local_atom():
    # Test public symbols
    assert cldomain.local_atom("foo", "foo:bar") == "bar"
    assert cldomain.local_atom("fooo", "foo:bar") == "foo:bar"

    # Test private symbols
    assert cldomain.local_atom("foo", "foo::bar") == "bar"
    assert cldomain.local_atom("fooo", "foo::bar") == "foo::bar"


def test_parse_specializer_arguments():
    """Test parsing the user input for specializers."""
    assert cldomain.parse_specializer_argument(
        "(eql tag) :test common-lisp:t common-lisp:t", "cl-git"
    ) == [
        ["EQL", "CL-GIT:TAG"],
        ["EQL", "KEYWORD:TEST"],
        "COMMON-LISP:T",
        "COMMON-LISP:T",
    ]


def test_specializer_to_str():
    """Test parsing the user input for specializers."""
    assert (
        cldomain.specializer_to_str(
            [
                ["EQ", "CL-GIT:TAG"],
                ["EQ", "KEYWORD:TEST"],
                "COMMON-LISP:T",
                "COMMON-LISP:T",
            ]
        )
        == "((EQ CL-GIT:TAG) (EQ KEYWORD:TEST) COMMON-LISP:T COMMON-LISP:T)"
    )


def test_sexp():
    result = node_to_dict(
        cldomain.SEXP("nil").as_parameterlist(
            addnodes.desc_name("myfun", "myfun")
        )
    )
    assert result == {"desc_clparameterlist": [{"desc_name": "myfun"}]}

    result = node_to_dict(
        cldomain.SEXP("(first second third)").as_parameterlist(
            addnodes.desc_name("myfun", "myfun")
        )
    )
    assert result == {
        "desc_clparameterlist": [
            {"desc_name": "myfun"},
            {"desc_clparameter": "first"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "second"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "third"},
        ],
    }

    result = node_to_dict(
        cldomain.SEXP("(first second third &key key1 key2)").as_parameterlist(
            addnodes.desc_name("myfun", "myfun")
        )
    )
    assert result == {
        "desc_clparameterlist": [
            {"desc_name": "myfun"},
            {"desc_clparameter": "first"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "second"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "third"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "&key"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "key1"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "key2"},
        ],
    }

    result = node_to_dict(
        cldomain.SEXP("(&key key1 key2)").as_parameterlist(
            addnodes.desc_name("myfun", "myfun")
        )
    )
    assert result == {
        "desc_clparameterlist": [
            {"desc_name": "myfun"},
            {"desc_clparameter": "&key"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "key1"},
            {"desc_sig_space": [{"#text": []}]},
            {"desc_clparameter": "key2"},
        ],
    }
