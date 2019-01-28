# coding: utf-8
import os
import sys
import json
import requests
from django.conf import settings

ssa_result_template = {
    "order": 0,
    "template": "ssa-result-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                #  for single JSON objects, not arrays of JSON objects(nested)
                "data": {
                    "type": "object",
                    "dynamic": True
                },
                "key": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "time": {
                    "format": "yyyy-MM-dd HH:mm:ss",
                    "type": "date"
                },
                "timestamp": {
                    "format": "strict_date_optional_time||epoch_millis",
                    "type": "date"
                }
            }
        }
    },
    "aliases": {}
}

# ssa_ids_template = {
#     "order": 0,
#     "template": "ids-*",
#     "settings": {
#         "index": {
#             "refresh_interval": "5s"
#         }
#     },
#     "mappings": {
#         "result": {
#             "dynamic_templates": [
#                 {
#                     "notanalyzed": {
#                         "mapping": {
#                             "index": "not_analyzed",
#                             "type": "string",
#                             "doc_values": "true"
#                         },
#                         "match_mapping_type": "string",
#                         "match": "*"
#                     }
#                 }
#             ],
#             "_all": {
#                 "omit_norms": True,
#                 "enabled": True
#             },
#             "properties": {
#                 "@timestamp": {
#                     "type": "date",
#                     "format": "strict_date_optional_time||epoch_millis"
#                 },
#                 "cve_id": {"type": "string", "index": "not_analyzed"},
#                 "dst_ip": {"type": "string", "index": "not_analyzed"},
#                 "dst_ip_location": {"type": "string", "index": "not_analyzed"},
#                 "dst_port": {"type": "long"},
#                 "fingerprint": {"type": "string", "index": "not_analyzed"},
#                 "internal_id": {"type": "long"},
#                 "level": {"type": "long"},
#                 "name": {"type": "string", "index": "not_analyzed"},
#                 "protocol": {"type": "string", "index": "not_analyzed"},
#                 "provider_id": {"type": "string", "index": "not_analyzed"},
#                 "src_ip": {"type": "string"},
#                 "src_ip_location": {"type": "string", "index": "not_analyzed"},
#                 "src_port": {"type": "long"},
#                 "time": {"type": "string"},
#                 "type_id": {"type": "string"}
#             }
#         }
#     },
#     "aliases": {}
# }

ssa_network_template = {
    "order": 0,
    "template": "network-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "app_name": {"type": "string", "index": "not_analyzed"},
                "app_names": {"type": "string", "index": "not_analyzed"},
                "app_proto": {"type": "long"},
                "device_type": {"type": "string", "index": "not_analyzed"},
                "download_bytes": {"type": "long"},
                "download_pkg": {"type": "long"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "dst_ip_location": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "long"},
                "end": {"type": "long"},
                "provider_id": {"type": "string", "index": "not_analyzed"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "src_ip_location": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "long"},
                "start": {"type": "long"},
                "time": {"type": "long"},
                "upload_bytes": {"type": "long"},
                "upload_pkg": {"type": "long"}
            }
        }
    },
    "aliases": {}
}

# ssa_event_bdgl_template_template = {
#     "order": 0,
#     "template": "ssa-event-bdgl-*",
#     "settings": {
#         "index": {
#             "refresh_interval": "5s"
#         }
#     },
#     "mappings": {
#         "result": {
#             "dynamic_templates": [
#                 {
#                     "notanalyzed": {
#                         "mapping": {
#                             "index": "not_analyzed",
#                             "type": "string",
#                             "doc_values": "true"
#                         },
#                         "match_mapping_type": "string",
#                         "match": "*"
#                     }
#                 }
#             ],
#             "_all": {
#                 "omit_norms": True,
#                 "enabled": True
#             },
#             "properties": {
#                 "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
#                 "anomaly_type": {"type": "long"},
#                 "app_module": {"type": "string", "index": "not_analyzed"},
#                 "app_system": {"type": "string", "index": "not_analyzed"},
#                 "count": {"type": "long"},
#                 "end_time": {"type": "string"},
#                 "entity": {"type": "string", "index": "not_analyzed"},
#                 "entity_type": {"type": "string"},
#                 "event_id": {"type": "string", "index": "not_analyzed"},
#                 "event_type": {"type": "long"},
#                 "start_time": {"type": "string"},
#                 "threat_level": {"type": "long"}
#             }
#         }
#     },
#     "aliases": {}
# }

