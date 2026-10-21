Synthetic dummy datasets for the DAB + GJO EV fast-charging manuscript

IMPORTANT: Every row in these files is synthetic, generated for testing plotting, code, and analysis workflows.
These are NOT measured experimental results, validated MATLAB/Simulink outputs, or evidence supporting manuscript claims.
Do not present these values as real results in a paper. Replace them with actual simulation/experimental exports before publication.

Files:
1. synthetic_cc_cv_charging_timeseries.csv
   10-second CC-CV charging illustration. Uses manuscript context: 300 V, 13 Ah battery, 2C = 26 A, voltage settling near 312 V, SoC 10.03% to 10.17%, nominal efficiency around 96.1%.
   CC/CV transition time is illustrative only and is not a validated controller implementation.

2. synthetic_parameter_sweep.csv
   500 artificial candidate parameter evaluations over phase shift, switching frequency, and series inductance. Ripple, tracking error, efficiency, loss index, and fitness are synthetic response surfaces, not calculated from a physical DAB model.

3. synthetic_gjo_convergence.csv
   Illustrative best-so-far fitness values across 100 iterations for a population size of 30. Not a real GJO execution.

4. synthetic_controller_comparison.csv
   Illustrative baseline comparison for manual tuning, Ziegler-Nichols, GA, PSO, and GJO. Values are fabricated for demonstration and must not be used as scientific claims.

5. synthetic_v2g_discharge_timeseries.csv
   Illustrative 10-second V2G discharge scenario at 13 A (1C for 13 Ah). The manuscript includes an inconsistency mentioning an approximately 90 A plotted operating point while referring to a 1C/13 A rate; this dummy dataset uses 13 A only as a clearly labeled illustrative scenario.

Suggested uses:
- Plot voltage/current/SoC traces.
- Demonstrate CSV import and analysis.
- Build example comparison charts and a mock optimization-convergence plot.

Columns use SI units where applicable. Current is negative in the V2G file to denote discharge/reverse power flow.
