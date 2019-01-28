<template>
    <div class="ys-con pos-r">
        <!--<div class="search-result ys-box-con ys-wrap" v-show="showSearch">
            <p class="textC" style="margin-top: 100px"><img src="../../assets/images/ip-search.png"
                                                            style="width:150px;"/></p>
            <div class="textC">
                <div class="search-input-box">
                    <div class="pos-r">
                        <input class="ys-input" placeholder="例：192.168.10.10:8888" v-model="searchValue"
                               @keydown="goKeyDownSearch($event)"/>
                        <tooltip id="search-tip" class="fRight" :placement="'top'" :visible.sync="true">
                            <div slot="content">
                                <div style="width:440px;overflow:hidden;padding: 10px 0px 10px 10px">
                                    <p>1.按端口： port:端口号 eg. port:22</p>
                                    <p>2.按banner： banner:banner内容关键词 eg. banner:ftp</p>
                                    <p>3.按ip(支持c段，b段模糊查询)： ip:ip地址  eg. ip:192.168.1.1／ip:192.168.1.</p>
                                    <p>4.按服务名： server:服务名  eg. server:iis</p>
                                    <p>5.按标题： title:标题内容关键词 eg. title:xxx管理系统</p>
                                    <p>6.按服务类型标签： tag:服务类型 eg. tag:apache</p>
                                    <p>7.按主机名： hostname:主机名 eg. hostname:server001</p>
                                    <p>8.全局模糊： all:查询内容  eg. all:tongcheng</p>
                                    <p>9.多条件： 条件1:内容1;条件2:内容2  eg. ip:192.168.1.1;port:22</p>
                                </div>
                            </div>
                            <span>
                            <i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                          </span>
                        </tooltip>
                    </div>
                </div>
            </div>
            <div class="textC m-t-20">
                <button class="ys-btn ys-btn-green" @click="goSearch()"><i class="ys-icon icon-search"></i>查询</button>
            </div>
        </div>-->
        <div class="search-result-box ys-box-con">
            <!--<div class="ys-box-con m-t-15">
                <div class="clearfix">
                    <table>
                        <tr>
                            <td>
                                <span class="ys-info-color">新增目标标签：</span>
                            </td>
                            <td>
                                <div class="tag-box m-r-10" v-for="list in addData" track-by="$index">
                                    <div class="ys-tag" @mouseover="list.remove=true" @mouseout="list.remove=false">
                                        <span class="d-i-b textC" style="min-width: 140px">192.168.123.321:8000</span>
                                        <span v-show="list.remove" class="remove text-cursor"
                                              @click="removeAddData(list,$index)"><i
                                                class="ys-icon icon-remove"></i></span>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>-->
            <div class="tool-box">
                <div class="pos-r fLeft">
                    <div class="ys-search d-i-b">
                        <input class="ys-input" placeholder="例：192.168.10.10:8888" style="width: 180px;"
                               v-model="searchValue"
                               @keydown="goKeyDownSearch($event)"/>
                        <button class="ys-search-btn" @click="goSearch()">
                            <i class="ys-icon icon-search"></i>
                        </button>
                    </div>
                    <tooltip id="search-tip" :delay="400" class="fRight" :placement="'bottom'" :visible.sync="true">
                        <div slot="content">
                            <div style="width:440px;overflow:hidden;padding: 10px 0px 10px 10px">
                                <p>1.按端口： port:端口号 eg. port:22</p>
                                <p>2.按banner： banner:banner内容关键词 eg. banner:ftp</p>
                                <p>3.按ip(支持c段，b段模糊查询)： ip:ip地址  eg. ip:192.168.1.1／ip:192.168.1.</p>
                                <p>4.按服务名： server:服务名  eg. server:iis</p>
                                <p>5.按标题： title:标题内容关键词 eg. title:xxx管理系统</p>
                                <p>6.按服务类型标签： tag:服务类型 eg. tag:apache</p>
                                <p>7.按主机名： hostname:主机名 eg. hostname:server001</p>
                                <p>8.全局模糊： all:查询内容  eg. all:tongcheng</p>
                                <p>9.多条件： 条件1:内容1;条件2:内容2  eg. ip:192.168.1.1;port:22</p>
                            </div>
                        </div>
                        <span>
                            <i style="margin-top: 2px; margin-left: 10px;"
                               class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                          </span>
                    </tooltip>
                </div>
                <div class="fRight">
                    <button class="ys-btn ys-btn-blue m-r-5" @click="addTask()"><i class="ys-icon icon-add-circle"></i>新增任务
                    </button>
                </div>
                <div class="fRight m-r-20">
                    <span class="verticalM m-l-10">当前生成结果共计<span
                            class="ys-success-color m-l-5 m-r-5">{{whole}}</span>个</span>
                </div>
            </div>
            <div class="clearfix"></div>

            <div class="m-t-10">
                <table class="ys-table">
                    <thead>
                    <tr>
                        <th>
                            <checkbox :show.sync="checkAll" :text="''" @ys-click="checkAllData"></checkbox>
                        </th>
                        <th>IP端口</th>
                        <th>时间</th>
                        <th>类型</th>
                        <th>服务</th>
                        <th>程序名称</th>
                        <th>详情</th>
                    </tr>
                    </thead>
                    <tbody v-for="list in tableList" track-by="$index">
                    <tr>
                        <td>
                            <checkbox :show.sync="list.selected" :text="''"></checkbox>
                        </td>
                        <td>
                            <a v-if="list.webinfo && list.webinfo.title != ''" :href="'http://'+list.ip+':'+list.port"
                               target="_blank">{{list.ip}}:{{list.port}}</a>
                            <span v-else>{{list.ip}}:{{list.port}}</span>
                        </td>
                        <td>{{list.time}}</td>
                        <td class="color-5c">{{list.server}}</td>
                        <td v-if="!list.webinfo"></td>
                        <td v-else>
                            <span class="displayIB p-r-5 p-l-5 color-59" v-for="tag in list.webinfo.tag">{{tag}}</span>
                        </td>
                        <td class="color-dc" v-if="!list.webinfo"></td>
                        <td class="color-dc" v-else="!list.webinfo">{{list.webinfo.title}}</td>
                        <td class="detail">
                                <span @click="showDetail(list._id)"><i class="ys-icon"
                                                                       v-bind:class="[curDetailId == list._id ? 'icon-downlist-up' : 'icon-downlist' ]"></i></span>
                        </td>
                    </tr>
                    <tr class="detail" v-bind:class="[curDetailId == list._id ? 'open' : '' ]">
                        <td colspan="7">
                            <div class="search-table-detail p-l-30 p-r-40">
                                hostname: {{list.hostname}} <br/>
                                banner:
                                <pre class="ys-info-color" style="border: none;">
                                      <code>{{list.banner}}</code>
                                    </pre>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table-data :url='tableUrl'
                            :filter.sync="tableFilter"
                            :data.sync="tableList"
                            :whole.sync="whole"
                            :search.sync="searchValue"
                            v-ref:table></table-data>
            </div>
        </div>
    </div>
    <!--<aside :show.sync="showAddConf" :header="'新增目标'" :width="'600px'" :left="'auto'">
        <textarea class="ys-textarea" placeholder="ip:端口 以','分割开" v-model="addConfInfo" name="" cols="30"
                  rows="10"></textarea>
        <div class="aside-foot m-t-20">
            <button class="ys-btn m-r-10" @click="saveAddconf">完成</button>
            <button class="ys-btn ys-btn-white" @click="showAddConf=false">取消</button>
        </div>
    </aside>-->

    <aside :show.sync="showAddTask" :header="'新增任务'" :width="'600px'" :left="'auto'">
        <table class="ys-form-table">
            <tr>
                <td>任务名称</td>
                <td>
                    <input class="ys-input" v-model="taskTitle" style="width: 200px" type="text">
                </td>
            </tr>
            <tr>
                <td>任务类型</td>
                <td>
                    <ys-select :option="taskType"
                               :width="200"
                               :selected.sync="taskTypeId"></ys-select>
                </td>
            </tr>
            <tr>
                <td>类型</td>
                <td>
                    <ys-select :option="plugType"
                               :width="200"
                               :selected.sync="plugTypeId" :select-id.sync="plugTypeId.id"></ys-select>
                </td>
            </tr>
            <tr>
                <td>危害等级</td>
                <td>
                    <ys-select :option="dangerLevel"
                               :width="200"
                               :selected.sync="dangerLevelId"></ys-select>
                </td>
            </tr>
        </table>
        <ys-transfer class="m-t-8" :data-list.sync="leftData"
                     :left="'选择插件'"
                     :target-list.sync="rightData"></ys-transfer>
        <div class="aside-foot m-t-20">
            <button class="ys-btn m-r-10" @click="saveAddTask">保存</button>
            <button class="ys-btn ys-btn-white" @click="showAddTask=false">取消</button>
        </div>
    </aside>
    </div>
