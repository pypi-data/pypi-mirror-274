import warnings
import numpy as np
import pandas as pd
from ..kernel import Jac6, Jac6c
from ..kernel import parameters_to_dataframe_result, parameters_to_dataframe

try:
    import jinja2

    if_style = True
except ImportError:
    if_style = False
    print("Jinja2 is not installed. Turn off colored table. Try pip install jinja2.")


def report_crlb(outparams, crlb, Jacfunc=None):
    """
    Generates a report on Cramér-Rao Lower Bounds (CRLBs).

    Args:
        outparams (lmfit Parameters object): DataFrame containing model parameters.
        crlb (numpy.ndarray): Array of CRLB values.
        Jacfunc (callable, optional): Function to compute the Jacobian. Defaults to None.

    Returns:
        pandas.DataFrame: DataFrame with CRLB information for relevant parameters.
    """
    pdpoptall = parameters_to_dataframe_result(outparams)
    # print(f"{Jacfunc=}, {pdpoptall=} {outparams=}")
    if Jacfunc is None or Jacfunc is Jac6:
        # You'll need to assert there is a peaklist in the fid_parameters
        poptall = pdpoptall["value"]
    elif Jacfunc is Jac6c:
        poptall = pdpoptall[~pdpoptall["name"].str.startswith("g")]["value"]
    # elif Jacfunc is flexible_Jac:
    #    poptall = pdpoptall[pdpoptall['vary']]['value'] # Parameters with vary=True
    else:
        # print(f"{Jacfunc=} is not supported!")
        # print("Jacfunc=%s is not supported!" % Jacfunc)
        warnings.warn("Jacfunc=%s is not supported!" % Jacfunc, RuntimeWarning)

    resultpd = pdpoptall.loc[poptall.index]
    resultpd["CRLB %"] = np.abs(crlb / poptall * 100.0)
    return resultpd


def highlight_rows_crlb_less_than_02(row):
    # highlight the rows of the input dataframe as green if the CRLB(%) <= 20.
    return [
        (
            "background-color: rgba(0, 255, 0, 0.5)"
            if row["CRLB(%)"] <= 20.0
            else "background-color: rgba(255, 0, 0, 0.2)"
        )
        for _ in row
    ]


def sum_multiplets(df):
    """
    Sums amplitude and standard deviation for multiplets
    with the same base name in the given DataFrame.

    Groups the DataFrame on base peak names (extracted by removing digits)
    and aggregates the columns, summing amplitude and standard deviation
    but taking the first value for other columns like chemical shift.

    Parameters:
        df (DataFrame): DataFrame with columns including 'amplitude',
            'sd', 'chem shift(ppm)'

    Returns:
        DataFrame: DataFrame grouped and aggregated on base peak names
    """

    def get_base_name(name):
        return "".join([i for i in name if not i.isdigit()])

    base_names = df.index.map(get_base_name)

    added_peaks = set()
    grouped_peak_list = [
        x for x in base_names if not (x in added_peaks or added_peaks.add(x))
    ]

    agg_funcs = {
        col: "first" if col not in ["amplitude", "sd"] else "sum" for col in df.columns
    }
    grouped_df = df.groupby(base_names).agg(agg_funcs)

    # return grouped_df.sort_values('chem shift(ppm)')
    return grouped_df.reindex(grouped_peak_list)


def contains_non_numeric_strings(df):
    def is_numeric_string(s):
        try:
            float(
                s
            )  
            return True
        except ValueError:
            return False

    return any(not is_numeric_string(str(idx)) for idx in df.index)


