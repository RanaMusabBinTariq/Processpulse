
import pandas as pd
from processpulse_logic import make_sample, normalize_csv, strongest_signal, detect_signals, safe_cpk, workflow_steps, process_twin_result, oee_estimate, requirements_brief, evidence_pack, I18N

def check(x, msg):
    if not x:
        raise AssertionError(msg)

def main():
    normal = normalize_csv(make_sample("normal"))
    check(strongest_signal(normal)["severity"] == "low", "normal should be low")

    ph = normalize_csv(make_sample("ph_drift"))
    check(any(s["parameter"] == "pH" for s in detect_signals(ph)), "pH drift signal missing")

    flow = normalize_csv(make_sample("flow_restriction"))
    check(any(s["parameter"] == "Flow" for s in detect_signals(flow)), "flow signal missing")

    temp = normalize_csv(make_sample("temperature_excursion"))
    check(any(s["parameter"] == "Temperature" and s["severity"] == "high" for s in detect_signals(temp)), "temperature high signal missing")

    missing_ipc = normalize_csv(make_sample("missing_ipc"))
    check(any(s["parameter"] == "pH" and s["severity"] == "high" for s in detect_signals(missing_ipc)), "missing IPC pH signal missing")

    partial = normalize_csv(pd.DataFrame({"time": pd.date_range("2026-01-01", periods=5), "Temperature": [24,24,24,24,24]}))
    check("pH" in partial["missing_required"], "pH should be missing")
    check("pH" not in partial["df"].columns, "pH should not be fabricated")

    check(safe_cpk([7.1,7.1,7.1], 6.8, 7.4) == 9.99, "constant in-range cpk failed")
    check(safe_cpk([9,9,9], 6.8, 7.4) == -9.99, "constant out-of-range cpk failed")

    check(workflow_steps(ph, {}), "workflow empty")
    check(0 <= process_twin_result(24,1.25,7.1,45,250,2)["risk"] <= 100, "twin risk")
    check(0 <= oee_estimate(ph)["oee"] <= 100, "oee range")
    check("user_req" in requirements_brief(ph), "requirements missing")
    check("ProcessPulse Evidence Pack" in evidence_pack(ph), "pack missing")

    en=set(I18N["en"].keys())
    de=set(I18N["de"].keys())
    check(en == de, f"translation keys mismatch: {en-de} {de-en}")

    print("LOGIC TESTS PASSED")

if __name__ == "__main__":
    main()
