#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import logging
import os
import threading
import multiprocessing
import time
import pandas as pd

from wiliot_core import WiliotGateway, ActionType, DataType, set_logger
from wiliot_testers.sample.modules.resolve_packets import ResolvePackets, TagStatus
from wiliot_testers.utils.wiliot_external_ids import is_external_id_valid


RESET_GW_TIME = 300  # number of seconds we allow to not getting packets until we reset the GW
RESOLVE_Q_SIZE = 100


class ResolverProcess(ResolvePackets):
    def __init__(self, owner_id, env, need_to_resolve_q, resolved_q, stop_event):
        logger_path, self.logger = set_logger('ResolverProcess', 'resolver_process', 'resolver')
        self.resolved_q = resolved_q
        super().__init__(tags_in_test=[], owner_id=owner_id, env=env, resolve_q=need_to_resolve_q,
                         set_tags_status_df=self.add_to_resolved_q, stop_event_trig=stop_event,
                         logger_name=self.logger.name)
        self.run()

    def check_tag_status(self, ex_id):
        if is_external_id_valid(ex_id['externalId']):
            status = TagStatus.INSIDE_TEST
        else:
            status = TagStatus.OUT_INVALID
            self.logger.warning(f'found invalid external id: {ex_id["externalId"]}, check serialization')
        self.logger.info(f'found new tag in test: {ex_id}')
        return status

    def add_to_resolved_q(self, element):
        self.resolved_q.put(element, block=False)


