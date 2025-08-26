from context import *

from common.packages import *
import numpy as np
import matplotlib.pyplot as plt
from controller.controller import SimulationController
from models.black_scholes import BlackScholesModel
from metrics.pfe_metric import PFEMetric
from metrics.epe_metric import EPEMetric
from products.bermudan_option import AmericanOption, OptionType
from products.equity import Equity 
from engine.engine import SimulationScheme


if __name__ == "__main__":
    # # --- CPU/GPU device setup ---
    print(f"Using device: {device}")

    # Setup model and product
    model = BlackScholesModel(calibration_date=0.0, spot=100, rate=0.05, sigma=0.5)
    num_exercise_dates=100
    maturity = 3.0
    strike = 100.0

    underlying = Equity('id')
    product = AmericanOption(underlying=underlying,maturity=maturity, num_exercise_dates=num_exercise_dates, strike=strike, option_type=OptionType.CALL)

    portfolio=[product]

    # Metric timeline for exposure
    exposure_timeline = np.linspace(0, 4.,100)
    ee_metric = EPEMetric()
    pfe_metric = PFEMetric(0.9)

    metrics=[ee_metric, pfe_metric]

    num_paths_mainsim=10000
    num_paths_presim=10000
    num_steps=1
    sc=SimulationController(portfolio, model, metrics, num_paths_mainsim, num_paths_presim, num_steps, SimulationScheme.ANALYTICAL, False, exposure_timeline)

    sim_results=sc.run_simulation()

    ees=sim_results.get_results(0,0)
    pfes=sim_results.get_results(0,1)

    plt.figure(figsize=(10, 6))
    plt.plot(exposure_timeline, ees, label='Expected Exposure (EE)', color='red')
    plt.plot(exposure_timeline, pfes, label='Potential Future Exposure (PFE)', color='blue', linestyle='--')

    # Labels and title
    plt.xlabel('Time')
    plt.ylabel('Exposure')
    plt.title('Exposure vs. Time')

    # Grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    out_dir = os.path.join("tests", "plots", "exposure_tests")
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "exposure_american_equity_option.png")
    plt.savefig(out_path)
    print(f"Plot saved to {out_path}")