ssa_etl_state_template = {
    "order": 0,
    "template": "etl-state",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "count": {"type": "long"},
                "flow": {"type": "keyword", "index": "not_analyzed"},
                "flow_id": {"type": "keyword", "index": "not_analyzed"},
                "state": {"properties": {
                    "count": {"type": "long"},
                    "failure": {"type": "long"},
                    "fix": {"type": "long"},
                    "input": {"type": "long"},
                    "output": {"type": "long"},
                },
                }
            }
        }
    },
    "aliases": {}
}

# ssa_jingzong_template = {
#     "order": 0,
#     "template": "jingzong-*",
#     "settings": {
#         "index": {
#             "refresh_interval": "5s"
#         }
#     },
#     "mappings": {
#         "result": {
#             "dynamic_templates": [
#                 {
#                     "notanalyzed": {
#                         "mapping": {
#                             "index": "not_analyzed",
#                             "type": "string",
#                             "doc_values": "true"
#                         },
#                         "match_mapping_type": "string",
#                         "match": "*"
#                     }
#                 }
#             ],
#             "_all": {
#                 "omit_norms": True,
#                 "enabled": True
#             },
#             "properties": {
#                 "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
#                 "organization": {"type": "keyword", "index": "not_analyzed"},
#                 "operate_time": {"type": "date", "format": "yyyyMMddHHmmss"},
#                 "reg_id": {"type": "long"},
#                 "operate_type": {"type": "long"},
#                 "num_id": {"type": "keyword"},
#                 "error_code": {"type": "long"},
#                 "organization_id": {"type": "long"},
#                 "user_id": {"type": "long"},
#                 "operate_result": {"type": "long"},
#                 "operate_condition": {"type": "keyword", "index": "not_analyzed"},
#                 "operate_name": {"type": "keyword", "index": "not_analyzed"},
#                 "user_name": {"type": "keyword", "index": "not_analyzed"},
#                 "terminal_id": {"type": "keyword", "index": "not_analyzed"},
#
#             }
#         }
#     },
#     "aliases": {}
# }

# 摆渡流量
ssa_ag_bd_template = {
    "order": 0,
    "template": "ssa-ag-bd-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "comp_ip": {"type": "string", "index": "not_analyzed"},
                "task_id": {"type": "string", "index": "not_analyzed"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "long"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "long"},
                "file_name": {"type": "string", "index": "not_analyzed"},
                "file_size": {"type": "long"},
                "is_success": {"type": "long"},
                "starttime": {"type": "date", "format": "yyyyMMddHHmmss"},
                "endtime": {"type": "date", "format": "yyyyMMddHHmmss"},
                "note": {"type": "string", "index": "not_analyzed"}
            }
        }
    },
    "aliases": {}
}