class ReelVerification(object):
    def __init__(self, user_input, stop_event, logger_name, logger_path):
        self.logger = logging.getLogger(logger_name)
        self.logger_path = logger_path
        self.user_inputs = user_input
        self.stop_event = stop_event

        # connect to the gw:
        self.gw_obj = None
        self.gw_init()
        self.gw_reset_and_config()

        # init data:
        self.packets_df = pd.DataFrame()
        # start app
        try:
            need_to_resolve_q = multiprocessing.Queue(maxsize=RESOLVE_Q_SIZE)
            resolved_q = multiprocessing.Queue(maxsize=RESOLVE_Q_SIZE)
            self.resolver_handler = multiprocessing.Process(target=ResolverProcess,
                                                            args=(self.user_inputs['owner_id'],
                                                                  self.user_inputs['env'],
                                                                  need_to_resolve_q,
                                                                  resolved_q,
                                                                  stop_event))
            self.resolver_handler.start()

            self.need_to_resolve_q = need_to_resolve_q
            self.resolved_q = resolved_q

            self.get_packet_handler = threading.Thread(target=self.run, args=())
            self.get_packet_handler.start()

        except Exception as e:
            self.logger.warning(f'exception during ReelVerification init: {e}')
            raise e

    def gw_init(self):
        """
        initialize gw and the data listener thread
        """
        self.gw_obj = WiliotGateway(auto_connect=True, logger_name=self.logger.name,
                                    is_multi_processes=True,
                                    log_dir_for_multi_processes=os.path.dirname(self.logger_path))
        try:
            if self.gw_obj.connected:
                self.gw_obj.start_continuous_listener()
            else:
                raise Exception('gateway was not detected, please check connection')
        except Exception as e:
            self.logger.log(logging.WARNING, e)
            raise e

    def gw_reset_and_config(self):
        """
        config gw to tester mode
        """
        self.gw_obj.reset_gw()
        if not self.gw_obj.is_gw_alive():
            raise Exception('GW is not responding')

        energy_pattern = int(self.user_inputs['energy_pattern'])
        time_profile = [int(x) for x in self.user_inputs['time_profile'].split(',')]
        ble_power = int(self.user_inputs['ble_power'])
        sub1g_power = int(self.user_inputs['sub1g_power'])
        sub1g_freq = int(self.user_inputs['sub1g_freq'])
        scan_ch = int(self.user_inputs['scan_ch'])
        is_bridge = self.user_inputs['is_listen_bridge'].lower() == 'yes'
        self.gw_obj.start_continuous_listener()
        if is_bridge:
            self.gw_obj.write('!listen_to_tag_only 0', with_ack=True)
        self.gw_obj.write(f'!set_sub_1_ghz_energizing_frequency {sub1g_freq}', with_ack=True)
        self.gw_obj.config_gw(received_channel=scan_ch,
                              energy_pattern_val=energy_pattern,
                              time_profile_val=time_profile,
                              effective_output_power_val=ble_power,
                              sub1g_output_power_val=sub1g_power,
                              start_gw_app=True, with_ack=True)

    def run(self):
        self.logger.info('GetPackets Start')
        cur_time = time.time()
        while True:
            time.sleep(0)
            try:
                if self.stop_event.is_set():
                    self.logger.info('GetPackets Stop')
                    self.exit_app()
                    return

                # check if there is data to read
                if self.gw_obj.is_data_available():
                    tag_collections_in = self.gw_obj.get_packets(action_type=ActionType.ALL_SAMPLE,
                                                                 data_type=DataType.TAG_COLLECTION)
                    for tag in tag_collections_in.keys():
                        if tag in self.packets_df.index:
                            self.packets_df.loc[tag, 'n_packets'] += 1
                        else:
                            self.logger.info(f'new tag was detected: {tag}')
                            try:
                                self.need_to_resolve_q.put({'tag': tag,
                                                            'payload': tag_collections_in[tag][0].get_payload()},
                                                           block=False)
                                self.packets_df = pd.concat([self.packets_df,
                                                             pd.DataFrame({'n_packets': 0, 'external_id': 'unknown'},
                                                                          index=[tag])])
                            except Exception as e:
                                self.logger.warning(f'could not add new data to need_to_resolve_q or to packets_df '
                                                    f'due to: {e}')

                if not self.resolved_q.empty():
                    self.merge_resolved_data()

                if time.time() - cur_time > RESET_GW_TIME:
                    self.logger.warning(f'did NOT get any packets after {RESET_GW_TIME} seconds. reset and config gw')
                    self.gw_reset_and_config()
                    cur_time = time.time()

            except Exception as e:
                self.logger.warning(f'GetPackets got exception: {e}')

    def merge_resolved_data(self):
        n = self.resolved_q.qsize()
        for _ in range(n):
            resolved = self.resolved_q.get(block=False)
            self.packets_df.loc[resolved['adv_address'], 'external_id'] = resolved['external_id']

    def exit_app(self):
        self.gw_obj.reset_gw()
        self.gw_obj.exit_gw_api()
        self.resolver_handler.join(5)
        if self.resolver_handler.is_alive():
            self.logger.warning('resolver process is still running')

    def get_packets_df(self):
        return self.packets_df


if __name__ == '__main__':
    from wiliot_core import set_logger
    RUN_TIME = 60

    tag_pref_logger_path, tag_pref_logger = set_logger(app_name='ReelVerification', dir_name='reel_verification',
                                                       file_name='verification_log')
    stop_event = multiprocessing.Event()
    user_input = {
        'energy_pattern': '51',
        'time_profile': '5,15',
        'ble_power': '22', 'sub1g_power': '29', 'sub1g_freq': '925000',
        'scan_ch': '37',
        'is_listen_bridge': 'yes',
        'owner_id': 'wiliot-ops',
        'env': 'prod'
    }
    v = ReelVerification(user_input=user_input, stop_event=stop_event,
                         logger_name=tag_pref_logger.name, logger_path=tag_pref_logger_path)

    t_i = time.time()
    while time.time() - t_i < RUN_TIME:
        time.sleep(1)
        df = v.get_packets_df()
        print(f'n unique adva: {len(df)}')
    # stop run
    stop_event.set()

    df = v.get_packets_df()
    df.index = df.index.set_names(['adv_address'])
    df = df.reset_index()
    df_path = tag_pref_logger_path.replace('.log', '_packets_df.csv')
    print(f'saving data at: {df_path}')
    df.to_csv(df_path, index=False)

    print('done')
