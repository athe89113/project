<style lang="less" scoped>
    .ys-textarea {
        min-height: 60px;
    }
</style>
<template>
    <div>
        <table class="ys-form-table">
            <tbody>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">*</span>名称</td>
                <td>
                    <input
                            class="ys-input"
                            placeholder="例：数据库违规"
                            v-model="model.rule_name"
                            style="width: 218px">
                </td>
            </tr>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">*</span>级别</td>
                <td>
                    <ys-select
                            :option="levelOptions"
                            :select-id.sync="model.level"
                            :width="218">
                    </ys-select>
                </td>
            </tr>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">*</span>时间范围</td>
                <td>
                    <ys-select
                            :option="timeOptions"
                            :select-id.sync="model.time_type"
                            :width="218">
                    </ys-select>
                    <div class="displayIB" class="m-l-5" v-if="model.time_type == '1'">
                        <input v-model="model.interval" @change="interval" type="number" class="ys-input"
                               style="width:48px;"><span class="m-l-5">分钟</span>
                    </div>
                    <div class="displayIB m-l-5" v-if="model.time_type == '2'">
                        <calendar :type="'time'"
                                  :value.sync="model.time_start"
                                  :text="'选择起始时间'"></calendar>
                        <span class="m-l-5 m-r-5">~</span>
                        <calendar :type="'time'"
                                  :value.sync="model.time_end"
                                  :text="'选择终止时间'"></calendar>
                    </div>
                </td>
            </tr>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">&nbsp;</span>描述</td>
                <td>
                    <textarea
                            class="ys-textarea"
                            placeholder="例：关于"
                            style="width:585px;"
                            v-model="model.description">
                    </textarea>
                </td>
            </tr>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">*</span>是否启用</td>
                <td>
                    <ys-switch :checked.sync="model.status">
                        <span slot="open">开启</span>
                        <span slot="close">关闭</span>
                    </ys-switch>
                </td>
            </tr>
            <tr>
                <td><span class="ys-error-color m-r-5 vertical-middle">*</span>规则条件</td>
                <td>
                    <div style="line-height: 30px" v-for="($index,list) in model.content" :key="$index">
                        <span v-if="$index" class="ys-success-color m-r-5">或</span>
                        <span v-if="list.event_type">[<span>&nbsp;</span>事件类型<span>&nbsp;=&nbsp;</span>{{list.event_type.name}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'event_type'">&nbsp;&&</span></span>
                        <span v-if="list.count">[<span>&nbsp;</span>发生次数<span>&nbsp;>=&nbsp;</span>{{list.count}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'count'">&nbsp;&&</span></span>
                        <span v-if="list.sourceIp">[<span>&nbsp;</span>源IP <span>&nbsp;=&nbsp;</span> {{list.sourceIp | formatter}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'sourceIp'">&nbsp;&&</span></span>
                        <span v-if="list.sourcePort">[<span>&nbsp;</span>源端口 <span>&nbsp;=&nbsp;</span> {{list.sourcePort | formatter}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'sourcePort'">&nbsp;&&</span></span>
                        <span v-if="list.targetIp">[<span>&nbsp;</span>目标IP <span>&nbsp;=&nbsp;</span> {{list.targetIp | formatter}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'targetIp'">&nbsp;&&</span></span>
                        <span v-if="list.targetPort">[<span>&nbsp;</span>目标端口 <span>&nbsp;=&nbsp;</span> {{list.targetPort | formatter}}<span>&nbsp;</span>]<span
                                v-if="list.last != 'targetPort'">&nbsp;&&</span></span>
                        <a class="ys-error-color m-l-5" @click="delCondition($index)"><i
                                class="ys-icon icon-trash"></i></a>
                    </div>
                </td>
            </tr>
            <tr>
                <td></td>
                <td style="border: 1px dashed #ccc">
                    <table class="ys-form-table">
                        <tbody>
                        <tr>
                            <td class="p-l-10">事件类型</td>
                            <td>
                                <div class="displayIB" v-bind:class="[bool.event_type?'':'disabled']">
                                    <ys-select
                                            :option="eventOptions"
                                            :selected.sync="condition.event_type"
                                            :width="218">
                                    </ys-select>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class="p-l-10">发生次数</td>
                            <td>
                                <span>大于等于</span>
                                <input v-model="condition.count" @change="positive" type="number"
                                       class="ys-input"
                                       style="width:48px;"><span class="m-l-5">次</span>
                            </td>
                        </tr>
                        <tr>
                            <td class="p-l-10">源IP范围</td>
                            <td>
                                <textarea
                                        class="ys-textarea m-r-10"
                                        style="width:440px;vertical-align: middle"
                                        placeholder="例：192.168.24.77-192.168.109.109;192.168.12.112"
                                        v-model="condition.sourceIp | trim">
                                </textarea>
                                <tooltip id="search-tip" :delay="400" :placement="'left'" :visible.sync="true">
                                    <div slot="content">
                                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                                            <p>地址段使用减号（-）进行分隔</p>
                                            <p>多个ip或ip段使用英文分号（;）进行分隔</p>
                                        </div>
                                    </div>
                                    <span>
                                        <i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                                    </span>
                                </tooltip>
                            </td>
                        </tr>
                        <tr>
                            <td class="p-l-10">源端口</td>
                            <td>
                                <textarea
                                        rows="2"
                                        class="ys-textarea m-r-10"
                                        placeholder="例：8000;80"
                                        style="width:440px;vertical-align: middle"
                                        v-model="condition.sourcePort | trimPort">
                                </textarea>
                                <tooltip id="search-tip" :delay="400" :placement="'left'" :visible.sync="true">
                                    <div slot="content">
                                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                                            <p>多个端口使用英文分号（;）进行分隔</p>
                                        </div>
                                    </div>
                                    <span>
                                        <i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                                    </span>
                                </tooltip>
                            </td>
                        </tr>
                        <tr>
                            <td class="p-l-10">目标IP范围</td>
                            <td>
                                <textarea
                                        class="ys-textarea m-r-10"
                                        style="width:440px;vertical-align: middle"
                                        placeholder="例：192.168.24.77-192.168.109.109;192.168.12.112"
                                        v-model="condition.targetIp | trim">
                                </textarea>
                                <tooltip id="search-tip" :delay="400" :placement="'left'" :visible.sync="true">
                                    <div slot="content">
                                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                                            <p>地址段使用减号（-）进行分隔</p>
                                            <p>多个ip或ip段使用英文分号（;）进行分隔</p>
                                        </div>
                                    </div>
                                    <span>
                                        <i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                                    </span>
                                </tooltip>
                            </td>
                        </tr>
                        <tr>
                            <td class="p-l-10">目标端口</td>
                            <td>
                                <textarea
                                        class="ys-textarea m-r-10"
                                        style="width:440px;vertical-align: middle"
                                        placeholder="例：8000;3000"
                                        v-model="condition.targetPort| trimPort">
                                </textarea>
                                <tooltip id="search-tip" :delay="400" :placement="'left'" :visible.sync="true">
                                    <div slot="content">
                                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                                            <p>多个端口使用英文分号（;）进行分隔</p>
                                        </div>
                                    </div>
                                    <span>
                                        <i class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                                    </span>
                                </tooltip>
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td>
                                <button class="ys-btn ys-btn-blue" @click="addCondition">添加条件</button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
        <div class="m-t-10 m-b-10">
            <button class="ys-btn m-r-10" @click="save">保存</button>
            <button class="ys-btn ys-btn-white m-r-10" @click="cancel">取消</button>
        </div>
    </div>
</template>
<script>
    import Api from 'src/lib/api'

    export default {
        name: 'safe_rule-add',
        props: {
            id: '',
            groupId: ''
        },
        data() {
            return {
                model: {
                    rule_name: '',
                    level: 1,
                    status: true,
                    description: '',
                    time_type: '1',
                    interval: 5,
                    time_start: '08:00:00',
                    time_end: '10:00:00',
                    content: [],
                },
                levelOptions: [{
                    id: 1, name: '严重'
                }, {
                    id: 2, name: '重大'
                }, {
                    id: 3, name: '次要'
                }, {
                    id: 4, name: '警告'
                }],
                condition: {
                    event_type: {id: -1, name: '未选择'},        //事件类型
                    count: 10,
                    sourceIp: '',
                    sourcePort: '',
                    targetIp: '',
                    targetPort: '',
                },
                bool: {
                    event_type: true,
                    count: true,
                    sourceIp: true,
                    sourcePort: true,
                    targetIp: true,
                    targetPort: true,
                },
                eventOptions: [],
                timeOptions: [{
                    id: '1', name: '时间间隔',
                }, {
                    id: '2', name: '时间范围',
                }]
            };
        },
        ready() {
            this.init();
        },
        filters: {
            formatter(value) {
                let val = value.replace(/;/g, ' || ');
                return val;
            },
            trim: {
                read: function (input) {
                    let _input = input.replace(/；/g, ';');
                    return _input.replace(/[^0-9\;\-\.\n]/g, '');
                },
                write: function (input) {
                    let _input = input.replace(/；/g, ';');
                    return _input.replace(/[^0-9\;\-\.\n]/g, '');
                }
            },
            trimPort: {
                read: function (input) {
                    let _input = input.replace(/；/g, ';');
                    return _input.replace(/[^0-9\;\-\.\n]/g, '');
                },
                write: function (input) {
                    let _input = input.replace(/；/g, ';');
                    return _input.replace(/[^0-9\;\-\.\n]/g, '');
                }
            }
        },
        methods: {
            positive() {
                this.condition.count = this.condition.count <= 0 ? 0 : this.condition.count
            },
            interval(){
                this.model.interval = this.model.interval <= 0 ? 0 : this.model.interval;
            },
            init() {
                this.$http.post('/api/op_store/alarm_rule/event_type', {}).then(function (response) {
                    this.eventOptions = response.data.data;
                    this.eventOptions.unshift({id: -1, name: '未选择'})
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
                if (!this.id) return false; //不存在id不请求详情
                this.$http.get(`/api/op_store/alarm_rule/${this.id}`, {}).then(function (response) {
                    if (response.data.status == 200) {
                        let res = response.data.data;
                        res.content = JSON.parse(response.data.data.content)
                        res.status = res.status == 1 ? true : false
                        this.model = res;
                    } else {
                        this.$root.errorMsg = response.data.msg;
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },
            save() {
                if (!this.model.content.length) {
                    this.$root.errorMsg = '请至少添加一个规则条件';
                    this.$root.alertError = true
                    return false;
                }
                if (this.id) {
                    let obj = Object.assign({
                        id: this.id,
                        group_id: this.groupId,
                    }, this.model);
                    this.$http.put(`/api/op_store/alarm_rule`, obj).then(function (response) {
                        this.$root.errorMsg = response.data.msg;
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true
                            this.cancel();
                        } else {
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                } else {
                    let obj = Object.assign({
                        group_id: this.groupId,
                    }, this.model);
                    this.$http.post(`/api/op_store/alarm_rule`, obj).then(function (response) {
                        this.$root.errorMsg = response.data.msg;
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true
                            this.cancel();
                        } else {
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                }

            },
            cancel() {
                this.$emit('cancel')
            },
            addCondition() {
                let item = {};
                for (let i in this['bool']) {
                    if (this['bool'][i] && this.condition[i]) {
                        item[i] = this.condition[i];
                    }
                }
                if (item.event_type && item.event_type.id == -1) delete item['event_type'];
                if (JSON.stringify(item) === "{}") {
                    this.$root.errorMsg = '至少选择一项不为空';
                    this.$root.alertError = true;
                    return false;
                }
                item['last'] = Object.keys(item)[Object.keys(item).length - 1]; //对象最后一个
                if (JSON.stringify(this.model.content).indexOf(JSON.stringify(item)) != -1) {
                    this.$root.errorMsg = '不可重复添加相同条件';
                    this.$root.alertError = true;
                    return false;
                }
                this.model.content.push(item);
                this.clearModel()
            },
            delCondition(index) {
                this.model.content.splice(index, 1);
            },
            CompareDate(t1, t2) {
                var date = new Date();
                var a = t1.split(":");
                var b = t2.split(":");
                return date.setHours(a[0], a[1], a[2]) > date.setHours(b[0], b[1], b[2]);
            },
            clearModel() {
                this.condition = {
                    event_type: {id: -1, name: '未选择'},        //事件类型
                    count: 10,
                    sourceIp: '',
                    sourcePort: '',
                    targetIp: '',
                    targetPort: '',
                };
            }
        },
        watch: {
            id() {
                this.init();
            },
            'model.time_start': function () {
                if (this.model.time_start && this.model.time_end && this.CompareDate(this.model.time_start, this.model.time_end)) {
                    let time = this.model.time_end;
                    this.model.time_end = this.model.time_start;
                    this.model.time_start = time;
                }
            },
            'model.time_end': function () {
                if (this.model.time_start && this.model.time_end && this.CompareDate(this.model.time_start, this.model.time_end)) {
                    let time = this.model.time_end;
                    this.model.time_end = this.model.time_start;
                    this.model.time_start = time;
                }
            },
        },
        components: {}
    }
    ;
</script>