# 隔离文件
ssa_ag_gl_template = {
    "order": 0,
    "template": "ssa-ag-gl-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "comp_ip": {"type": "string", "index": "not_analyzed"},
                "task_id": {"type": "string", "index": "not_analyzed"},
                "proto": {"type": "long"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "long"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "long"},
                "send_flow_statis": {"type": "long"},
                "recv_flow_statis": {"type": "long"},
                "is_normal": {"type": "long"},
                "starttime": {"type": "date", "format": "yyyyMMddHHmmss"},
                "endtime": {"type": "date", "format": "yyyyMMddHHmmss"},
                "note": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端日志
ssa_ag_all_terminal_template = {
    "order": 0,
    "template": "ssa-ag-all-terminal-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "long"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "act_type": {"type": "string", "index": "not_analyzed"},
                "app_path": {"type": "string", "index": "not_analyzed"},
                "app_name": {"type": "string", "index": "not_analyzed"},
                "login_ip": {"type": "string", "index": "not_analyzed"},
                "login_name": {"type": "string", "index": "not_analyzed"},
                "os_username": {"type": "string", "index": "not_analyzed"},
                "login_type": {"type": "long"},
                "login_result": {"type": "long"},
                "ie_name": {"type": "string", "index": "not_analyzed"},
                "file_name": {"type": "string", "index": "not_analyzed"},
                "user_ip": {"type": "string", "index": "not_analyzed"},
                "request_type": {"type": "long"},
                "request_name": {"type": "string", "index": "not_analyzed"},
                # "request_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "approver_name": {"type": "string", "index": "not_analyzed"},
                "approve_time": {"type": "string", "index": "not_analyzed"},
                "dev_name": {"type": "string", "index": "not_analyzed"},
                "print_doc": {"type": "string", "index": "not_analyzed"},
                "file_path": {"type": "string", "index": "not_analyzed"},
                "act_info": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端程序日志
ssa_ag_zd_cx_template = {
    "order": 0,
    "template": "ssa-ag-zd-cx-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "act_type": {"type": "string", "index": "not_analyzed"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "app_path": {"type": "string", "index": "not_analyzed"},
                "app_name": {"type": "string", "index": "not_analyzed"},
                "log_id": {"type": "long"},
            }
        }
    },
    "aliases": {}
}

# 终端登录日志
ssa_ag_zd_dl_template = {
    "order": 0,
    "template": "ssa-ag-zd-dl-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "login_ip": {"type": "string", "index": "not_analyzed"},
                "login_name": {"type": "string", "index": "not_analyzed"},
                "os_username": {"type": "string", "index": "not_analyzed"},
                "login_type": {"type": "long"},
                "login_result": {"type": "long"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "log_id": {"type": "long"},
            }
        }
    },
    "aliases": {}
}

