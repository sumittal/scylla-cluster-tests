import os
import re
import time
from avocado import main

from sdcm.tester import ClusterTester


class RunParallelNemesisTest(ClusterTester):
    """
    Test a Scylla cluster with running a multiple nemesis in parallel
    :avocado: enable
    """

    def test_run_two_nemesis(self):
        """
        Run cassandra-stress with params defined in data_dir/scylla.yaml
        """
        self.log.info('DB cluster is: %s', self.db_cluster)

        self.db_cluster.add_nemesis(nemesis=self.get_nemesis_class(),
                                    loaders=self.loaders,
                                    monitoring_set=self.monitors,
                                    db_stats=self.get_stats_obj())
        
        # check if we shall wait for total_used_space
        self.db_cluster.wait_total_space_used_per_node()

        # start the nemesis in parallel
        self.db_cluster.start_nemesis(interval=self.params.get('nemesis_interval'))
        time.sleep(180 * 60)

        #self.kill_stress_thread()

        # verify if the data is intact or not


if __name__ == '__main__':
    main()
