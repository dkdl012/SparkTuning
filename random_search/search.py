import os
import gin
import json
import logging
from random_search.spark import SparkBench
from envs.utils import get_foldername

@gin.configurable
class RandomSearch: # Random Optimizer?
    def __init__(
        self,
        sb: SparkBench,
        maximum_number_evaluations: int
    ):
        self.sb = sb
        self.maximum_number_evaluations = maximum_number_evaluations                        
        self._set_result_dir()
    
    def _set_result_dir(self, path='/home/jieun/SparkTuning/random_search/results'):
        self.results_dir = get_foldername(path)
        os.makedirs(self.results_dir, exist_ok=True)
        logging.info(f"Results are saved in .. {self.results_dir}")
    
    def run(self):
        logging.info("Start Random Search!!")       
        best_config = None
        best_res = 10000
        
        configs = []
        results = []
        
        for _ in range(self.maximum_number_evaluations):
            sampled_config = self.sb.random_sampling_configuration()
            self.sb.apply_configuration()
            
            res = self.sb.get_results()
            logging.info(f"[{_}/{self.maximum_number_evaluations}]!!!!!!!!!!!!!!Results:{res}!!!!!!!!!!!!!!")
            
            if res < best_res:
                logging.info(f"## Best result is updated!! : {best_res} --> {res}")
                best_res = res
                
                # best_config = sampled_config
                f = open('../data/add-spark.conf', 'r')
                best_config = f.readlines()    
                
            configs.append(sampled_config.get_dictionary())
            results.append(res)
        
        # Save history.. configs and results
        with open(os.path.join(self.results_dir, 'configs.json'), 'w') as f:
            json.dump(configs, f)
        
        with open(os.path.join(self.results_dir, 'results.json'), 'w') as f:
            json.dump(results, f)
            
        logging.info("......................")
        logging.info("..Best Configuration..")
        for l in best_config:
            logging.info(l, end='')
        logging.info("......................")