# 终端浏览网页日志
ssa_ag_zd_ll_template = {
    "order": 0,
    "template": "ssa-ag-zd-ll-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "ie_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "log_id": {"type": "long"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端历史文件浏览日志
ssa_ag_zd_ls_template = {
    "order": 0,
    "template": "ssa-ag-zd-ls-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "file_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "log_id": {"type": "long"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端设备审批日志
ssa_ag_zd_sp_template = {
    "order": 0,
    "template": "ssa-ag-zd-sp-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "user_ip": {"type": "string", "index": "not_analyzed"},
                "request_type": {"type": "long"},
                "request_name": {"type": "string", "index": "not_analyzed"},
                "act_type": {"type": "long"},
                "request_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "approver_name": {"type": "string", "index": "not_analyzed"},
                "approve_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "dev_name": {"type": "string", "index": "not_analyzed"},
                "print_doc": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端刻录文件日志
ssa_ag_zd_kl_template = {
    "order": 0,
    "template": "ssa-ag-zd-kl-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "file_path": {"type": "string", "index": "not_analyzed"},
                "file_name": {"type": "string", "index": "not_analyzed"},
                "log_id": {"type": "long"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端移动盘拷贝日志
ssa_ag_zd_uc_template = {
    "order": 0,
    "template": "ssa-ag-zd-uc-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "act_type": {"type": "long"},
                "act_info": {"type": "string", "index": "not_analyzed"},
                "log_id": {"type": "long"},
                "act_ip": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 防火墙
firewall_template = {
    "order": 0,
    "template": "ssa-ag-fw-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "long"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "long"},
                "provider_id": {"type": "string", "index": "not_analyzed"},
                "device_name": {"type": "string", "index": "not_analyzed"},
                "level": {"type": "long"},
                "event_type": {"type": "string", "index": "not_analyzed"},
                "event_name": {"type": "string", "index": "not_analyzed"},
                "event_digest": {"type": "string", "index": "not_analyzed"},
                "protocol": {"type": "string", "index": "not_analyzed"},
                "src_mac": {"type": "string", "index": "not_analyzed"},
                "dst_mac": {"type": "string", "index": "not_analyzed"},
                "username": {"type": "string", "index": "not_analyzed"},
                "program": {"type": "string", "index": "not_analyzed"},
                "operation": {"type": "string", "index": "not_analyzed"},
                "object": {"type": "string", "index": "not_analyzed"},
                "result": {"type": "string", "index": "not_analyzed"},
                "response": {"type": "string", "index": "not_analyzed"},
                "msg": {"type": "string", "index": "not_analyzed"},
                "flow": {"type": "long"},
                "deny_re": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 摆渡机隔离设备事件
ssa_event_bdgl_template = {
    "order": 0,
    "template": "ssa-event-bdgl-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "event_id": {"type": "string", "index": "not_analyzed"},
                "event_type": {"type": "long"},
                "app": {"type": "string", "index": "not_analyzed"},
                "event_path": {"type": "string", "index": "not_analyzed"},
                "app_name": {"type": "string", "index": "not_analyzed"},
                "level": {"type": "long"},
                "event_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "subject": {"type": "string", "index": "not_analyzed"},
                "content": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 终端事件：
ssa_event_terminal_template = {
    "order": 0,
    "template": "ssa-event-terminal-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "event_id": {"type": "string", "index": "not_analyzed"},
                "event_top_type": {"type": "string", "index": "not_analyzed"},
                "event_type": {"type": "string", "index": "not_analyzed"},
                "event_source": {"type": "string", "index": "not_analyzed"},
                "event_index": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "event_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "remark": {"type": "string", "index": "not_analyzed"},
                "terminal": {"type": "string", "index": "not_analyzed"},
                "organization": {"type": "string", "index": "not_analyzed"},
                "event_level": {"type": "long"},
            }
        }
    },
    "aliases": {}
}

# 事件评分
score_template = {
    "order": 0,
    "template": "score-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "ip": {"type": "string", "index": "not_analyzed"},
                "event_time": {"type": "date", "format": "yyyyMMddHH"},
                "source": {"type": "string", "index": "not_analyzed"},
                "level": {"type": "long"},
                "num": {"type": "long"},
                "score": {"type": "long"},
            }
        }
    },
    "aliases": {}
}

# 数据库审计
ssa_ag_database_template = {
    "order": 0,
    "template": "ssa-ag-database-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "id": {"type": "string", "index": "not_analyzed"},
                "provider_id": {"type": "string", "index": "not_analyzed"},
                "event_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "transport_protocol": {"type": "string", "index": "not_analyzed"},
                "app_protocol": {"type": "string", "index": "not_analyzed"},
                "level": {"type": "string", "index": "not_analyzed"},
                "dev_ip": {"type": "string", "index": "not_analyzed"},
                "server_ip": {"type": "string", "index": "not_analyzed"},
                "client_ip": {"type": "string", "index": "not_analyzed"},
                "server_port": {"type": "string", "index": "not_analyzed"},
                "redirect_port": {"type": "string", "index": "not_analyzed"},
                "client_port": {"type": "string", "index": "not_analyzed"},
                "server_mac": {"type": "string", "index": "not_analyzed"},
                "client_mac": {"type": "string", "index": "not_analyzed"},
                "ruleset_name": {"type": "string", "index": "not_analyzed"},
                "rule_name": {"type": "string", "index": "not_analyzed"},
                "bizaccout": {"type": "string", "index": "not_analyzed"},
                "auth_account": {"type": "string", "index": "not_analyzed"},
                "policy_id": {"type": "long"},
                "rule_id": {"type": "long"},
                "rule_templet_id": {"type": "long"},
                "direction": {"type": "string", "index": "not_analyzed"},
                "response_time": {"type": "long"},
                "error_code": {"type": "long"},
                "block": {"type": "string", "index": "not_analyzed"},
                "record_rows": {"type": "long"},
                "sql": {"type": "string", "index": "not_analyzed"},
                "client_host": {"type": "string", "index": "not_analyzed"},
                "server_host": {"type": "string", "index": "not_analyzed"},
                "library": {"type": "string", "index": "not_analyzed"},
                "client_software": {"type": "string", "index": "not_analyzed"},
                "client_user": {"type": "string", "index": "not_analyzed"},
                "instance_name": {"type": "string", "index": "not_analyzed"},
                "db_name": {"type": "string", "index": "not_analyzed"},
                "table_name": {"type": "string", "index": "not_analyzed"},
                "object_name": {"type": "string", "index": "not_analyzed"},
                "cmd": {"type": "string", "index": "not_analyzed"},
                "subcmd": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# IDS
ssa_ag_ids_template = {
    "order": 0,
    "template": "ssa-ag-ids-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "source": {"type": "string", "index": "not_analyzed"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "string", "index": "not_analyzed"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "string", "index": "not_analyzed"},
                "type_id": {"type": "long"},
                "name": {"type": "string", "index": "not_analyzed"},
                "cve_id": {"type": "long"},
                "fingerprint": {"type": "string", "index": "not_analyzed"},
                "level": {"type": "long"},
                "internal_id": {"type": "string", "index": "not_analyzed"},
                "provider_id": {"type": "string", "index": "not_analyzed"},
                "event_name": {"type": "string", "index": "not_analyzed"},
                "src_mac": {"type": "string", "index": "not_analyzed"},
                "dst_mac": {"type": "string", "index": "not_analyzed"},
                "event_count": {"type": "long"},
                "protocol": {"type": "string", "index": "not_analyzed"},
                "response": {"type": "string", "index": "not_analyzed"},
                "action": {"type": "string", "index": "not_analyzed"},
                "description": {"type": "string", "index": "not_analyzed"},
                "securityid": {"type": "long"},
                "attackid": {"type": "long"},
            }
        }
    },
    "aliases": {}
}

# 360
ssa_ag_360_template = {
    "order": 0,
    "template": "ssa-ag-360-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "host_ip": {"type": "string", "index": "not_analyzed"},
                "computer_name": {"type": "string", "index": "not_analyzed"},
                "infectedfileinfo_code": {"type": "string", "index": "not_analyzed"},
                "infectedfileinfo_cleared": {"type": "long"},
                "infectedfileinfo_filehash": {"type": "string", "index": "not_analyzed"},
                "infectedfileinfo_filepath": {"type": "string", "index": "not_analyzed"},
                "infectedfileinfo_custommediatype": {"type": "string", "index": "not_analyzed"},
                "infectedfileinfo_mediatype": {"type": "long"},
                "time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "utcms": {"type": "date", "format": "yyyyMMddHHmmss"},
                "custominitiativedefencesource": {"type": "string", "index": "not_analyzed"},
                "initiativedefencecode": {"type": "string", "index": "not_analyzed"},
                "customsource": {"type": "string", "index": "not_analyzed"},
                "mainsourcecode": {"type": "string", "index": "not_analyzed"},
                "taskid": {"type": "long"},
                "custommediatype": {"type": "string", "index": "not_analyzed"},
                "mediatype": {"type": "string", "index": "not_analyzed"},
                "clearedfilenumber": {"type": "long"},
                "infectedfilenumber": {"type": "long"},
                "customtype": {"type": "string", "index": "not_analyzed"},
                "virusfingerprint": {"type": "string", "index": "not_analyzed"},
                "virustype": {"type": "string", "index": "not_analyzed"},
                "virusname": {"type": "string", "index": "not_analyzed"},
                "provider_id": {"type": "string", "index": "not_analyzed"},
            }
        }
    },
    "aliases": {}
}

