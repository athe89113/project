<template>
    <div class="ys-box-con pos-r">
        <div class="tool-box">
            <a @click="goBack" class="m-r-10"><i class="ys-icon icon-arrow-left"></i>返回</a>
            <span>{{type}}<span class="ys-success-color"> {{whole}}</span> 个</span>
        </div>
        <div class="ys-wrap">
            <table class="ys-table">
                <thead>
                <tr>
                    <th>地址</th>
                    <th>时间</th>
                    <th>详情</th>
                    <th>危险等级</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="list in tableList" track-by="$index">
                    <td>
                        <!--<a target="_blank" :href="'http://'+list.ip+':'+list.port">{{list.ip+':'+list.port}}</a>-->
                        {{list.ip+':'+list.port}}
                    </td>
                    <td>{{list.time}}</td>
                    <td>{{list.info}}</td>
                    <td>{{list.vul_level}}</td>
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
</template>
<style scoped>

</style>
<script>
    import Api from '../../lib/api'

    export default {
        name: "scn-scan",
        props: {
            id: {
                default: ''
            },
            plugin: {
                default: ''
            },
            show: {
                default: false
            }
        },
        data() {
            return {
                tableUrl: '/api/scan/task/result/dts',
                tableList: [],
                tableFilter: '',
                searchValue: '',
                whole: 0,
                type: ''
            }
        },
        ready() {

        },
        methods: {
            tableRe() {
                this.$refs.table.Re()
            },
            goBack(){
                //this.$router.go({"name": 'scan-task'})
                this.show = false ;
            }
        },
        watch: {
            'show': function () {
                this.searchValue = this.id;
                this.type = this.plugin;
                this.$nextTick(()=>{
                    this.tableRe();
                })
            }
        }
    }
</script>
