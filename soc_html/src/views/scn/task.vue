<template>
    <div class="ys-con pos-r">
        <div class="ys-box-con ys-wrap" v-show="!showResult">
            <div class="tool-box">
                <span class="verticalM m-l-10">任务总数<span class="ys-success-color m-l-5 m-r-5">{{whole}}</span>个</span>
            </div>
            <div>
                <table class="ys-table">
                    <thead>
                    <tr>
                        <th></th>
                        <th>名称</th>
                        <th>种类</th>
                        <th>任务类型</th>
                        <th>任务状态</th>
                        <th>时间</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody v-for="list in tableList" track-by="$index">
                    <tr>
                        <td class="detail">
                            <span @click="showDetail($index)">
                              <i class="ys-icon"
                                 v-bind:class="[curDetailId == $index ? 'icon-downlist-up' : 'icon-downlist' ]"></i>
                            </span>
                        </td>
                        <td>{{list.title}}</td>
                        <td>{{list.plugin}}</td>
                        <td>
                            <span v-if="list.plan==0">执行一次</span>
                            <span v-if="list.plan==1">每天执行</span>
                            <span v-if="list.plan==2">每周执行</span>
                            <span v-if="list.plan==3">每月执行</span>
                        </td>
                        <td>
                            <span v-if="list.status==0 && list.plan==0" class="ys-error-color">未开始</span>
                            <span v-if="list.status==1 && list.plan==0" class="ys-primary-color">正在执行</span>
                            <span v-if="list.status==2 && list.plan==0" class="ys-success-color">扫描完成</span>
                            <span v-if="list.plan!=0" class="ys-success-color">已执行{{list.status}}次</span>
                        </td>
                        <td>{{list.time}}</td>
                        <td class="operate">
                            <tooltip :content="'搜索结果'" :delay="0">
                                <a @click="target(list)"><i class="ys-icon icon-eye font14"></i></a>
                            </tooltip>
                            <tooltip :content="'复测'" :delay="0">
                                <a v-if="list.plan==0 && list.status==2" @click="restart(list._id)"><i class="ys-icon icon-refresh font12"></i></a>
                                <a v-else><i class="ys-icon icon-refresh font12 color-ee"></i></a>
                            </tooltip>
                            <tooltip :content="'删除'" :delay="0">
                                <ys-poptip confirm
                                           :title="'确认删除'+list.title+'？'"
                                           :placement="'left'"
                                           @on-ok="delTask(list._id)"
                                           @on-cancel="">
                                    <a class="d-i-b ys-error-color"><i class="ys-icon icon-trash"></i></a>
                                </ys-poptip>
                            </tooltip>
                        </td>
                    </tr>
                    <tr class="detail" v-bind:class="[curDetailId == $index ? 'open' : '' ]">
                        <td>

                        </td>
                        <td colspan="8">
                            <div class="m-b-5">
                                <span class="d-i-b m-t-10 m-r-10 bg-color col-md-2" v-for="item in list.target">
                                    {{item[0] +':'+ item[1]}}
                                </span>
                                <div class="clearfix"></div>
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
        <div v-show="showResult">
            <task-result :id="list._id" :plugin="list.plugin" :show.sync="showResult"></task-result>
        </div>
    </div>
</template>
<style scoped>
    .bg-color{
        background-color: rgba(0, 0, 0, 0.15);
        border-radius: 2px;
        text-align: center;
    }
    .color-ee{
        color: #807b7b;
        cursor: not-allowed;
    }
</style>
<script>
    import Api from '../../lib/api'
    import taskResult from './task_result.vue'
    export default {
        name: "scn-task",
        data() {
            return {
                tableUrl: '/api/scan/task/dts',
                tableList: [],
                tableFilter: '',
                searchValue: '',
                whole: 0,
                curDetailId: '-1',
                list: {},
                showResult: false
            }
        },
        ready() {

        },
        methods: {
            target(list) {
                this.list = list;
                this.showResult = true ;
            },
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
            restart(id) {
                let obj = {
                    taskid: id
                };
                this.$http.post('/api/scan/task/check', obj).then(function (response) {
                    if (response.data.status === 200) {
                        this.$root.alertSuccess = true;
                        this.$root.errorMsg = response.data.msg
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            delTask(id) {
                this.$http.delete('/api/scan/task/' + id).then(function (response) {
                    if (response.data.status === 200) {
                        this.$root.alertSuccess = true;
                        this.$root.errorMsg = response.data.msg
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            tableRe() {
                this.$refs.table.Re()
            },
        },
        components: {
            taskResult
        }
    }
</script>