# 事件统计
event_template = {
    "order": 0,
    "template": "event-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "string", "index": "not_analyzed"},
                "protocol": {"type": "string", "index": "not_analyzed"},
                "event_top_type": {"type": "string", "index": "not_analyzed"},
                "event_type": {"type": "string", "index": "not_analyzed"},
                "event_source": {"type": "string", "index": "not_analyzed"},
                "start_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "end_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "organization": {"type": "string", "index": "not_analyzed"},
                "event_total": {"type": "long"},
                "terminal": {"type": "string", "index": "not_analyzed"},
                "event_level": {"type": "long"}
            }
        }
    },
    "aliases": {}
}

ssa_ag_zt_basic_template = {
    "order": 0,
    "template": "ssa-ag-zt-basic-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "devip": {"type": "string", "index": "not_analyzed"},
                "computer_name": {"type": "string", "index": "not_analyzed"},
                "current_user_name": {"type": "string", "index": "not_analyzed"},
                "cpu_info": {"type": "string", "index": "not_analyzed"},
                "os_info": {"type": "string", "index": "not_analyzed"},
                "memory_info": {"type": "string", "index": "not_analyzed"},
                "mac_address": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
            }
        }
    },
    "aliases": {}
}

# 终端安装软件表
ssa_ag_zt_soft_template = {
    "order": 0,
    "template": "ssa-ag-zt-soft-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "devip": {"type": "string", "index": "not_analyzed"},
                "software_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
            }
        }
    },
    "aliases": {}
}