</template>
<style scoped>
    .color-5c {
        color: #eb5273;
    }

    .color-dc {
        color: #5cb6dc;
    }

    .color-59 {
        color: #59c072;
    }

    .activeLink {
        color: #5ac7d4;
        cursor: pointer;
    }

    .search-table-detail {
        width: 100%;
        word-break: break-all;
        word-wrap: break-word;
    }

    #search-tip {
        right: 0px;
        top: 6px;
    }

    .search-result {
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .search-result.off {
        height: 0px !important;
        min-height: 0px !important;
        padding: 0px;
        overflow: hidden;
    }

    .search-result-box {
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .search-result-box.off {
        height: 0px !important;
        overflow: hidden;
    }

    .search-input-box {
        width: 200px;
        text-align: center;
        display: inline-block;
    }

    .search-input-box input {
        height: 25px;
        width: 180px;
        font-size: 12px;
    }

    .search-input-box div i {
        position: absolute;
        font-size: 20px;
    }

    .search-input-box p {
        line-height: 2;
    }

    .search-result-box {
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .search-result-box.off {
        height: 0px !important;
        overflow: hidden;
    }

    .ys-tag {
        position: relative;
        background: rgba(74, 146, 255, 0.4);
        background: linear-gradient(-135deg, transparent 5px, rgba(74, 146, 255, 0.4) 0);
        border-top-left-radius: 3px;
        border-bottom-right-radius: 3px;
        border-bottom-left-radius: 3px;
        height: 28px;
        padding: 0px 22px 0px 10px;
        display: inline-block;
        line-height: 28px;
        font-size: 12px;
    }

    .ys-tag:before {
        content: '';
        position: absolute;
        top: -1px;
        right: -1px;
        background: linear-gradient(to left bottom, transparent 50%, #4a92ff 0, #4a92ff) 100% 0 no-repeat;
        width: 9px;
        height: 9px;
        transform: translateY(0px) rotate(0deg);
        transform-origin: bottom right;
        border-bottom-left-radius: inherit;
        box-shadow: -.2em .2em .3em -.1em rgba(0, 0, 0, .15);
    }

    .ys-tag .remove {
        position: absolute;
        right: 0px;
        top: 0px;
        width: 12px;
        height: 12px;
        background: #e96157;
        border-top-right-radius: 3px;
        border-bottom-left-radius: 3px;
    }

    .ys-tag .remove i {
        position: absolute
    }

    .tag-box {
        position: relative;
        display: inline-block;
        margin-right: 10px;
        margin-top: 5px;
    }

</style>
<script>
    import Api from '../../lib/api'
    import ysTransfer from 'src/components/transfer.vue'
    import Tooltip from "../../components/tooltip.vue";

    export default {
        name: "scn-search",
        data() {
            return {
                tableUrl: '/api/scan/search/dts',
                tableList: [],
                tableFilter: '',
                searchValue: '',
                curDetailId: '-1',
                addData: [{
                    remove: false
                }, {
                    remove: false
                }],
                showAddConf: false,
                addConfInfo: '',
                showAddTask: false,
                leftData: [],
                rightData: [],
                taskType: [{id: 0, name: '执行一次'}, {id: 1, name: '每天执行'}, {id: 2, name: '每周执行'}, {id: 3, name: '每月执行'}],
                taskTypeId: {id: 0, name: '执行一次'},
                plugType: [{id: 0, name: '插件一'}],
                plugTypeId: {id: 0, name: '插件一'},
                dangerLevel: [{id: '5', name: ''}, {id: 0, name: '低危'}, {id: 1, name: '中危'}, {
                    id: 2,
                    name: '高危'
                }, {id: 3, name: '风险'}, {id: 4, name: '紧急'}],
                dangerLevelId: {id: '5', name: ''},
                autoUpdate: [{id: 0, name: '否'}, {id: 1, name: '是'}],
                autoUpdateId: {id: 0, name: '否'},
                whole: 0,
                taskTitle: '',
                idsArr: [],
                checkAll: false
            }
        },
        ready() {
            this.goSearch();
        },
        components: {
            Tooltip,
            ysTransfer
        },
        methods: {
            /*goLink (ip, port) {
                window.location.href = 'https://' + ip +':'+ port ;
            },*/
            checkAllData(val) {
                if (this.checkAll) {
                    for (let i in this.tableList) {
                        this.tableList[i].selected = true;
                    }
                } else {
                    for (let j in this.tableList) {
                        this.tableList[j].selected = false;
                    }
                }
            },
            goKeyDownSearch(e) {
                if (e.keyCode == 13) {
                    this.$refs.table.Re();
                }
            },
            //新增任务
            saveAddTask() {
                let rightStr = [];
                this.idsArr = [];
                for (let j in this.tableList) {
                    if (this.tableList[j].selected) {
                        this.idsArr.push(this.tableList[j].ip + ':' + this.tableList[j].port);
                    }
                }
                for (let i in this.rightData) {
                    rightStr.push(this.rightData[i].name);
                }
                if (!this.taskTitle) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '任务名称不能为空';
                    return false;
                }
                if (rightStr.length == 0) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '请选择插件';
                    return false;
                }
                if (this.idsArr.length == 0) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '请选择任务分配对象';
                    return false;
                }
                let data = {
                    title: this.taskTitle,
                    plugin: rightStr.join(','),
                    plan: this.taskTypeId.id,
                    ids: this.idsArr.join(','),
                    condition: this.searchValue
                };
                this.$http.post('/api/scan/task', data).then(function (response) {
                    if (response.data.status == 200) {
                        this.$router.go({
                            name: 'scan-task'
                        });
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            addTask() {
                this.idsArr = [];
                for (let j in this.tableList) {
                    if (this.tableList[j].selected) {
                        this.idsArr.push(this.tableList[j].ip + ':' + this.tableList[j].port);
                    }
                }
                if (this.idsArr.length == 0) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '请选择任务分配对象';
                    return false;
                }
                this.plugTypeId = {id: '', name: ''};
                this.clearTaskConf();
                this.getPluginType();
                this.showAddTask = true;
            },
            clearTaskConf() {
                this.taskTitle = '';
                this.taskTypeId = {id: 0, name: '执行一次'};
                this.dangerLevelId = {id: '5', name: ''};
                this.rightData = [].concat([]);
            },
            getPluginType() {
                this.$http.post('/api/scan/plugin/type',).then(function (res) {
                    this.plugType = [{id: '', name: ''}];
                    for (let key in res.data.data) {
                        let obj = {
                            id: res.data.data[key],
                            name: res.data.data[key]
                        };
                        this.plugType.push(obj);
                    }
                    this.plugTypeId = {id: '', name: ''};
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getPlugin() {
                let data = {
                    type: this.plugTypeId.name,
                    risk: this.dangerLevelId.name
                };
                this.$http.get('/api/scan/plugin', data).then(function (res) {
                    this.leftData = [];
                    for (let i in res.data.data) {
                        let obj = {
                            id: res.data.data[i].name,
                            name: res.data.data[i].name,
                            selected: false
                        };
                        this.leftData.push(obj);
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            goSearch() {
                this.$refs.table.Re();
            },
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
            returnSearch() {
                $(".search-result").removeClass("off");
                $(".search-result-box").addClass("off");
            }
        },
        watch: {
            'plugTypeId': function () {
                this.getPlugin();
            },
            'dangerLevelId': function () {
                this.getPlugin();
            },
            'tableList': function () {
                if (this.tableList.length > 0) {
                    for (let j in this.tableList) {
                        this.tableList[j].selected = false;
                    }
                }
                this.checkAll = false;
            }
        }
    }
</script>
