"""Registry of backend types for Annif"""
from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from annif.backend.backend import AnnifBackend


# define functions for lazily importing each backend (alphabetical order)
def _dummy() -> Type[AnnifBackend]:
    from . import dummy

    return dummy.DummyBackend


def _ensemble() -> Type[AnnifBackend]:
    from . import ensemble

    return ensemble.EnsembleBackend


def _fasttext() -> Type[AnnifBackend]:
    try:
        from . import fasttext

        return fasttext.FastTextBackend
    except ImportError:
        raise ValueError("fastText not available, cannot use fasttext backend")


def _http() -> Type[AnnifBackend]:
    from . import http

    return http.HTTPBackend


def _mllm() -> Type[AnnifBackend]:
    from . import mllm

    return mllm.MLLMBackend


def _nn_ensemble() -> Type[AnnifBackend]:
    try:
        from . import nn_ensemble

        return nn_ensemble.NNEnsembleBackend
    except ImportError:
        raise ValueError(
            "Keras and TensorFlow not available, cannot use " + "nn_ensemble backend"
        )


def _omikuji() -> Type[AnnifBackend]:
    try:
        from . import omikuji

        return omikuji.OmikujiBackend
    except ImportError:
        raise ValueError("Omikuji not available, cannot use omikuji backend")


def _pav() -> Type[AnnifBackend]:
    from . import pav

    return pav.PAVBackend


def _stwfsa() -> Type[AnnifBackend]:
    try:
        from . import stwfsa

        return stwfsa.StwfsaBackend
    except ImportError:
        raise ValueError("STWFSA not available, cannot use stwfsa backend")


def _svc() -> Type[AnnifBackend]:
    from . import svc

    return svc.SVCBackend


def _tfidf() -> Type[AnnifBackend]:
    from . import tfidf

    return tfidf.TFIDFBackend


def _yake() -> Type[AnnifBackend]:
    try:
        from . import yake

        return yake.YakeBackend
    except ImportError:
        raise ValueError("YAKE not available, cannot use yake backend")


def _minilmv2() -> Type[AnnifBackend]:
    try:
        from . import minilmv2

        return minilmv2.MiniLmV2Backend
    except ImportError as e:
        raise ValueError("MiniLMv2 not available, cannot use minilmv2 backend")


def _xlmroberta() -> Type[AnnifBackend]:
    try:
        from . import xlmroberta

        return xlmroberta.XlmRobertaBackend
    except ImportError:
        raise ValueError("XlmRoberta not available, cannot use xlmroberta backend")


def _mdeberta() -> Type[AnnifBackend]:
    try:
        from . import mdeberta

        return mdeberta.MDeBertaBackend
    except ImportError:
        raise ValueError("MDeBERTa not available, cannot use mdeberta backend")


def _ehribert() -> Type[AnnifBackend]:
    try:
        from . import ehribert

        return ehribert.EhriBertBackend
    except ImportError:
        raise ValueError("EhriBert not available, cannot use ehribert backend")


def _mistral() -> Type[AnnifBackend]:
    try:
        from . import mistral

        return mistral.MistralBackend
    except ImportError:
        raise ValueError("Mistral not available, cannot use mistral backend")


# registry of the above functions
_backend_fns = {
    "dummy": _dummy,
    "ensemble": _ensemble,
    "fasttext": _fasttext,
    "http": _http,
    "mllm": _mllm,
    "nn_ensemble": _nn_ensemble,
    "omikuji": _omikuji,
    "pav": _pav,
    "stwfsa": _stwfsa,
    "svc": _svc,
    "tfidf": _tfidf,
    "yake": _yake,
    "xlmroberta": _xlmroberta,
    "minilmv2": _minilmv2,
    "ehribert": _ehribert,
    "mdeberta": _mdeberta,
    "mistral": _mistral,
}


def get_backend(backend_id: str) -> Type[AnnifBackend]:
    if backend_id in _backend_fns:
        return _backend_fns[backend_id]()
    else:
        raise ValueError("No such backend type {}".format(backend_id))