# 日志统计
statistics_template = {
    "order": 0,
    "template": "statistics-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "string", "index": "not_analyzed"},
                "protocol": {"type": "string", "index": "not_analyzed"},
                "log_top_type": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "log_total": {"type": "long"},
                "start_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "end_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "organization": {"type": "string", "index": "not_analyzed"},
                "terminal": {"type": "string", "index": "not_analyzed"},
                "log_flow": {"type": "long"},
                "log_source": {"type": "string", "index": "not_analyzed"}
            }
        }
    },
    "aliases": {}
}

ssa_ag_zt_share_template = {
    "order": 0,
    "template": "ssa-ag-zt-share-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "devip": {"type": "string", "index": "not_analyzed"},
                "share_name": {"type": "string", "index": "not_analyzed"},
                "folder_path": {"type": "string", "index": "not_analyzed"},
                "share_des": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
            }
        }
    },
    "aliases": {}
}

# 终端用户信息表
ssa_ag_zt_user_template = {
    "order": 0,
    "template": "ssa-ag-zt-user-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "agent_id": {"type": "string", "index": "not_analyzed"},
                "log_type": {"type": "string", "index": "not_analyzed"},
                "term_ip": {"type": "string", "index": "not_analyzed"},
                "term_computer_name": {"type": "string", "index": "not_analyzed"},
                "term_duty": {"type": "string", "index": "not_analyzed"},
                "term_group_id": {"type": "string", "index": "not_analyzed"},
                "term_group_name": {"type": "string", "index": "not_analyzed"},
                "devip": {"type": "string", "index": "not_analyzed"},
                "group_name": {"type": "string", "index": "not_analyzed"},
                "user_name": {"type": "string", "index": "not_analyzed"},
                "act_time": {"type": "date", "format": "yyyyMMddHHmmss"},
            }
        }
    },
    "aliases": {}
}

