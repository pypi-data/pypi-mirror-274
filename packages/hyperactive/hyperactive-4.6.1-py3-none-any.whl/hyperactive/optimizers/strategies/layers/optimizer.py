# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from ..optimizer_attributes import OptimizerAttributes


class OptimizerLayer(OptimizerAttributes):
    def __init__(self):
        super().__init__()

    def run_optimization_layer(self, nth_process, p_bar):
        hyper_opt = self.c_layer_setup["opt-algorithm"]
        n_iter = self.c_layer_setup["n_iter"]
        opt_strat_early_stopping = self.c_layer_setup["early_stopping"]

        if opt_strat_early_stopping:
            early_stopping = opt_strat_early_stopping
        else:
            early_stopping = self.early_stopping

        """

        # initialize
        if self.best_para is not None:
            initialize = {}
            if "warm_start" in initialize:
                initialize["warm_start"].append(self.best_para)
            else:
                initialize["warm_start"] = [self.best_para]
        else:
            initialize = dict(self.initialize)

        # memory_warm_start
        if self.search_data is not None:
            memory_warm_start = self.search_data
        else:
            memory_warm_start = self.memory_warm_start

        # warm_start_smbo
        if (
            hyper_opt.optimizer_class.optimizer_type == "sequential"
            and self.search_data is not None
        ):
            hyper_opt.opt_params["warm_start_smbo"] = self.search_data
            
        """

        hyper_opt.setup_search(
            objective_function=self.objective_function,
            s_space=self.s_space,
            n_iter=n_iter,
            initialize=self.initialize,
            pass_through=self.pass_through,
            callbacks=self.callbacks,
            catch=self.catch,
            max_score=self.max_score,
            early_stopping=early_stopping,
            random_state=self.random_state,
            memory=self.memory,
            memory_warm_start=self.memory_warm_start,
            verbosity=self.verbosity,
        )

        hyper_opt.search(nth_process, p_bar)

        self._add_result_attributes(
            hyper_opt.best_para,
            hyper_opt.best_score,
            hyper_opt.best_since_iter,
            hyper_opt.eval_times,
            hyper_opt.iter_times,
            hyper_opt.search_data,
            hyper_opt.gfo_optimizer.random_seed,
        )
