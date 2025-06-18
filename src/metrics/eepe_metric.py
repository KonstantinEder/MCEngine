from metrics.metric import *

# Metric for Effective Expected Positive Exposure
class EEPEMetric(Metric):
    def __init__(self, evaluation_type=Metric.EvaluationType.NUMERICAL):
        super().__init__(metric_type=MetricType.EEPE, evaluation_type=evaluation_type)

    def evaluate_analytically(self, *args, **kwargs):
        raise NotImplementedError("Analytical EEPE not implemented.")

    def evaluate_numerically(self, exposures,cfs):
        expected_exposures=[]
        for e in exposures:
            ee = torch.relu(e).mean()
            expected_exposures.append(ee)
        return [torch.stack(expected_exposures).mean()]  # Return for each time point