<template>
    <div class="ys-con pos-r">
        <div class="ys-box-con">
            <p>用户可查询、查看、下载已生成的历史报表</p>
        </div>
        <ul class="ys-nav m-t-10">
            <li v-for="list in typeData" @click="clickType(list.id)">
                <a :class="curIndex == list.id ? 'on' : ''">
                    <span class="ys-nav-cor"></span>
                    <span class="text">{{list.name}}</span>
                </a>
            </li>
            <div class="clearfix"></div>
        </ul>
        <div class="ys-box-con">
            <div class="tool-box">
                <div class="fLeft d-i-b">
                    <span class="verticalM m-l-10">当前生成报表共计<span
                            class="ys-success-color m-l-5 m-r-5">{{tableTotal}}</span>份</span>
                </div>
                <div class="ys-search d-i-b m-l-10 fRight">
                    <input type="text" placeholder="输入关键词查询"
                           v-model="searchValue"
                           @blur="tableRe()"
                           @keyup.enter="tableRe()"
                           class="ys-input" style="width:180px;"/>
                    <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                </div>
            </div>
            <table class="ys-table m-t-10">
                <thead>
                <tr>
                    <th>报告名称</th>
                    <th>生成时间</th>
                    <th>报告类型</th>
                    <th>大小</th>
                    <th>操作</th>
                </tr>
                </thead>
                <tbody v-for="list in tableList">
                <tr>
                    <td>{{list.name}}</td>
                    <td>{{list.create_time}}</td>
                    <td v-if="list.template_type==1">定制模版</td>
                    <td v-else>固定模版</td>
                    <td>{{list.docx_size | changeUnit}}</td>
                    <td class="operate">
                        <tooltip :content="'.doc下载'" :delay="0">
                            <a class="ys-success-color" :href="'/api/ssa/report/download/docx/'+ list.id"
                               download="report"><i class="ys-icon icon-cloud-download"></i></a>
                            <!--<a @click="downDocxReportFile(list)"><i class="ys-icon icon-cloud-download"></i></a>-->
                        </tooltip>
                        <tooltip :content="'.pdf下载'" :delay="0">
                            <a :href="'/api/ssa/report/download/pdf/'+ list.id" download="report"><i
                                    class="ys-icon icon-cloud-download"></i></a>
                            <!--<a @click="downPdfReportFile(list)"><i class="ys-icon icon-cloud-download"></i></a>-->
                        </tooltip>
                        <ys-poptip confirm
                                   title="您确认删除此报告吗？"
                                   :placement="'left'"
                                   @on-ok="delReport(list)"
                                   @on-cancel="">
                            <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                        </ys-poptip>
                    </td>
                </tr>
                </tbody>
            </table>
            <table-data :url='tableUrl'
                        :whole.sync="tableTotal"
                        :data.sync="tableList"
                        :filter.sync="tableFilter"
                        :search.sync="searchValue"
                        v-ref:table></table-data>
        </div>
    </div>
</template>
<style scoped>

</style>
<script>
    import Api from 'src/lib/api'

    export default {
        name: "report-mgt",
        data() {
            return {
                tableUrl: "/api/ssa/report/result/dts",
                tableList: "",
                tableTotal: 0,
                searchValue: "",
                tableFilter: {
                    template_type: {'id': 2},
                },
                typeData: [{
                    id: 2, name: '终端安全检查报表'
                }, {
                    id: 3, name: '安全审计报表'
                }, {
                    id: 1, name: '定制报表'
                },],
                curIndex: 2,
            }
        },
        ready() {

        },
        filters: {
            changeUnit(val) {
                if (val < 1024) {
                    return val + "b"
                } else if (val >= 1024 && val < 1024 * 1024) {
                    val = (val / 1024).toFixed(1);
                    return val + "Kb"
                } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024)).toFixed(1);
                    return val + "Mb"
                } else if (val >= 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024 * 1024)).toFixed(1);
                    return val + "Gb"
                }
            }
        },
        methods: {
            downDocxReportFile(list) {
                window.open('/api/ssa/report/download/docx/' + list.id)
            },
            downPdfReportFile(list) {
                window.open('/api/ssa/report/download/pdf/' + list.id)
            },
            clickType(id) {
                this.curIndex = id;
                this.tableFilter.template_type.id = id;
                this.tableRe();
            },
            delReport(list) {
                this.$http.delete('/api/ssa/report/result/' + list.id).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            tableRe() {
                this.$refs.table.Re()
            },
        }
    }
</script>