def report_amares(outparams, fid_parameters, verbose=False):
    """
    Generates a comprehensive report on AMARES analysis results.

    Args:
        outparams (lmfit fitting parameter): Output parameters from the fitting process.
        fid_parameters (argspace Namespace object): FID parameters object.
        verbose (bool, optional): Controls verbosity of output. Defaults to False.

    Returns:
        pandas.Styler: A DataFrame for presentation of the results with rows whose CRLB<=20
        are highlighted by green.
    """
    from pyAMARES.util.crlb import create_pmatrix, evaluateCRB  # delayed import

    pkpd = parameters_to_dataframe(outparams)
    Pmatrix = create_pmatrix(pkpd, ifplot=verbose)
    evaluateCRB(outparams, fid_parameters, P=Pmatrix, verbose=verbose)
    resulttable = fid_parameters.resultpd
    peaklist = [
        x.replace("phi_", "")
        for x in resulttable[resulttable["name"].str.startswith("phi")]["name"].values
    ]

    final_table = pd.DataFrame()
    all_peak_data = []

    for peak in peaklist:
        peak_data = []

        for parameter in ["ak", "freq", "dk", "phi", "g"]:
            var_name = parameter + "_" + peak
            currentrow = resulttable[resulttable["name"] == var_name][
                ["value", "std", "CRLB %"]
            ].copy()
            peak_data.extend(currentrow.values.flatten())
        all_peak_data.append(peak_data)

    column_names = []
    for parameter in ["ak", "freq", "dk", "phi", "g"]:
        column_names.extend(
            [parameter + "_value", parameter + "_std", parameter + "_CRLB %"]
        )
    final_table = pd.DataFrame(all_peak_data, columns=column_names)

    MHz = fid_parameters.MHz
    result = final_table.rename(
        columns={
            "ak_value": "amplitude",
            "ak_std": "a_sd",
            "ak_CRLB %": "a_CRLB(%)",
            "freq_value": "chem shift",
            "freq_std": "freq_sd",
            "freq_CRLB %": "freq_CRLB(%)",
            "dk_value": "lw",
            "dk_std": "lw_sd",
            "dk_CRLB %": "lw_CRLB(%)",
            "phi_value": "phase",
            "phi_std": "phase_sd",
            "phi_CRLB %": "phase_CRLB(%)",
            "g_CRLB %": "g_CRLB(%)",
        }
    )
    # fid_parameters.result2 = result.copy() # debug
    negative_amplitude = result["amplitude"] < 0
    if negative_amplitude.sum() > 0:
        print(
            "The amplitude of index",
            result.loc[negative_amplitude].index.values,
            " is negative! Make it positive and flip the phase!",
        )
        result.loc[negative_amplitude, "amplitude"] = result.loc[
            negative_amplitude, "amplitude"
        ].abs()
        result.loc[negative_amplitude, "phase"] += np.pi

    # For poor lmfit fitting, there may not be any sd estimated. Then use CRLB instead
    sd_columns = ["a_sd", "freq_sd", "lw_sd", "phase_sd", "g_std"]
    crlb_columns = [
        "a_CRLB(%)",
        "freq_CRLB(%)",
        "lw_CRLB(%)",
        "phase_CRLB(%)",
        "g_CRLB(%)",
    ]
    val_columns = ["amplitude", "chem shift", "lw", "phase", "g_value"]
    for col, crlb_col, val_col in zip(sd_columns, crlb_columns, val_columns):
        if result[col].isnull().all():
            print("%s is all None, use crlb instead!" % col)
            result[col] = result[crlb_col] / 100 * result[val_col]

    result["chem shift"] = result["chem shift"] / MHz
    result["freq_sd"] = result["freq_sd"] / MHz
    result["lw"] = result["lw"] / np.pi
    result["lw_sd"] = result["lw_sd"] / np.pi
    result["phase"] = np.rad2deg(result["phase"]) % 360
    try:
        result["phase_sd"] = np.rad2deg(result["phase_sd"])
    except Exception as e:
        print(f"Caught an error: {e}")
        result["phase_sd"] = np.nan
    # Change 'g_CRLB(%)' values to NaN where they are 0.0
    result.loc[result["g_CRLB(%)"] == 0.0, "g_CRLB(%)"] = np.nan
    result.columns = [
        "amplitude",
        "sd",
        "CRLB(%)",
        "chem shift(ppm)",
        "sd(ppm)",
        "CRLB(cs%) ",
        "LW(Hz)",
        "sd(Hz)",
        "CRLB(LW%)",
        "phase(deg)",
        "sd(deg)",
        "CRLB(phase%)",
        "g",
        "g_sd",
        "g (%)",
    ]
    result["name"] = peaklist
    result = result.set_index("name")
    if hasattr(fid_parameters, "peaklist"):
        # By default, there should be a peak list from the fid_parameters
        result.reindex(
            fid_parameters.peaklist
        )  # reorder to the peaklist from the pk, not the local peaklist
    # fid_parameters.peaklist = peaklist
    else:
        print("No peaklist, probably it is from an HSVD initialized object")
    fid_parameters.result_multiplets = result  # Keep the multiplets
    # Sum multiplets if needed
    if contains_non_numeric_strings(result):  # assigned peaks in the index
        fid_parameters.result_sum = sum_multiplets(result)
        # Sum the amplitude of each multiplets. For example, make BATP, BATP2, BATP3 as BATP
        if if_style:
            styled_df = fid_parameters.result_sum.style.apply(
                highlight_rows_crlb_less_than_02, axis=1
            ).format("{:.3f}")
        else:
            styled_df = (
                fid_parameters.result_sum
            )  # python 3.7 and older may not support Jinja2
    else:  # all numers, HSVD assigned parameters
        if if_style:
            styled_df = fid_parameters.result_multiplets.style.apply(
                highlight_rows_crlb_less_than_02, axis=1
            ).format("{:.3f}")
        else:
            styled_df = (
                fid_parameters.result_multiplets
            )  # python 3.7 and older may not support Jinja2
    if hasattr(fid_parameters, "result_sum"):
        fid_parameters.metabolites = fid_parameters.result_sum.index.to_list()
    else:
        print("There is no result_sum generated, probably there is only 1 peak")
    fid_parameters.styled_df = styled_df
    return styled_df
