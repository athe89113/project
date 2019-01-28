<style scoped>
    .conf-border{
        background-color: rgba(30, 36, 53, 0.25);
        padding: 20px 10px;
    }
    .conf {
        margin: 0 auto;
        height: 100%;
    }

    .conf-item {
        background-color: rgba(0, 0, 0, 0.2);
        padding-bottom: 20px;
    }

    .conf-item-title {
        height: 36px;
        line-height: 36px;
    }

    .conf-item-title:before {
        content: '';
        width: 232px;
        height: 36px;
        background: url('../../assets/images/ys-display-box-title-tag.png');
        background-size: 232px;
        position: absolute;
        left: 10px;
    }

    .conf-input {
        width: 100%;
        height: 38px;
    }

    .input-border {
        width: 90%;
        margin: 20px auto 0;
        text-align: center;
    }

    .conf-btn {
        width: 200px;
        height: 34px;
    }

    .conf-textarea {
        min-height: 90px;
        padding: 7px 12px;
        height: 90px;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.2);
        font-size: 12px;
        border-radius: 3px;
        cursor: text;
        border: 1px solid rgba(74, 146, 255, 0.2);
        box-shadow: inset 1px 1px 3px 0px rgba(0, 0, 0, 0.2);
        resize: vertical;
    }

    .icon-color {
        color: #e96157;
    }
</style>
<template>
    <div class="conf-border">
        <div class="conf">
        <div v-for="item in confData" :class="['col-md-6', 'p-l-10', 'p-r-10', {'m-t-20': $index>1}]">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span v-if="(item.type == 'Thread' || item.type == 'White_list') && item.conftype == 'vulscan'"
                          class="m-l-10">扫描引擎{{ item.info }}</span>
                    <span v-if="(item.type == 'Thread' || item.type == 'White_list') && item.conftype == 'nascan'"
                          class="m-l-10">爬虫引擎{{ item.info }}</span>
                    <span v-if="item.type != 'Thread' && item.type != 'White_list'" class="m-l-10">{{ item.info
                        }}</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden;white-space:normal !important;">
                                <p style="width: 220px; word-wrap: break-word;">{{item.help}}</p>
                            </div>
                        </div>
                        <span>
							<i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
						</span>
                    </tooltip>
                    <ys-switch v-if="item.type == 'Masscan' || item.type == 'Port_list'" class="fRight m-r-20 m-t-10"
                               :checked.sync="item.status"
                               @on-change="goKeyDownSearch(item.type, item.status?1:0, item.conftype)">
                        <span slot="open">开启</span>
                        <span slot="close">关闭</span>
                    </ys-switch>
                </div>
                <div class="input-border">
                    <div v-if="item.type == 'Masscan'" class="col-md-6">
                        <input class="ys-input conf-input input-path" placeholder="路径" :value="item.path"
                               v-model="path"/>
                    </div>
                    <div v-if="item.type == 'Masscan'" class="col-md-6">
                        <input class="ys-input conf-input input-speed" placeholder="速率" :value="item.speed"
                               v-model="speed"/>
                    </div>
                    <input v-if="item.show == 'word' && item.type != 'Masscan'" class="ys-input conf-input input-normal"
                           v-model="item.value"/>
                    <textarea v-if="item.show == 'list'" class="conf-textarea" v-model="item.value"></textarea>
                    <button v-if="item.type == 'Masscan'" class="ys-btn ys-btn-blue m-t-10 conf-btn"
                            @click="goKeyDownSearch(item.type, speed+'|'+path, item.conftype)">更新
                    </button>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" v-else
                            @click="goKeyDownSearch(item.type, item.value, item.conftype)">更新
                    </button>
                </div>
            </div>
        </div>
        <div class="clearfix"></div>
        <!--<div class="col-md-6 p-l-10 p-r-10">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">爬虫引擎最大线程数</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>爬虫引擎的最大线程数限制</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({reptileMaxLine:reptileMaxLine})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">连接超时时间(TCP)</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>WEB请求的超时时间，socket连接超时为值的一半。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <input class="ys-input conf-input" v-model="linkOvertime"/>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({linkOvertime:linkOvertime})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">资产探测周期</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>设置资产探测的扫描周期，格式：天数|</p>
                                <p>小时，例如 5|16，即每5天的16点开始</p>
                                <p>进行扫描。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <input class="ys-input conf-input" v-model="resDetectionPeriod"/>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({resDetectionPeriod:resDetectionPeriod})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">扫描引擎最大线程数</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>漏洞扫描的并发线程数</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <input class="ys-input conf-input" v-model="searchMaxLine"/>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({searchMaxLine: searchMaxLine})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">请求超时时间</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>插件扫描时会使用此参数作为连接超时</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <input class="ys-input conf-input" v-model="reqOvertime"/>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({reqOvertime:reqOvertime})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">cms识别规则</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>用于识别WEB的CMS，格式：CMS名称|判断方</p>
                                <p>式|判断对象|判断正则。识别信息保存于tag</p>
                                <p>记录中，可使用tag:dedecms方式进行搜索。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="recognitionRule"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({recognitionRule:recognitionRule})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">代码语言识别规则</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>用于识别WEB的开发语言，识别信息保存于tag</p>
                                <p>记录中，可使用tag:php方式进行搜索。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="codeLanguage"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({codeLanguage:codeLanguage})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">组件容器识别规则</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>用于识别WEB的容器、中间件等组件信息，</p>
                                <p>格式：组件名称|判断方式|判断对象|判</p>
                                <p>断正则。识别信息保存于tag记录中，可</p>
                                <p>使用tag:tomcat方式进行搜索。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="componentContainer"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({componentContainer:componentContainer})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">网络资产探测列表(必填)</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>指定爬虫引擎探测范围，格式：192.16</p>
                                <p>8.1.1-192.168.1.254(修改会立刻触</p>
                                <p>发资产扫描收集)</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="netRes"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({netRes:netRes})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">端口探测列表(TCP探测)</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>默认探测端口列表，可开启ICMP，开启</p>
                                <p>后只对存活的IP地址进行探测</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                    <ys-switch class="fRight m-r-20 m-t-8" :checked.sync="portSearchStatus">
                        <span slot="open">on</span>
                        <span slot="close">off</span>
                    </ys-switch>
                    <span class="fRight m-r-10">存活探测(ICMP)</span>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="portSearch"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({portSearch:portSearch,status: portSearchStatus})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">服务类型识别规则</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>用于识别开放端口上所运行的服务信息，格式:服</p>
                                <p>务名称|端口号|匹配模式|匹配正则，结果以正则</p>
                                <p>匹配为优先，无正则内容时使用端口号进行默认</p>
                                <p>匹配，再无结果时即主动发送探测包进行识别，识</p>
                                <p>别结果保存于server记录中，可使用server:ftp/p>
                                <p>方式进行搜索<</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="serverType"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({serverType:serverType})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">资产发现白名单</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>不对白名单内的IP列表进行资产发现</p>
                                <p>。格式：x.x.x.x，以行分割</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="resFind"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({resFind:resFind})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">扫描引擎白名单</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>不对白名单内的IP列表进行漏洞检测</p>
                                <p>。格式：x.x.x.x，以行分割</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <textarea class="conf-textarea" v-model="whiteName"></textarea>
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({whiteName:whiteName})">更新</button>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-l-10 p-r-10 m-t-20">
            <div class="conf-item">
                <div class="conf-item-title">
                    <span class="m-l-10">弱口令字典</span>
                    <tooltip :placement="'bottom'" class="m-l-10" :visible.sync="true">
                        <div slot="content">
                            <div style="padding: 10px 10px 10px 10px;overflow: hidden">
                                <p>弱口令列表，部分漏洞检测插件会</p>
                                <p>调用此列表进行弱口令检测。格式：</p>
                                <p>以行分割，不支持中文密码。</p>
                            </div>
                        </div>
                        <span>
                            <i class="ys-icon icon-warn-outline icon-color text-cursor"></i>
                        </span>
                    </tooltip>
                </div>
                <div class="input-border">
                    <button class="ys-btn ys-btn-blue m-t-10 conf-btn" @click="goKeyDownSearch({weakPassword:weakPassword})">更新</button>
                </div>
            </div>
        </div>-->
    </div>
    </div>
