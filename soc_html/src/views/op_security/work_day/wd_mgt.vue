<template>
    <div class="ys-box">
        <div class="ys-box-con ys-wrap">
            <div class="ys-box-con">
                工作日设置
            </div>
            <table class="ys-table m-t-10">
                <thead>
                <tr>
                    <th>工作日</th>
                    <th>班次时间段</th>
                    <th>操作</th>
                </tr>
                </thead>
                <tbody>
                <template v-for="list in tableList">
                    <tr>
                        <td>{{ list.week }}</td>
                        <td>
                            <span v-if="list.state == 2">休息</span>
                            <span v-if="list.state == 1">{{list.am_start_time+'—'+list.am_end_time }}</span>
                            <span v-if="list.state == 1" class="m-l-5">{{list.pm_start_time+'—'+list.pm_end_time }}</span>
                        </td>
                        <td class="operate">
                            <tooltip :content="'编辑'" :delay="1000">
                                <a @click="showEdit(list)"><i class="ys-icon icon-edit"></i></a>
                            </tooltip>
                        </td>
                    </tr>
                </template>
                </tbody>
            </table>
        </div>
        <aside :show.sync="configStatus"
               :header="configHead"
               :left="'auto'"
               :width="'500px'">
            <div>
                <radio class="m-b-20" :list="radioData" :value.sync="curRadio"></radio>
                <table class="ys-form-table" v-if="curRadio == 1">
                    <tbody>
                    <tr>
                        <td style="width: 60px">上午:</td>
                        <td>
                            <calendar :type="'time'"
                                      :value.sync="amStartTime"
                                      :text="'选择起始时间'"></calendar>
                            <span class="ys-info-color">—</span>
                            <calendar :type="'time'"
                                      :value.sync="amEndTime"
                                      :text="'选择结束时间'"></calendar>
                        </td>
                    </tr>
                    <tr>
                        <td style="width: 60px">下午:</td>
                        <td>
                            <calendar :type="'time'"
                                      :value.sync="pmStartTime"
                                      :text="'选择起始时间'"></calendar>
                            <span class="ys-info-color">—</span>
                            <calendar :type="'time'"
                                      :value.sync="pmEndTime"
                                      :text="'选择结束时间'"></calendar>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <div class="aside-foot m-t-20">
                    <button class="ys-btn m-r-10" @click="changeConfig()">确定</button>
                    <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
                </div>
            </div>
        </aside>
    </div>
</template>
<script>
    import Api from '../../../lib/api'
    import ysTable from 'src/components/table-data.vue'
    import ysSelect from 'src/components/select.vue'
    import ysPoptip from 'src/components/poptip.vue'
    import aside from 'src/components/Aside.vue'

    export default {
        name: "sm-mgt",
        props: [],
        computed: {},
        data() {
            return {
                tableList: [],
                //添加
                configStatus: false,
                configHead: "编辑",
                editType: 0,
                editId: "",
                radioData: [
                    {id: 1, text: "班"},
                    {id: 2, text: "休"},
                ],
                curRadio: 1,
                week:'',
                amStartTime: '',
                amEndTime: '',
                pmStartTime: '',
                pmEndTime: '',
            }
        },
        ready: function () {
            this.init()
        },
        methods: {
            init() {
                this.$http.get('/api/op_store/workdaylist').then(function (response) {
                    if (response.data.result == 'ok') {
                        this.tableList = response.data.data;
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            showEdit(list) {
                this.configStatus = true;
                this.editId = list.id;
                this.week = list.week;
                this.curRadio = parseInt(list.state);
                if(this.curRadio == 1){
                    this.amStartTime = list.am_start_time
                    this.amEndTime = list.am_end_time
                    this.pmStartTime = list.pm_start_time
                    this.pmEndTime = list.pm_end_time
                }else{
                    this.amStartTime = ''
                    this.amEndTime = ''
                    this.pmStartTime = ''
                    this.pmEndTime = ''
                }
            },
            getSmInfo() {
                let self = this,data = {
                    id:self.editId
                };
                this.$http.get('/api/op_store/workdayedit',data).then(function (response) {
                    if (response.data.status == 200) {
                        self.sm = response.data.data
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            changeConfig() {
                let data = {
                    id:this.editId,
                    week:this.week,
                    state:this.curRadio
                };
                if(this.curRadio == 1){
                    data['am_start_time'] = this.amStartTime;
                    data['am_end_time'] = this.amEndTime;
                    data['pm_start_time'] = this.pmStartTime;
                    data['pm_end_time'] = this.pmEndTime;
                }
                this.$http.put('/api/op_store/workdaysave',data).then(function (response) {
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.configStatus = false;
                        this.init();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            }
        },
        components: {
            ysTable,
            ysSelect,
            ysPoptip,
            aside,
        }
    }

</script>