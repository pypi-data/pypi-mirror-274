from qmio.clients import ZMQClient
import json


def _optimization_options_builder(optimization, opt_type="Tket"):
    """
    Optimization builder to not depend on qat

    Just Tket for now
    """
    if opt_type != "Tket":
        raise TypeError(f"{opt_type}: Not a valid type")
    if optimization == 1:
        opt_value = 18
    elif optimization == 2:
        opt_value = 30
    elif optimization == 0:
        opt_value = 1
    else:
        raise ValueError(f"{optimization}: Not a valid Optimization Value")
    return opt_value


def _results_format_builder(res_format="binary_count"):
    """
    Results Format Builder without QAT

    Posibilities:
    raw:

    binary:
    Binary string
    binary_count (default):
    Returns a count of each instance of measured qubit registers.
        Switches result format to raw.
    squash_binary_result_arrays:
    Squashes binary result list into a singular bit string. Switches results to
        binary.
    """
    if res_format != "binary_count":
        if res_format == "raw":
            # Check
            InlineResultsProcessing = 1
            ResultsFormatting = 2
        elif res_format == "binary":
            # Check
            InlineResultsProcessing = 2
            ResultsFormatting = 2
        elif res_format == "squash_binary_result_arrays":
            # Check
            InlineResultsProcessing = 2
            ResultsFormatting = 6
    elif res_format == "binary_count":
        # Desde recién instanciado - check
        InlineResultsProcessing = 1
        ResultsFormatting = 3
    else:
        raise TypeError(f"{res_format}: Not a valid result format")
    return InlineResultsProcessing, ResultsFormatting


def _config_build(shots: int, repetition_period=None, optimization=0, res_format="binary_count"):
    """
    Builds a config json object from options
    not qat dependent
    """
    inlineResultsProcessing, resultsFormatting = _results_format_builder(res_format)
    opt_value = _optimization_options_builder(optimization=optimization)
    config = {
        "$type": "<class \'qat.purr.compiler.config.CompilerConfig\'>",
        "$data": {
            "repeats": shots,
            "repetition_period": repetition_period,
            "results_format": {
                "$type": "<class \'qat.purr.compiler.config.QuantumResultsFormat\'>",
                "$data": {
                    "format": {
                        "$type": "<enum \'qat.purr.compiler.config.InlineResultsProcessing\'>",
                        "$value": inlineResultsProcessing
                    },
                    "transforms": {
                        "$type": "<enum \'qat.purr.compiler.config.ResultsFormatting\'>",
                        "$value": resultsFormatting
                    }
                }
            },
            "metrics": {
                "$type": "<enum \'qat.purr.compiler.config.MetricsType\'>",
                "$value": 6
            },
            "active_calibrations": [],
            "optimizations": {
                "$type": "<enum \'qat.purr.compiler.config.TketOptimizations\'>",
                "$value": opt_value
            }
        }
    }
    config_str = json.dumps(config)
    return config_str


class QPUBackend:
    def __init__(self):
        self.client = None

    def __enter__(self):
        self.client = ZMQClient()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()
            self.client = None

    def connect(self):
        self.client = ZMQClient()

    def disconnect(self):
        self.client.close()
        self.client = None

    # def run_v0(self, circuit, config):
    #     if not self.client:
    #         raise RuntimeError("Not connected to the server")

    #     job = (circuit, config)
    #     self.client._send(job)
    #     result = self.client._await_results()
    #     return result

    # def run_v1(self, circuit, shots):
    #     if not self.client:
    #         raise RuntimeError("Not connected to the server")

    #     config = _config_build(shots)
    #     job = (circuit, config)
    #     self.client._send(job)
    #     result = self.client._await_results()
    #     return result

    def run(self, circuit, shots, repetition_period=None, optimization=0, res_format="binary_count"):
        if not self.client:
            raise RuntimeError("Not connected to the server")

        config = _config_build(shots, repetition_period=repetition_period, optimization=optimization, res_format=res_format)
        job = (circuit, config)
        self.client._send(job)
        result = self.client._await_results()
        return result
