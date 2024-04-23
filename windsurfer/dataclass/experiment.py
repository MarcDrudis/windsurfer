from dataclasses import KW_ONLY, dataclass, field
from datetime import datetime

import numpy as np
from dataclass_wizard import DumpMixin, LoadMixin, YAMLWizard
from icecream import ic


@dataclass
class SetupExperiment(LoadMixin, DumpMixin):
    timestamp: datetime = field(default_factory=datetime.now, init=False)


@dataclass
class ResultExperiment(LoadMixin, DumpMixin):
    timestamp: datetime = field(default_factory=datetime.now, init=False)
    _: KW_ONLY
    artifact_dir: str

    @staticmethod
    def dump_with_str(o: str, *_):
        ic("dumping str", o)
        return o

    def __post_init__(self):
        def dump_with_array(o: np.ndarray, *_):
            ic("dumping array")
            path_to_artifact = self.artifact_dir + f"{hash(o.tostring())}.npy"
            np.save(path_to_artifact, o)
            return path_to_artifact

        self.register_dump_hook(typ=np.ndarray, func=dump_with_array)

        def load_from_array(o: np.ndarray, base_type: np.ndarray):
            ic("load array")
            return np.load(o)

        self.register_load_hook(typ=np.ndarray, func=load_from_array)


@dataclass
class Experiment(YAMLWizard, LoadMixin, DumpMixin):
    setup: SetupExperiment
    result: ResultExperiment | None = None
    additional_data: dict = field(default_factory=dict)
