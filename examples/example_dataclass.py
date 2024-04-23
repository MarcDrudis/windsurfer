from dataclasses import KW_ONLY, dataclass, field
from datetime import datetime

import numpy as np
from icecream import ic

from windsurfer.dataclass.experiment import (Experiment, ResultExperiment,
                                             SetupExperiment)

# from dataclass_wizard import (DumpMixin, JSONSerializable, LoadMixin,
#                               YAMLWizard, json_key)
#
#
# @dataclass
# class SetupExperiment(LoadMixin, DumpMixin):
#     timestamp: datetime = field(default_factory=datetime.now, init=False)
#
#     def dump_with_str(o: str, *_):
#         return o.upper()
#
#     # def __post_init__(self):
#     #     pass
#     # self.register_dump_hook(typ=np.ndarray, func=ResultExperiment.dump_with_array)
#
#
# @dataclass
# class ResultExperiment(LoadMixin, DumpMixin):
#     timestamp: datetime = field(default_factory=datetime.now, init=False)
#     _: KW_ONLY
#     artifact_dir: str
#
#     @staticmethod
#     def dump_with_str(o: str, *_):
#         ic("dumping str", o)
#         return o
#
#     def __post_init__(self):
#         def dump_with_array(o: np.ndarray, *_):
#             ic("dumping array")
#             path_to_artifact = self.artifact_dir + f"{hash(o.tostring())}.npy"
#             np.save(path_to_artifact, o)
#             return path_to_artifact
#
#         self.register_dump_hook(typ=np.ndarray, func=dump_with_array)
#
#         def load_from_array(o: np.ndarray, base_type: np.ndarray):
#             ic("load array")
#             return np.load(o)
#
#         self.register_load_hook(typ=np.ndarray, func=load_from_array)
#
#
# @dataclass
# class Experiment(YAMLWizard, LoadMixin, DumpMixin):
#     setup: SetupExperiment
#     result: ResultExperiment | None = None
#     additional_data: dict = field(default_factory=dict)
#
#     # @classmethod
#     # def set(*args, **kwargs):
#     #     experiment_setup = SetupExperiment(*args, **kwargs)
#     #     return Experiment(setup=experiment_setup, result=None)
#

if __name__ == "__main__":
    import numpy as np
    from icecream import ic

    @dataclass
    class InstanceSetup(SetupExperiment):
        a: list
        b: str
        c: int

    @dataclass
    class InstanceResult(ResultExperiment):
        d: str
        e: np.ndarray
        f: int

    @dataclass
    class InstanceExperiment(Experiment):
        setup: InstanceSetup
        result: InstanceResult | None

    # emtpy_experiment = Experiment.set(field_a=1, field_b=2, field_c=3)
    setup = InstanceSetup([1, 1, 1], "h", 3)
    # setup = InstanceSetup(1, 2, 3)
    empty_experiment = InstanceExperiment(setup)
    empty_experiment.result = InstanceResult(
        "l",
        np.array([3, 4, 5]),
        6,
        artifact_dir="/home/marc/Documents/windsurfer/examples/",
    )
    empty_experiment.additional_data["an other"] = 10
    print(empty_experiment)
    print(empty_experiment.to_yaml())
    empty_experiment.to_yaml_file("examples/test.yaml")
    reconstructed = InstanceExperiment.from_yaml(empty_experiment.to_yaml())
    print(reconstructed)
    print(type(reconstructed.setup.a))