</template>
<script>
    import Api from '../../lib/api'

    export default {
        name: "scn-scan",
        data() {
            return {
                openPath: '',
                openSpeed: '',
                openStatus: true,
                reptileMaxLine: '',
                linkOvertime: '',
                resDetectionPeriod: '',
                searchMaxLine: '',
                reqOvertime: '',
                recognitionRule: '',
                codeLanguage: '',
                componentContainer: '',
                netRes: '',
                portSearch: '',
                portSearchStatus: true,
                serverType: '',
                resFind: '',
                whiteName: '',
                weakPassword: '',
                confData: [],
                path: '',
                speed: '',
                val: ''
            }
        },
        ready() {
            this.getConfData();
        },
        methods: {
            goKeyDownSearch(type, value, conftype) {
                if (!value.toString() || value == 0) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '请输入配置信息';
                    return false;
                }
                let data = {
                    type: type,
                    value: value,
                    conftype: conftype
                };
                this.$http.post('/api/scan/config/update', data).then(function (res) {
                    if (res.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.$root.errorMsg = '更新成功'
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = res.data.msg
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getConfData() {
                this.$http.post('/api/scan/config/info', '').then(function (res) {
                    if (res.data.status == 200) {
                        this.confData = res.data.data;
                        for (let key in this.confData) {
                            if (this.confData[key].type == 'Port_list') {
                                this.confData[key].value = this.confData[key].value.split('|')[1];
                                this.confData[key].status = this.confData[key].value.split('|')[0] == 0 ? false : true;
                            } else if (this.confData[key].type == 'Masscan') {
                                this.confData[key].speed = this.confData[key].value.split('|')[1];
                                this.confData[key].path = this.confData[key].value.split('|')[2];
                                this.confData[key].status = this.confData[key].value != '0|1' ? false : true;
                            }
                        }
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            }
        }
    }
</script>