# 事件表
all_event_template = {
    "order": 0,
    "template": "all-event-*",
    "settings": {
        "index": {
            "refresh_interval": "5s"
        }
    },
    "mappings": {
        "result": {
            "dynamic_templates": [
                {
                    "notanalyzed": {
                        "mapping": {
                            "index": "not_analyzed",
                            "type": "string",
                            "doc_values": "true"
                        },
                        "match_mapping_type": "string",
                        "match": "*"
                    }
                }
            ],
            "_all": {
                "omit_norms": True,
                "enabled": True
            },
            "properties": {
                "@timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "event_host": {"type": "string", "index": "not_analyzed"},
                "event_one_type": {"type": "string", "index": "not_analyzed"},
                "event_two_type": {"type": "string", "index": "not_analyzed"},
                "event_three_type": {"type": "string", "index": "not_analyzed"},
                "event_source": {"type": "long"},
                "src_ip": {"type": "string", "index": "not_analyzed"},
                "dst_ip": {"type": "string", "index": "not_analyzed"},
                "src_port": {"type": "string", "index": "not_analyzed"},
                "dst_port": {"type": "string", "index": "not_analyzed"},
                "tran_protocol": {"type": "string", "index": "not_analyzed"},
                "app_protocol": {"type": "string", "index": "not_analyzed"},
                "start_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "end_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "stastic_time": {"type": "date", "format": "yyyyMMddHHmmss"},
                "opt_result": {"type": "long"},
                "flow": {"type": "long"},
                "event_level": {"type": "long"},
                "organization": {"type": "string", "index": "not_analyzed"},
                "event_total": {"type": "long"},
                "event_contents": {"type": "string", "index": "not_analyzed"},
                "event_detail": {"type": "string", "index": "not_analyzed"},

            }
        }
    },
    "aliases": {}
}


def create_index_template(mapping, index_tempalte):
    """
    设置
    :return:
    """
    es_host = settings.ELASTICSEARCH_HOSTS
    host = es_host[0]
    if not host.endswith('/'):
        host += "/"

    template_name = index_tempalte["template"]
    # 检查是否已经存在相应的模板
    url = host + "_template/" + mapping
    response = requests.head(url)
    if response.status_code == 200:
        print("模板: [%s] 已经存在" % template_name)
    else:
        # 创建模板
        response = requests.put(url, data=json.dumps(index_tempalte))
        if response.status_code == 200:
            print("成功创建模板: [%s] " % template_name)
        else:
            print("失败！创建模板: [{}] {}".format(template_name, response.text))


if __name__ == "__main__":
    # print(os.path.abspath(os.path.dirname(__file__)))
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")
    import django

    django.setup()
    # 态势感知数据结果模板


    # create_index_template('ssa-ag-zd-cx', ssa_ag_zd_cx_template)
    # create_index_template('ssa-ag-zd-dl', ssa_ag_zd_dl_template)
    # create_index_template('ssa-ag-zd-ll', ssa_ag_zd_ll_template)
    # create_index_template('ssa-ag-zd-ls', ssa_ag_zd_ls_template)
    # create_index_template('ssa-ag-zd-sp', ssa_ag_zd_sp_template)
    # create_index_template('ssa-ag-zd-kl', ssa_ag_zd_kl_template)
    # create_index_template('ssa-ag-zd-uc', ssa_ag_zd_uc_template)

    create_index_template('ssa-ag-all-terminal', ssa_ag_all_terminal_template)

    create_index_template('ssa-ag-bd', ssa_ag_bd_template)
    create_index_template('ssa-ag-gl', ssa_ag_gl_template)

    create_index_template('all-event', all_event_template)
    create_index_template('ssa-ag-fw', firewall_template)
    create_index_template('ssa-ag-zt-basic', ssa_ag_zt_basic_template)
    create_index_template('ssa-ag-zt-soft', ssa_ag_zt_soft_template)
    create_index_template('ssa-ag-zt-share', ssa_ag_zt_share_template)
    create_index_template('ssa-ag-zt-user', ssa_ag_zt_user_template)
    #
    create_index_template('ssa-event-terminal', ssa_event_terminal_template)
    create_index_template('ssa-event-bdgl', ssa_event_bdgl_template)
    #
    create_index_template('ssa-ag-database', ssa_ag_database_template)
    create_index_template('ssa-ag-ids', ssa_ag_ids_template)
    create_index_template('ssa-ag-360', ssa_ag_360_template)
    #
    create_index_template('event', event_template)
    create_index_template('statistics', statistics_template)
    create_index_template('score', score_template)



    # create_index_template('ssa-event-terminal', ssa_event_terminal_template)

    # curl - XPUT localhost:9200/_template/soc-ssa/ -d ''
