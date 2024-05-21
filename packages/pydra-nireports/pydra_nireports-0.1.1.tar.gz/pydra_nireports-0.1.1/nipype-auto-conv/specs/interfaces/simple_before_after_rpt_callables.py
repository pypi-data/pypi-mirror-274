"""Module to put any functions that are referred to in the "callables" section of SimpleBeforeAfterRPT.yaml"""


def out_report_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_report"]


# Original source at L419 of <nipype-install>/interfaces/base/core.py
def BaseInterface___list_outputs(
    inputs=None, stdout=None, stderr=None, output_dir=None
):
    """List the expected outputs"""
    if True:
        raise NotImplementedError
    else:
        return None


# Original source at L54 of <nipype-install>/interfaces/mixins/reporting.py
def ReportCapableInterface___list_outputs(
    inputs=None, stdout=None, stderr=None, output_dir=None
):
    try:
        outputs = BaseInterface___list_outputs()
    except NotImplementedError:
        outputs = {}
    if _out_report is not None:
        outputs["out_report"] = _out_report
    return outputs


# Original source at L54 of <nipype-install>/interfaces/mixins/reporting.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    try:
        outputs = BaseInterface___list_outputs()
    except NotImplementedError:
        outputs = {}
    if _out_report is not None:
        outputs["out_report"] = _out_report
    return outputs


# Original source at L54 of <nipype-install>/interfaces/mixins/reporting.py
def nireports_interfaces_reporting_base__RegistrationRC___list_outputs(
    inputs=None, stdout=None, stderr=None, output_dir=None
):
    try:
        outputs = BaseInterface___list_outputs()
    except NotImplementedError:
        outputs = {}
    if _out_report is not None:
        outputs["out_report"] = _out_report
    return outputs
